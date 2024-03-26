Prompt builder should return a formatted string that the llm can use. We need to
fill it up with some information in order to do that.

# Data in the full file:

- analysis_message
- solved_example_file_name
- solved_example_diff XOR (solved_example_before AND solved_example_after)
- src_file_name
- analysis_line_number
- src_file_name
- src_file_contents

- Load up the model choice. Each model may respond differently to different
  formats.
- "Group by" formatting

<!-- Always follows format of:

thing: <wrap-begin>{var_for_thing}<wrap-end> -->

# Future

Chain of thought reasoning for CodePlan

---

# Java EE to Quarkus Migration

Blah blah blah

# Input information

## Input file

File name: "{src_file_name}"
Source file contents:

```{src_file_language}
{src_file_contents}
```

## Issue(s, do plural) to fix

1.  - Issue to fix: "{analysis_message}"
    - Line number: {analysis_line_number} <!-- may be a list -->
    - Solved example <!-- if present -->:

2.  - Issue to fix: "{analysis_message}"
    - Line number: {analysis_line_number}
    - Solved example <!-- if present -->:

# Output instructions

Structure your output in the following Markdown format:

## Reasoning

Write the step by step reasoning in this markdown section. If you are unsure of a step or reasoning, clearly state you are unsure and why.

## Updated File

```{src_file_language}
// Write the updated file for Quarkus in this section
```
