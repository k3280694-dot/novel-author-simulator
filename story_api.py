from typing import Dict, List

from deepseek_client import ask_deepseek


def _summarize_state(state: Dict) -> str:
    period = state.get("period", "未知旬")
    month = state.get("month", "未知月")
    total_words = state.get("total_words", state.get("words", "未知"))
    favorites = state.get("favorites", state.get("collect", "未知"))
    fans = state.get("fans", state.get("followers", "未知"))
    pressure = state.get("pressure", "未知")
    health = state.get("health", "未知")
    motivation = state.get("motivation", state.get("energy", "未知"))
    balance = state.get("balance", state.get("money", "未知"))
    signed = state.get("signed", state.get("is_signed", "未知"))
    vip = state.get("vip", state.get("is_vip", "未知"))

    summary_parts = [
        f"当前进度：{month}第{period}",
        f"总字数：{total_words}",
        f"收藏数：{favorites}",
        f"粉丝数：{fans}",
        f"压力：{pressure}",
        f"健康：{health}",
        f"动力：{motivation}",
        f"余额：{balance}",
        f"是否签约：{signed}",
        f"是否入V：{vip}",
    ]
    return "，".join(summary_parts)


def generate_story_idea(state: Dict) -> str:
    summary = _summarize_state(state)
    prompt = (
        "你是一名熟悉晋江风格的网文编辑，根据作者当前状态，给出一个简短的一句话写作灵感，用中文回答。"
        f"\n作者状态摘要：{summary}"
    )
    try:
        return str(ask_deepseek(prompt))
    except Exception:
        return "灵感服务器有点累了，先根据你当前的剧情节奏，随便写一段你自己也会感兴趣的小场景。"


def generate_plot_conflict(state: Dict) -> str:
    summary = _summarize_state(state)
    prompt = (
        "你是网文责编，请基于作者当前进度，生成一个适合当下节奏的剧情冲突建议。"
        "冲突可以包含男女主情感矛盾、职场/家族/任务冲突、或世界观危机。"
        "请用中文输出2到4句的故事型描述。"
        f"\n作者状态摘要：{summary}"
    )
    try:
        return str(ask_deepseek(prompt))
    except Exception:
        return ""


def generate_reader_comments(state: Dict, n: int = 5) -> List[str]:
    summary = _summarize_state(state)
    prompt = (
        "这是晋江/长佩风格的读者评论区，请根据作者状态生成评论。"
        "背景是本旬刚更新完的一章。"
        "评论区需要同时包含：夸夸作者的彩虹屁、催更、吐槽剧情的小杠精、偶尔一条理性长评。"
        "请输出多行文本，每行一条评论，不要加前缀编号。"
        f"\n作者状态摘要：{summary}"
    )
    try:
        response = ask_deepseek(prompt)
        lines = [line.strip() for line in str(response).split("\n")]
        comments = [line for line in lines if line]
        return comments[:n]
    except Exception:
        return [
            "这章氛围感拉满，太会写了吧！",
            "作者大大快更新呀，孩子等不及了~",
            "这一段逻辑有点怪，我先杠一下，但还是爱看。",
        ]
