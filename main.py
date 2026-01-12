"""Main entry point for the novel author simulator."""

from game.player import Player


def main() -> None:
    """Run a short sample routine for the player."""
    player = Player("Kexin")
    for plan in ("focus_writing", "focus_writing", "rest"):
        player.advance_period(plan)
        print(player.summary())


if __name__ == "__main__":
    main()
