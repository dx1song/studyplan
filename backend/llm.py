"""LLM 接口调用封装。

使用 OpenAI SDK 的兼容接口，可对接 DeepSeek、通义千问（DashScope 兼容模式）、
OpenAI 等任意支持 /chat/completions 的服务，通过环境变量切换。
"""

import json
import os

from openai import OpenAI

from prompts import SYSTEM_PROMPT, build_user_prompt
from mock_data import build_mock_plan


def _is_mock() -> bool:
    return os.getenv("USE_MOCK", "").strip().lower() in ("1", "true", "yes")


def call_llm(student: dict) -> str:
    """调用大模型生成学习计划，返回原始文本（JSON 字符串）。"""
    if _is_mock():
        return json.dumps(build_mock_plan(student), ensure_ascii=False)

    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError(
            "未配置 LLM_API_KEY。请在 backend/.env 中配置，"
            "或设置 USE_MOCK=true 进行无密钥联调。"
        )

    client = OpenAI(
        api_key=api_key,
        base_url=os.getenv("LLM_BASE_URL") or None,
    )

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(student)},
        ],
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.4")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "4096")),
    )
    return (response.choices[0].message.content or "").strip()
