"""Player model for author stats and state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar
import random


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(value, maximum))


@dataclass
class Player:
    SHOP_ACTIVITIES: ClassVar[dict[str, dict[str, int | str]]] = {
        "movie": {
            "label": "看电影",
            "cost": 80,
            "stress": -10,
            "health": 5,
            "motivation": 5,
        },
        "massage": {
            "label": "按摩",
            "cost": 200,
            "stress": -25,
            "health": 15,
            "motivation": 10,
        },
        "ktv": {
            "label": "KTV 唱歌",
            "cost": 300,
            "stress": -20,
            "health": 5,
            "motivation": 15,
        },
        "gym": {
            "label": "健身房出汗",
            "cost": 150,
            "stress": -15,
            "health": 10,
            "motivation": 10,
        },
    }
    name: str
    month: int = 1
    period: int = 1
    balance: int = 20000
    rent_level: str = "1200"
    food_level: str = "1000"
    rent_cost: int = 1200
    food_cost: int = 1000
    other_cost: int = 500
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
    last_period_words: int = 0  # 上一旬写了多少字
    update_tier: str = "normal"  # 当前更新档位："low" / "normal" / "high" / "overwork"
    words_this_month: int = 0  # 本月新增写作字数
    favorites_delta_this_month: int = 0
    fans_delta_this_month: int = 0
    new_rank_used: bool = False  # 新书千字榜是否已经触发
    monthly_royalty: int = 0  # 当月稿费
    monthly_tips: int = 0  # 当月打赏
    just_burnout: bool = False
    just_signed: bool = False
    just_in_v: bool = False

    def _update_lifestyle(self) -> tuple[int, int, int]:
        """Update lifestyle costs and return monthly status deltas."""
        if self.rent_level == "800":
            self.rent_cost = 800
            rent_stress = 6
            rent_health = -1
            rent_motivation = -1
        elif self.rent_level == "1200":
            self.rent_cost = 1200
            rent_stress = 0
            rent_health = 0
            rent_motivation = 0
        elif self.rent_level == "2000":
            self.rent_cost = 2000
            rent_stress = -3
            rent_health = 0
            rent_motivation = 2
        elif self.rent_level == "3000":
            self.rent_cost = 3000
            rent_stress = -4
            rent_health = 0
            rent_motivation = 3
        else:
            self.rent_cost = 1200
            rent_stress = 0
            rent_health = 0
            rent_motivation = 0

        if self.food_level == "600":
            self.food_cost = 600
            food_stress = 2
            food_health = -4
            food_motivation = 0
        elif self.food_level == "1000":
            self.food_cost = 1000
            food_stress = 0
            food_health = 0
            food_motivation = 0
        elif self.food_level == "1600":
            self.food_cost = 1600
            food_stress = 0
            food_health = 3
            food_motivation = 0
        elif self.food_level == "2400":
            self.food_cost = 2400
            food_stress = -1
            food_health = -1
            food_motivation = 2
        else:
            self.food_cost = 1000
            food_stress = 0
            food_health = 0
            food_motivation = 0

        self.monthly_expense = self.rent_cost + self.food_cost + self.other_cost

        stress_delta = rent_stress + food_stress
        health_delta = rent_health + food_health
        motivation_delta = rent_motivation + food_motivation
        return stress_delta, health_delta, motivation_delta

    def do_activity(self, activity: str) -> None:
        """花钱进行一次休闲活动，用于减压 / 回血 / 恢复创作动力。"""
        cfg = self.SHOP_ACTIVITIES.get(activity)
        if not cfg:
            return
        if self.balance < cfg["cost"]:
            return

        self.balance -= cfg["cost"]
        self.stress = _clamp(self.stress + int(cfg["stress"]), 0, 100)
        self.health = _clamp(self.health + int(cfg["health"]), 0, 100)
        self.motivation = _clamp(self.motivation + int(cfg["motivation"]), 0, 100)

    def advance_period(self, plan: str) -> None:
        before = self.words
        if plan == "focus_writing":
            words_gained = random.randint(8000, 12000)
            self.words += words_gained
            self.words_this_month += words_gained
            self.stress += 8
            self.health -= 4
            self.motivation += 3
            fans_gained = random.randint(3, 10)
            favorites_gained = random.randint(20, 60)
            self.fans += fans_gained
            self.book_favorites += favorites_gained
            self.fans_delta_this_month += fans_gained
            self.favorites_delta_this_month += favorites_gained
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

        self.last_period_words = self.words - before
        if self.stress > 70:
            self.health -= 5

        self.stress = _clamp(self.stress, 0, 100)
        self.health = _clamp(self.health, 0, 100)
        self.motivation = _clamp(self.motivation, 0, 100)

        self._check_sign_contract()
        self.period += 1
        if self.period > 3:
            self.period = 1
            self._update_update_tier()
            self._end_of_month()
            self.month += 1

        self.stress = _clamp(self.stress, 0, 100)
        self.health = _clamp(self.health, 0, 100)

        self.just_burnout = False
        if self.stress >= 100 or self.health <= 0:
            self.just_burnout = True
            self.balance = max(0, self.balance - 1000)
            self.motivation = max(0, self.motivation - 15)

    def summary(self) -> str:
        labels = {1: "上旬", 2: "中旬", 3: "下旬"}
        label = labels.get(self.period, "未知")
        if self.signed:
            sign_status = f"已签约，合同剩余 {self.contract_months_left} 个月"
        else:
            sign_status = "未签约"
        tier_label = {
            "low": "低强度",
            "normal": "常规",
            "high": "高强度",
            "overwork": "过载",
        }.get(self.update_tier, "常规")
        return (
            f"Month {self.month}-{label} | 签约状态: {sign_status} | Words: {self.words} "
            f"| Balance: {self.balance} | Stress: {self.stress} | Health: {self.health} "
            f"| Motivation: {self.motivation} | Fans: {self.fans} | 更新档位: {tier_label}"
        )

    def is_book_finished(self) -> bool:
        return self.words >= 300_000 and self.health > 0

    def is_game_over(self) -> tuple[bool, str]:
        if self.is_book_finished():
            return True, "finished"
        return False, ""

    def _check_sign_contract(self) -> None:
        self.just_signed = False
        if self.signed:
            return
        if (
            self.words >= 10_000
            and self.health >= 50
            and self.stress <= 80
            and self.motivation >= 60
        ):
            self.signed = True
            self.just_signed = True
            self.contract_months_left = 36
            print("【编辑来信】题材不错，文笔有潜力，我们来签一个三年约吧。")

    def _check_in_v(self) -> None:
        self.just_in_v = False
        if self.in_v:
            return
        if self.signed and self.words >= 60000 and self.book_favorites >= 300:
            self.in_v = True
            self.just_in_v = True
            print("【编辑来信】你的小说表现不错，已通过审核，本书正式入V！")

    def _update_update_tier(self) -> None:
        total_words_this_month = self.words_this_month
        if total_words_this_month < 30000:
            self.update_tier = "low"
        elif total_words_this_month < 60000:
            self.update_tier = "normal"
        elif total_words_this_month < 90000:
            self.update_tier = "high"
        else:
            self.update_tier = "overwork"

    def _apply_new_book_rank_boost(self) -> None:
        base = max(1, 30 - self.book_favorites // 300)
        upper = min(base + 10, 30)
        rank = random.randint(base, upper)
        if 1 <= rank <= 3:
            gain = random.randint(5000, 10000)
        elif 4 <= rank <= 10:
            gain = random.randint(2000, 6000)
        elif 11 <= rank <= 20:
            gain = random.randint(800, 2000)
        else:
            gain = random.randint(200, 600)
        self.book_favorites += gain
        self.favorites_delta_this_month += gain
        fans_gained = gain // 50
        self.fans += fans_gained
        self.fans_delta_this_month += fans_gained
        print(
            "【新书千字榜】今天榜单排名第 "
            f"{rank} 名，新增收藏 {gain} 个，当前收藏 {self.book_favorites} 个。"
        )

    def _calc_tips(self) -> int:
        if not self.signed:
            return 0
        if not self.in_v:
            probability = 0.05 + min(self.book_favorites, 1000) / 1000 * 0.10
            if random.random() > probability:
                return 0
            return random.choices([2, 5, 10, 20], weights=[4, 4, 1, 1], k=1)[0]
        scale = max(self.book_favorites, self.fans * 2)
        probability = 0.2 + min(scale, 10000) / 10000 * 0.6
        if random.random() > probability:
            return 0
        base = scale / 100
        amount = int(random.gauss(base, max(1, base / 3)))
        return max(0, min(1000, amount))

    def _end_of_month(self) -> None:
        stress_delta, health_delta, motivation_delta = self._update_lifestyle()
        self.stress += stress_delta
        self.health += health_delta
        self.motivation += motivation_delta
        cost = self.monthly_expense
        self.monthly_royalty = 0
        self.monthly_tips = 0
        self._check_in_v()
        if self.in_v and not self.new_rank_used:
            self._apply_new_book_rank_boost()
            self.new_rank_used = True
        if not self.signed:
            status_note = "当前未签约，暂无收入"
        elif not self.in_v:
            self.monthly_tips = self._calc_tips()
            status_note = "已签约，仍在免费期，只有打赏收入"
        else:
            self.monthly_tips = self._calc_tips()
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
        self.fans_delta_this_month += new_fans
        multiplier = 1.0
        update_note = "本月更新节奏稳定，读者反馈正常。"
        if self.update_tier == "low":
            multiplier = 0.7
            update_note = "更新节奏有点不稳，读者有点着急。"
        elif self.update_tier == "high":
            multiplier = 1.2
            self.stress += 5
            update_note = "更新很给力，读者好感度提升。"
        elif self.update_tier == "overwork":
            multiplier = 1.1
            self.stress += 10
            self.health -= 5
            update_note = "更新过于猛，读者热情高涨，但身体开始透支。"

        print(f"【读者反馈】{update_note}")

        if self.favorites_delta_this_month or self.fans_delta_this_month:
            self.book_favorites -= self.favorites_delta_this_month
            self.fans -= self.fans_delta_this_month
            adjusted_favorites = int(
                round(self.favorites_delta_this_month * multiplier)
            )
            adjusted_fans = int(round(self.fans_delta_this_month * multiplier))
            self.book_favorites += adjusted_favorites
            self.fans += adjusted_fans

        self.favorites_delta_this_month = 0
        self.fans_delta_this_month = 0
        print(
            f"【月末结算】Month {self.month} | 成本: {cost} 元（房租 {self.rent_cost} + "
            f"伙食 {self.food_cost} + 其他 {self.other_cost}） | "
            f"稿费: {self.monthly_royalty} 元 | 打赏: {self.monthly_tips} 元 | "
            f"净变化: {net} 元 | 当前余额: {self.balance} 元 | "
            f"评价: {verdict} | 入 v：{in_v_status} | {status_note}"
        )
        tier_label = {
            "low": "低强度更新",
            "normal": "常规更新",
            "high": "高强度更新",
            "overwork": "过载更新",
        }.get(self.update_tier, "常规更新")
        print(f"【更新档位】本月属于{tier_label}")
        print(f"【粉丝】本月新增: {new_fans} 个，总粉丝: {self.fans} 个")
        self.words_this_month = 0
        if self.signed and self.contract_months_left > 0:
            self.contract_months_left -= 1
            if self.contract_months_left == 0:
                print("三年合同到期了，编辑问你要不要续约（暂时自动续约）。")
