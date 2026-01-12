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

    def advance_period(self, plan: str) -> None:
        if plan == "focus_writing":
            self.words += random.randint(8000, 12000)
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
            self.words += random.randint(2000, 4000)
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

    def _end_of_month(self) -> None:
        cost = self.monthly_expense
        tips = 0
        subs = 0
        self._check_in_v()
        if self.signed:
            if self.in_v:
                subs = int(self.book_favorites * 0.6)
                tips = int(self.book_favorites * 0.08)
            else:
                tips = int(self.book_favorites * 0.2)
        income = tips + subs
        net = income - cost
        self.balance += net
        verdict = "入不敷出" if net < 0 else "略有盈余"
        in_v_status = "已入V" if self.in_v else "未入V"
        print(
            f"【月末结算】Month {self.month} | 成本: {cost} | 打赏: {tips} | "
            f"订阅: {subs} | 净变化: {net} | 当前余额: {self.balance} | "
            f"评价: {verdict} | 入V: {in_v_status}"
        )
        if self.signed and self.contract_months_left > 0:
            self.contract_months_left -= 1
            if self.contract_months_left == 0:
                print("三年合同到期了，编辑问你要不要续约（暂时自动续约）。")
