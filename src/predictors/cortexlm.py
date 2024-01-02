#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cortex.loaders.string import Loader
from cortex.slicers.solidity import Slicer
from cortex.llm.openai import LLM, ModelNames
from cortex.mappers.solidity_vulnerabilities import Mapper as SolidityVulnerabilitiesMapper  # noqa: E501
from cortex.injectors.mythirl import Injector as MythirlInjector
from cortex.injectors.slither import Injector as SlitherInjector
from cortex.injectors.basic import Injector as BasicInjector
from cortex.output_validators.json import Validator as JSONValidator
from cortex import (
    Cortex,
    Prompt,
    Context,
    Reducer,
)


def cortexlm(prompt: str, **kwargs):
    """
    Run the IQ Code CortexLM with the given prompt. here the prompt
    must be proper solidity code.
    """
    loader = Loader(prompt)
    slicers = [Slicer(code, include_global_code=True) for code in loader.code]

    json_validator = JSONValidator([{
        "function": str,
        "defect": str,
        "exists": bool,
        "description": str,
    }])

    slice_prompts = []
    for slicer in slicers:
        for code_context in slicer.contexts:
            prompt = Prompt(
                [code_context],
                validator=json_validator,
            )
            slice_prompts.append(prompt)

    main_prompts = []
    for code in loader.code:
        prompt = Prompt([
            Context(
                code,
                tag='code',
            ),
        ],
            validator=json_validator
        )
        main_prompts.append(prompt)

    mythil_injector = MythirlInjector()
    mythil_injector.inject(main_prompts)

    slither_injector = SlitherInjector()
    slither_injector.inject(main_prompts)

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
        """,
        tag='footer',
    )
    footer_injector = BasicInjector(footer)
    footer_injector.inject(prompts)

    llm = LLM(model=ModelNames.GPT_3_5)

    reducer = Reducer()

    cortex = Cortex(
        prompts=prompts,
        llm=llm,
        reducer=reducer,
    )

    final_output = []
    for output in cortex.run():
        final_output.append(output)

    return "\n".join(final_output) + "\n"
