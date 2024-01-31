# Notes

## Interesting Papers

- [ReAct: SYNERGIZING REASONING AND ACTING IN LANGUAGE MODELS](https://arxiv.org/pdf/2210.03629.pdf)
- [Repository-Level Prompt Generation for Large Language Models of Code](https://arxiv.org/abs/2206.12839v2)
- [CodePlan: Repository-level Coding using LLMs and Planning](https://arxiv.org/pdf/2309.12499.pdf)
- [Guiding Language Models of Code with Global Context using Monitors](https://arxiv.org/abs/2306.10763)
  - https://github.com/microsoft/monitors4codegen
  - Highlights:
    Some recent approaches use static analysis (Shrivastava et al., 2022; Ding et al., 2022; Pei et al., 2023)
    or retrieval (Zhang et al., 2023) to extract relevant code fragments from the global context. These approaches expand the prompt (Shrivastava et al., 2022; Pei et al., 2023; Zhang et al., 2023) or require architecture modifications (Ding et al., 2022) and additional training (Ding et al., 2022; Pei et al.,
    2023). In comparison, we provide token-level guidance to a frozen LM by invoking static analysis on demand. Our method is complementary to these approaches as they condition the generation by modifying the input to the LM, whereas we apply output-side constraints by reshaping the logits.
- [RepoFusion: Training Code Models to Understand Your Repository](https://arxiv.org/pdf/2306.10998.pdf)
- [RAG vs Fine-tuning: Pipelines, Tradeoffs, and a Case Study on Agriculture](https://arxiv.org/abs/2401.08406)
- [QUANTIFYING LANGUAGE MODELS’ SENSITIVITY TO SPURIOUS FEATURES IN PROMPT DESIGN or: How I learned to start worrying about prompt formatting](https://arxiv.org/pdf/2310.11324.pdf)
- [LLaMA-Reviewer: Advancing Code Review Automation with Large Language Models through Parameter-Efficient Fine-Tuning](https://arxiv.org/pdf/2308.11148v2.pdf)

## Interesting Blog Posts/Examples/Tutorials

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://react-lm.github.io/)
- [Fine-Tune LLaMA 2 with QLoRA](https://colab.research.google.com/drive/1Zmaceu65d7w4Tcd-cfnZRb6k_Tcv2b8g?usp=sharing)
  - From: https://github.com/smol-ai/llama-fine-tuning-hackameetup/tree/main#getting-started
- [Codebase Analysis: Langchain Agents](https://carbonated-yacht-2c5.notion.site/Codebase-Analysis-Langchain-Agents-0b0587acd50647ca88aaae7cff5df1f2)

## Interesting Projects

- [LLMLingua: Enhancing Large Language Model Inference via Prompt Compression](https://github.com/microsoft/LLMLingua)
