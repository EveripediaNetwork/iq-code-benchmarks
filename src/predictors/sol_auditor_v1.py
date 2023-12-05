import runpod
import os


def sol_auditor_v1(prompt: str, **kwargs):
    """
    Run the Sol Auditor LLM with the given prompt.
    """
    runpod.api_key = os.getenv("RUNPOD_API_KEY")
    endpoint = runpod.Endpoint(os.getenv("SOL_AUDITOR_V1_ENDPOINT_ID"))

    run_request = endpoint.run_sync(
        {
            "input": {
                "prompt": prompt,
                **kwargs,
            }
        }
    )

    return "".join(run_request["output"])
