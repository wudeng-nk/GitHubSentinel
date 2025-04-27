# src/llm.py

import os
from openai import OpenAI
from logger import LOG

class LLM:
    def __init__(self):
        self.client = OpenAI()
        LOG.add("daily_progress/llm_logs.log", rotation="1 MB", level="DEBUG")

    def generate_daily_report(self, markdown_content, dry_run=False):
        prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
        
        if dry_run:
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(prompt)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"

        LOG.info("Starting report generation using GPT model.")
        LOG.info("Prompt: {}", prompt)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "你是一名专业的技术文档撰写助手，擅长将项目进展整理为结构清晰、重点突出的日报。"
                            "请严格按照以下要求生成报告：\n"
                            "1. 结构分明，分为【新增功能】、【主要改进】、【修复问题】三大部分，每部分用小标题标明。\n"
                            "2. 每个部分下，条理清晰地列出要点，避免冗余和重复，合并同类项。\n"
                            "3. 语言简洁、准确，避免主观臆断，仅基于输入内容总结。\n"
                            "4. 保持客观中立，避免夸大其词。\n"
                            "5. 输出为标准Markdown格式。\n"
                            "6. 只允许生成中文。\n"
                            "如无相关内容的部分，请注明“无”。"
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            LOG.debug("GPT response: {}", response)
            return response.choices[0].message.content
        except Exception as e:
            LOG.error("An error occurred while generating the report: {}", e)
            raise

