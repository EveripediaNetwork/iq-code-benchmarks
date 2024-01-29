#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cortex.loaders.path import PathLoader as Loader
from cortex.slicers.solidity import Slicer
from cortex.output_validators.json import Validator as JSONValidator
from cortex import (
    Cortex,
    Prompt,
    Context,
)
from cortex.mappers.solidity_issues import Mapper as SolidityIssuesMapper
from cortex.processors.static_analysis.mythirl import Processor as MythirlProcessor
from cortex.processors.static_analysis.slither import Processor as SlitherProcessor
from cortex.injectors.basic import Injector as BasicInjector
from cortex.processors.llm.openai import LLM, ModelNames
import os
import tempfile


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

    # ==========================================================================
    # 1️⃣ PROCESSOR: LLM - Collect the prompts from code slices and use LLM to detect issues
    # ==========================================================================

    json_validator = JSONValidator([{
        "function": str,
        "issue": str,
        "title": str,
        "description": str,
        "severity": str,
        "exists": bool,
    }])

    # 📚 CREATE: slice and main prompts which contains prompts on code slices and the whole code respectively
    slicers = [Slicer(code, include_global_code=True) for code in loader.code]
    slice_prompts = [Prompt([code_context], json_validator) for slicer in slicers for code_context in slicer.contexts]
    main_prompts = [Prompt([Context(code, tag='code')], json_validator) for code in loader.code]

    # 💉 INJECT: Every prompt with footer to instruct the LLM to produce output properly
    footer_injector = BasicInjector(Context(
        """
            - Analyze **exclusively** in the presence of the given <code>.
            - Do not explain the defect if not present in the <code>.
            - Be brief and concise.

            This is the most important sentence:
            Output format:
            [
                {{
                    "function": str,
                    "issue": str,
                    "title": str,
                    "description": str,
                    "severity": str,
                    "exists": bool
                }}
            ]
            Do not wrap the output in any codeblocks, directly paste the JSON.
        """,
        tag='footer',
    ))
    footer_injector.inject(slice_prompts)
    footer_injector.inject(main_prompts)

    # 🗺️ MAP: map all the prompts
    slices_mapper = SolidityIssuesMapper(scopes=['local'])
    slice_prompts = list(slices_mapper.map(slice_prompts))
    main_prompts = list(slices_mapper.map(main_prompts))
    prompts = slice_prompts + main_prompts
    llm = LLM(model=ModelNames.GPT_4_TURBO)
    llm_processor_output = llm.process(prompts)

    # ==========================================================================
    # 2️⃣ PROCESSOR: Static Analysis - Mythril and Slither
    # ==========================================================================
    mythril_processor = MythirlProcessor()
    slither_processor = SlitherProcessor()
    mythril_processor_output = mythril_processor.process(loader.code[0])
    slither_processor_output = slither_processor.process(loader.code[0])

    # ==========================================================================
    #  🛠️ Initialize Cortex and pass the processor outputs to get organized results
    # ==========================================================================
    cortex = Cortex(
        llm=llm,
        grouped_outputs=[
            mythril_processor_output,
            slither_processor_output,
            llm_processor_output,
        ],
    )

    # remove the temporary file
    os.remove(file_name)

    final_output = []
    for output in cortex.outputs:
        if (output.get('exists')):
            final_output.append(output)

    return "\n".join(final_output) + "\n"
