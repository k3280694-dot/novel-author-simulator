"""Main entry point for the novel author simulator."""

from game.player import Player


def main() -> None:
    """Run a short sample routine for the player."""
    print("请选择居住方案：")
    print("1) 800 元：城郊合租（更省钱但更挤压）")
    print("2) 1200 元：普通合租")
    print("3) 2000 元：小区单间（安静）")
    print("4) 3000 元：市中心精装")
    rent_choice = input("输入 1/2/3/4，回车确认：").strip()

    rent_map = {"1": "800", "2": "1200", "3": "2000", "4": "3000"}
    rent_level = rent_map.get(rent_choice, "1200")

    print("请选择伙食方案：")
    print("A) 600 元：泡面+外卖")
    print("B) 1000 元：食堂为主")
    print("C) 1600 元：正常三餐+水果")
    print("D) 2400 元：外食+奶茶")
    food_choice = input("输入 A/B/C/D，回车确认：").strip().upper()

    food_map = {"A": "600", "B": "1000", "C": "1600", "D": "2400"}
    food_level = food_map.get(food_choice, "1000")

    player = Player("Kexin", rent_level=rent_level, food_level=food_level)
    for _ in range(12):
        for plan in ("focus_writing", "focus_writing", "focus_writing"):
            player.advance_period(plan)
            print(player.summary())
            if player.new_rank_used:
                return


if __name__ == "__main__":
    main()
