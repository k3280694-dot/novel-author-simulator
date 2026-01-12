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
    signed: bool = False

    def advance_period(self, plan: str) -> None:
        if plan == "focus_writing":
            self.words += random.randint(8000, 12000)
            self.stress += 8
            self.health -= 4
            self.motivation += 3
            self.fans += random.randint(3, 10)
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

        self._check_sign_status()
        self.period += 1
        if self.period > 3:
            self.period = 1
            self._end_of_month()
            self.month += 1

    def summary(self) -> str:
        labels = {1: "上旬", 2: "中旬", 3: "下旬"}
        label = labels.get(self.period, "未知")
        sign_status = "已签约" if self.signed else "未签约"
        return (
            f"Month {self.month}-{label} | 身份: {sign_status} | Words: {self.words} "
            f"| Balance: {self.balance} | Stress: {self.stress} | Health: {self.health} "
            f"| Motivation: {self.motivation} | Fans: {self.fans}"
        )

    def _check_sign_status(self) -> None:
        if self.signed:
            return
        if self.words >= 50_000 and self.fans >= 300:
            self.signed = True
            print(
                f"【系统提示】你的小说达到 {self.words} 字、收藏 {self.fans}，编辑发来私信："
                "恭喜签约入V，之后章节开始有收入了！"
            )

    def _end_of_month(self) -> None:
        cost = self.monthly_expense
        royalty = self.fans * 15 if self.signed else 0
        net = royalty - cost
        self.balance += net
        verdict = "入不敷出" if net < 0 else "略有盈余"
        print(
            f"【月末结算】Month {self.month} | 成本: {cost} | 稿费: {royalty} | "
            f"净变化: {net} | 当前余额: {self.balance} | 评价: {verdict}"
        )
