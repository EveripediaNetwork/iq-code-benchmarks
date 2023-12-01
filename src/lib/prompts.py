from langchain.prompts import PromptTemplate

issues_prediction_prompt = PromptTemplate.from_template(
    """
You will be analyzing a smart contract to identify any potential security vulnerabilities present within the code. Your output will be crucial for improving the contract's security posture.

Please make sure you are provided with the following information:
- The complete, unaltered smart contract code enclosed within <code> tags.

Follow these instructions carefully:

Dos:
- Conduct a thorough examination of the provided <code> to uncover any vulnerabilities.
- Assign a severity level to each vulnerability found: High, Medium, Low, or as an Optimization effort.
- Include a clear, concise description of each vulnerability, detailing why it is a security concern.
- Use the specified format without deviation for your output.

Don'ts:
- Refrain from suggesting corrections or methods to rectify the identified vulnerabilities.
- Avoid listing vulnerabilities that merely offer informational severity without signifying a real threat to security.
- Ensure that your analysis remains objective and refrain from incorporating subjective judgments about the code quality or style.

Your output should strictly follow the format below, with each identified vulnerability detailed on its own separate lines followed by a blank line:

<S No.>) <Vulnerability Category> - <Vulnerability Description> [<Impact>]

What follows is the smart contract code:

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
