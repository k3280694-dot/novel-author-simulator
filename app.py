"""Streamlit UI for the novel author simulator."""

from __future__ import annotations

import streamlit as st

from game.game import Game


def _period_label(period: int) -> str:
    return {1: "上旬", 2: "中旬", 3: "下旬"}.get(period, "未知")


def _ensure_game() -> Game:
    if "game" not in st.session_state:
        st.session_state.game = Game("Kexin")
    return st.session_state.game


def main() -> None:
    st.set_page_config(page_title="Novel Author Simulator", layout="wide")

    st.sidebar.header("控制台")
    if st.sidebar.button("重新开始一局"):
        st.session_state.game = Game("Kexin")
        st.rerun()

    game = _ensure_game()
    state = game.get_state()

    if state.get("just_signed"):
        st.success("📩 编辑来信：题材不错，文笔有潜力，我们来签一个三年约吧。")

    if state.get("just_in_v"):
        st.success("🎉 恭喜本书正式入 V！今天你拿到了新书千字榜的机会。")

    if state.get("just_burnout"):
        st.error("⚠️ 这几旬把自己彻底熬垮了，去医院检查花了 1000 元，下旬开始最好多安排休息或花钱解压。")

    if state["month"] == 1 and state["period"] == 1:
        st.subheader("🏠 选择起步生活方式")
        rent_label = st.radio(
            "房租档位",
            [
                "800：城郊合租（更省钱但更挤压）",
                "1200：普通合租",
                "2000：小区单间（安静）",
                "3000：市中心精装",
            ],
            index=1,
        )
        food_label = st.radio(
            "伙食档位",
            [
                "600：泡面+外卖",
                "1000：食堂为主",
                "1600：正常三餐+水果",
                "2400：外食+奶茶",
            ],
            index=1,
        )
        if st.button("确认生活成本设置"):
            rent_level = rent_label.split("：")[0]
            food_level = food_label.split("：")[0]
            game.set_lifestyle(rent_level, food_level)
            st.rerun()

    st.header("📖 小说作者模拟器")
    period_label = _period_label(state["period"])
    st.write(f"当前进度：第 {state['month']} 月 {period_label}")

    info_cols = st.columns(5)
    info_cols[0].metric("总字数", f"{state['words']:,}")
    info_cols[1].metric("收藏", f"{state['book_favorites']:,}")
    info_cols[2].metric("粉丝", f"{state['fans']:,}")
    info_cols[3].metric("余额", f"{state['balance']:,} 元")
    info_cols[4].metric("上旬新增字数", f"{state['last_period_words']:,}")

    status_cols = st.columns(5)
    status_cols[0].metric("压力", f"{state['stress']}/100")
    status_cols[1].metric("健康", f"{state['health']}/100")
    status_cols[2].metric("动力", f"{state['motivation']}/100")
    status_cols[3].metric("签约状态", "已签约" if state["signed"] else "未签约")
    status_cols[4].metric("入 V", "已入 V" if state["in_v"] else "未入 V")

    st.subheader("💰 生活成本")
    st.write(
        f"房租 {state['rent_cost']} 元 | 伙食 {state['food_cost']} 元 | "
        f"其他 {state['other_cost']} 元 | 月支出 {state['monthly_expense']} 元"
    )

    with st.expander("🛒 本旬用钱回血 / 解压（可选）", expanded=False):
        st.write("用赚来的稿费改善生活吧～")
        col_a, col_b, col_c, col_d = st.columns(4)

        if col_a.button("看电影（80 元）"):
            game.apply_activity("movie")
            st.rerun()
        if col_b.button("按摩（200 元）"):
            game.apply_activity("massage")
            st.rerun()
        if col_c.button("KTV（300 元）"):
            game.apply_activity("ktv")
            st.rerun()
        if col_d.button("健身（150 元）"):
            game.apply_activity("gym")
            st.rerun()

    st.subheader("🗓️ 选择本旬安排")
    plan_label = st.radio(
        "计划",
        [
            "专注写作（字数高，压力增加）",
            "兼职写作（字数一般，赚点外快）",
            "休息调整（恢复健康和动力）",
            "摸鱼摆烂（字数少，可能更轻松）",
        ],
    )
    plan_map = {
        "专注写作（字数高，压力增加）": "focus_writing",
        "兼职写作（字数一般，赚点外快）": "part_time",
        "休息调整（恢复健康和动力）": "rest",
        "摸鱼摆烂（字数少，可能更轻松）": "slack",
    }
    if st.button("推进到下一旬"):
        game.step(plan_map[plan_label])
        st.rerun()


if __name__ == "__main__":
    main()
