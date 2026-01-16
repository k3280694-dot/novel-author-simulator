"""DeepSeek client utilities for AI editing suggestions."""

from __future__ import annotations

import os

from openai import OpenAI


def format_state_for_ai(state: dict) -> str:
    period_label = {1: "上旬", 2: "中旬", 3: "下旬"}.get(state.get("period"), "未知")
    signed_label = "已签约" if state.get("signed") else "未签约"
    in_v_label = "已入 V" if state.get("in_v") else "未入 V"

    parts = [
        "你是一名网文编辑，请根据作者当前情况给出简短编辑建议（中文，3-5 条即可）。",
        f"进度：第 {state.get('month')} 月 {period_label}",
        f"总字数：{state.get('words')}，上旬新增：{state.get('last_period_words')}",
        f"收藏：{state.get('book_favorites')}，粉丝：{state.get('fans')}",
        f"余额：{state.get('balance')} 元，生活月支出：{state.get('monthly_expense')} 元",
        f"压力：{state.get('stress')}/100，健康：{state.get('health')}/100，动力：{state.get('motivation')}/100",
        f"签约状态：{signed_label}，入 V 状态：{in_v_label}",
    ]
    return "\n".join(parts)


def ask_deepseek(prompt: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("缺少 DeepSeek API Key，请设置环境变量 DEEPSEEK_API_KEY。")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
    except Exception as exc:  # pragma: no cover - depends on upstream client
        message = str(exc)
        lowered = message.lower()
        if "insufficient" in lowered or "balance" in lowered or "quota" in lowered:
            raise RuntimeError("DeepSeek 余额不足或额度耗尽，请检查账户余额。") from exc
        raise RuntimeError(f"DeepSeek 调用失败：{message}") from exc

    content = response.choices[0].message.content if response.choices else ""
    if not content:
        raise RuntimeError("DeepSeek 返回内容为空，请稍后重试。")
    return content.strip()
