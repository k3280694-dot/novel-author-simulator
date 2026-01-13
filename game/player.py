"""Player model for author stats and state."""

from __future__ import annotations

from dataclasses import dataclass
import random


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(value, maximum))


@dataclass
class Player:
    name: str
    month: int = 1
    period: int = 1
    balance: int = 20000
    monthly_expense: int = 4000
    stress: int = 20
    health: int = 100
    motivation: int = 70
    fans: int = 0
    words: int = 0
    signed: bool = False  # 作者是否已签约
    contract_months_left: int = 0  # 合同剩余月份，未签约为 0
    book_favorites: int = 0
    in_v: bool = False
    words_this_month: int = 0  # 本月新增写作字数
    new_book_chart_used: bool = False  # 新书千字榜是否已经触发
    monthly_royalty: int = 0  # 当月稿费
    monthly_tips: int = 0  # 当月打赏

    def advance_period(self, plan: str) -> None:
        if plan == "focus_writing":
            words_gained = random.randint(8000, 12000)
            self.words += words_gained
            self.words_this_month += words_gained
            self.stress += 8
            self.health -= 4
            self.motivation += 3
            self.fans += random.randint(3, 10)
            self.book_favorites += random.randint(20, 60)
        elif plan == "rest":
            self.stress = max(0, self.stress - 8)
            self.health = min(100, self.health + 5)
            self.motivation = min(100, self.motivation + 2)
        else:
            words_gained = random.randint(2000, 4000)
            self.words += words_gained
            self.words_this_month += words_gained
            self.balance += 1500
            self.stress += 2
            self.motivation -= 1

        if self.stress > 70:
            self.health -= 5

        self.stress = _clamp(self.stress, 0, 100)
        self.health = _clamp(self.health, 0, 100)
        self.motivation = _clamp(self.motivation, 0, 100)

        self._check_sign_contract()
        self.period += 1
        if self.period > 3:
            self.period = 1
            self._end_of_month()
            self.month += 1

    def summary(self) -> str:
        labels = {1: "上旬", 2: "中旬", 3: "下旬"}
        label = labels.get(self.period, "未知")
        if self.signed:
            sign_status = f"已签约，合同剩余 {self.contract_months_left} 个月"
        else:
            sign_status = "未签约"
        return (
            f"Month {self.month}-{label} | 签约状态: {sign_status} | Words: {self.words} "
            f"| Balance: {self.balance} | Stress: {self.stress} | Health: {self.health} "
            f"| Motivation: {self.motivation} | Fans: {self.fans}"
        )

    def _check_sign_contract(self) -> None:
        if self.signed:
            return
        if (
            self.words >= 10_000
            and self.health >= 50
            and self.stress <= 80
            and self.motivation >= 60
        ):
            self.signed = True
            self.contract_months_left = 36
            print("【编辑来信】题材不错，文笔有潜力，我们来签一个三年约吧。")

    def _check_in_v(self) -> None:
        if self.in_v:
            return
        if self.signed and self.words >= 60000 and self.book_favorites >= 300:
            self.in_v = True
            print("【编辑来信】你的小说表现不错，已通过审核，本书正式入V！")

    def _new_book_chart_boost(self) -> None:
        roll = random.random()
        if roll < 0.3:
            rank = 1
            fav_gain = random.randint(8000, 12000)
        elif roll < 0.6:
            rank = random.randint(2, 3)
            fav_gain = random.randint(6000, 10000)
        elif roll < 0.9:
            rank = random.randint(4, 10)
            fav_gain = random.randint(3000, 6000)
        else:
            rank = random.randint(11, 30)
            fav_gain = random.randint(800, 2000)
        self.book_favorites += fav_gain
        new_fans = int(fav_gain * random.uniform(0.03, 0.07))
        self.fans += new_fans
        print(
            "【新书千字榜】本书今日登上千字推荐榜，第 "
            f"{rank} 名。新增收藏 {fav_gain}，当日涨粉 {new_fans}。"
        )

    def _end_of_month(self) -> None:
        cost = self.monthly_expense
        self.monthly_royalty = 0
        self.monthly_tips = 0
        self._check_in_v()
        if self.in_v and not self.new_book_chart_used:
            self._new_book_chart_boost()
            self.new_book_chart_used = True
        if not self.signed:
            status_note = "当前未签约，暂无收入"
        elif not self.in_v:
            self.monthly_tips = random.randint(0, self.fans * 50)
            status_note = "已签约，仍在免费期，只有打赏收入"
        else:
            self.monthly_tips = random.randint(0, self.fans * 50)
            approx_subs = min(
                int(self.book_favorites * 1.5),
                int(self.fans * 2.5),
            )
            unit_royalty = random.uniform(0.22, 0.28)
            thousands = self.words_this_month / 1000
            self.monthly_royalty = int(thousands * approx_subs * unit_royalty)
            status_note = "已签约且入 V，有稿费和打赏收入"
        net = self.monthly_royalty + self.monthly_tips - cost
        self.balance += net
        verdict = "入不敷出" if net < 0 else "略有盈余"
        in_v_status = "已入 v" if self.in_v else "未入 v"
        new_fans = int(self.book_favorites * 0.03)
        new_fans = min(200, new_fans)
        self.fans += new_fans
        print(
            f"【月末结算】Month {self.month} | 成本: {cost} 元 | "
            f"稿费: {self.monthly_royalty} 元 | 打赏: {self.monthly_tips} 元 | "
            f"净变化: {net} 元 | 当前余额: {self.balance} 元 | "
            f"评价: {verdict} | 入 v：{in_v_status} | {status_note}"
        )
        print(f"【粉丝】本月新增: {new_fans} 个，总粉丝: {self.fans} 个")
        self.words_this_month = 0
        if self.signed and self.contract_months_left > 0:
            self.contract_months_left -= 1
            if self.contract_months_left == 0:
                print("三年合同到期了，编辑问你要不要续约（暂时自动续约）。")
