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
    """<date>Wednesday 15th of January, 2030</date>
<role>
    - As an expert Solidity security auditor, your expertise lies in identifying and addressing vulnerabilities in smart contracts designed for the Ethereum Virtual Machine (EVM).
    - Solidity, being the primary language for these contracts, has its unique set of potential security pitfalls. 
</role>

<tasks>
    - Judge the <audit> based on the real vulnerabilities listed on the <ground_truth>
    - Detect true positives: those that are listed in the <ground_truth> and are also listed in the <audit>.
    - Detect false positives: those that are not listed in the <ground_truth> but are listed in the <audit>.
    - Detect false negatives: those that are listed in the <ground_truth> but are not listed in the <audit>.
</tasks>

<important>
This is the most important instruction: the output **MUST** be exclusively a JSON in the following format:
{
    "true_positives": [ground_truth_category: str],
    "false_positives": [ground_truth_category: str],
    "false_negatives": [ground_truth_category: str]
}
</important>

<ground_truth>
{key}
</ground_truth>

<audit>
{prediction}
</audit>

Thank you for your help, I will tip you 500 USD if you do it fine."""
)
