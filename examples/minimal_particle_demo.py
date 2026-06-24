from pyxel_goal_game.tools.deterministic_replay import make_sample_replay


def main() -> None:
    particles = make_sample_replay()
    print(f"sample particles: {len(particles)}")


if __name__ == "__main__":
    main()
