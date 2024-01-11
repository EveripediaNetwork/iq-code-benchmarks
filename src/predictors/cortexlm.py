#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cortex.loaders.path import Loader
from cortex.slicers.solidity import Slicer
from cortex.llm.openai import LLM, ModelNames
from cortex.mappers.solidity_vulnerabilities import Mapper as SolidityVulnerabilitiesMapper  # noqa: E501
from cortex.injectors.mythirl import Injector as MythirlInjector
from cortex.injectors.slither import Injector as SlitherInjector
from cortex.output_validators.json import Validator as JSONValidator
from cortex.injectors.basic import Injector as BasicInjector
from cortex import (
    Cortex,
    Prompt,
    Context,
    Reducer,
)
import tempfile
import os


json_validator = JSONValidator([{
    "function": str,
    "defect": str,
    "exists": bool,
    "description": str,
}])


def cortexlm(prompt: str, **kwargs):
    """
    Run the IQ Code CortexLM with the given prompt. here the prompt
    must be proper solidity code.
    """
    # Create a temporary file and store the code there and load it into loader
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(prompt)
        f.flush()
        loader = Loader(f.name)
        file_name = f.name

    loader = Loader(file_name)
    slicers = [Slicer(code, include_global_code=True) for code in loader.code]

    slice_prompts = []
    for slicer in slicers:
        for context in slicer.contexts:
            prompt = Prompt([context], validator=json_validator)
            prompt.add_context(Context(
                f"""
                - Analyze **exclusively** in the presence of {context.tag} in <code>.
                - Do not explain the defect if not present in the <code>.
                - Be brief and concise.

                This is the most important sentence:
                Output format:
                [
                    {{
                        "function": str,
                        "defect": str,
                        "exists": bool,
                        "description": str
                    }}
                ]
                Do not wrap the output in any codeblocks, directly paste the JSON.
                """,
                tag='footer',
            ))
            slice_prompts.append(prompt)

    main_prompts = []
    for code in loader.code:
        prompt = Prompt([Context(
            code,
            tag='code',
        )], validator=json_validator)
        prompt.add_context(Context(
            f"""
            - Analyze **exclusively** in the presence of {prompt._contexts[0].tag} in <code>.
            - Do not explain the defect if not present in the <code>.
            - Be brief and concise.

            This is the most important sentence:
            Output format:
            [
                {{
                    "function": str,
                    "defect": str,
                    "exists": bool,
                    "description": str
                }}
            ]
            Do not wrap the output in any codeblocks, directly paste the JSON.
            """,
            tag='footer',
        ))
        main_prompts.append(prompt)

    mythil_injector = MythirlInjector()
    mythil_injector.inject(main_prompts)

    slither_injector = SlitherInjector()
    slither_injector.inject(main_prompts)

    slices_mapper = SolidityVulnerabilitiesMapper(scopes=['local'])
    global_mapper = SolidityVulnerabilitiesMapper(scopes=['global'])

    slice_prompts = list(slices_mapper.map(slice_prompts))
    main_prompts = list(global_mapper.map(main_prompts))

    prompts = main_prompts + slice_prompts

    mapper = SolidityVulnerabilitiesMapper()
    prompts = list(mapper.map(prompts))

    footer = Context(
        f"""
            - Analyze **exclusively** the presence of {mapper.start_tag} in <code>.
            - Do not explain the defect if not present in the <code>.
            - Be brief and concise.

            This is the most important sentence:
            Output format:
            [
                {{
                    "function": str,
                    "defect": str,
                    "exists": bool,
                    "description": str
                }}
            ]
        Do not wrap the output in any codeblocks, directly paste the JSON.
        """,
        tag='footer',
    )
    footer_injector = BasicInjector(footer)
    footer_injector.inject(prompts)

    llm = LLM(model=ModelNames.GPT_3_5)

    reducer = Reducer(llm, None)

    cortex = Cortex(
        prompts=prompts,
        llm=llm,
        reducer=reducer,
    )

    final_output = []
    for output in cortex.run():
        final_output.append(output)

    # remove the temporary file
    os.remove(file_name)

    return "\n".join(final_output) + "\n"
