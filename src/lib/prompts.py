from langchain.prompts import PromptTemplate

issues_prediction_prompt = PromptTemplate.from_template(
    """You will be given a smart contract. Your task is to find any vulnerabilities in the contract.

You are provided with:
- <code>: the smart contract code

Dos
- Analyze the <code> and find any vulnerabilities
- Categorize the vulnerabilities found into High, Medium, Low
- Provide a description of the vulnerability
- Follow the format of the output

Dont's
- Do not provide a solution or fix to the vulnerability
- Do not provide improvement suggestions that are not serious vulnerabilities (e.g. gas optimization, logging, magic numbers, etc.)
- Do not provide opinionated views on the code.

The output should be lines of vulnerabilities seperated by new empty line **exclusively** in the format of:
<S No.>) <Vulnerability Category> - <Vulnerability Description> [<impact>]

<code>
{code}
</code>
"""
)

judge_predictions_prompt = PromptTemplate.from_template(
    """Your role is to to judge a code audit:
- blockchain: ethereum
- language: solidity

You are provided with:
- <ground_truth>: the real and only vulnerabilities that exist in the code
- <audit>: the audit to be judged by an external system

Dos
- Analyze the <audit> based on the real vulnerabilities listed on the <ground_truth>
- Detect true positives
- Detect false positives
- Detect false negatives

Dont's
- Vulnerabilities not listed in the <ground_truth> are considered false positives
- Judge based on your knowledge how well the <audit> is comparing it to the <ground_truth>
- True positives lists vulnerabilities other than the ones listed in the <ground_truth>

The output should be **exclusively** in json format with keys:
- false_negatives: array of issue categories
- false_positives: array of issue categories
- true_positives: array of issue categories

Where each element of the array is the category name of the vulnerability.

<ground_truth>
{key}
</ground_truth>

<audit>
{prediction}
</audit>"""
)
