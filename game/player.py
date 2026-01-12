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

    def advance_period(self, plan: str) -> None:
        period_expense = int(self.monthly_expense / 3)
        self.balance -= period_expense

        if plan == "focus_writing":
            self.stress += 3
            self.motivation += 4
            self.fans += random.randint(3, 10)
        elif plan == "part_time":
            self.balance += 800
            self.stress += 6
            self.motivation -= 5
            self.fans = max(0, self.fans - random.randint(0, 2))
        elif plan == "rest":
            self.stress = max(0, self.stress - 8)
            self.health = min(100, self.health + 5)
            self.motivation = min(100, self.motivation + 2)
        else:
            raise ValueError(f"Unknown plan: {plan}")

        if self.stress > 70:
            self.health -= 5

        self.stress = _clamp(self.stress, 0, 100)
        self.health = _clamp(self.health, 0, 100)
        self.motivation = _clamp(self.motivation, 0, 100)

        self.period += 1
        if self.period > 3:
            self.period = 1
            self.month += 1

    def summary(self) -> str:
        labels = {1: "上旬", 2: "中旬", 3: "下旬"}
        label = labels.get(self.period, "未知")
        return (
            f"Month {self.month}-{label} | Balance: {self.balance} | Stress: {self.stress} "
            f"| Health: {self.health} | Motivation: {self.motivation} | Fans: {self.fans}"
        )
