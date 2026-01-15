"""Game wrapper for player state used by the UI."""

from __future__ import annotations

from typing import Any

from game.player import Player


class Game:
    """Thin wrapper around Player for UI interactions."""

    def __init__(self, name: str) -> None:
        self.player = Player(name)

    def _get(self, name: str, default: Any = None) -> Any:
        return getattr(self.player, name, default)

    def get_state(self) -> dict[str, Any]:
        state = {
            "month": self._get("month", 1),
            "period": self._get("period", 1),
            "balance": self._get("balance", 0),
            "words": self._get("words", 0),
            "stress": self._get("stress", 0),
            "health": self._get("health", 0),
            "motivation": self._get("motivation", 0),
            "fans": self._get("fans", 0),
            "book_favorites": self._get("book_favorites", 0),
            "signed": self._get("signed", False),
            "contract_months_left": self._get("contract_months_left", 0),
            "in_v": self._get("in_v", False),
            "rent_level": self._get("rent_level", "1200"),
            "food_level": self._get("food_level", "1000"),
            "rent_cost": self._get("rent_cost", 1200),
            "food_cost": self._get("food_cost", 1000),
            "other_cost": self._get("other_cost", 500),
            "monthly_expense": self._get("monthly_expense", 0),
            "last_period_words": self._get("last_period_words", 0),
            "update_tier": self._get("update_tier", "normal"),
            "words_this_month": self._get("words_this_month", 0),
            "monthly_royalty": self._get("monthly_royalty", 0),
            "monthly_tips": self._get("monthly_tips", 0),
            "just_signed": self._get("just_signed", False),
            "just_in_v": self._get("just_in_v", False),
            "just_burnout": self._get("just_burnout", False),
            "just_moved": self._get("just_moved", False),
        }
        self.player.just_moved = False
        return state

    def step(self, plan: str) -> dict[str, Any]:
        self.player.advance_period(plan)
        return self.get_state()

    def apply_activity(self, activity: str) -> dict[str, Any]:
        """对当前玩家应用一次花钱解压活动，并返回最新状态。"""
        self.player.do_activity(activity)
        return self.get_state()

    def set_lifestyle(self, rent_level: str, food_level: str) -> dict[str, Any]:
        """更新玩家的房租与伙食档位，并刷新生活成本。"""
        old_rent_level = self.player.rent_level
        self.player.rent_level = rent_level
        self.player.food_level = food_level
        self.player._update_lifestyle()
        if rent_level != old_rent_level:
            moving_cost = int(rent_level)
            self.player.balance -= moving_cost
            self.player.stress = min(100, self.player.stress + 5)
            self.player.motivation = max(0, self.player.motivation - 3)
            self.player.just_moved = True
        return self.get_state()
