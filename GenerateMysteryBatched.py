import random

import yaml


def load_all_games(games):
    game_data = {}

    for game in games:
        with open(f"games/{game}.yaml", encoding="utf-8-sig") as game_file:
            game_settings: dict = yaml.unsafe_load(game_file)
            game_data[game] = game_settings

    return game_data



def main():
    with open("games/__meta__.yaml") as file:
        data = yaml.unsafe_load(file)

    player_header = {**data}
    del player_header["game"]

    game_data = load_all_games(data["game"].keys())
    all_games = []
    with open("games/__groups__.yaml") as file:
        groups = yaml.unsafe_load(file)

    for group_name, group in groups.items():
        game_names = list(group["games"].keys())
        weights = group["games"].values()

        selected_games = random.choices(game_names, weights, k=group["players"])

        print(f"Group {group_name} with {group['players']}")
        print(f"Output: {selected_games}")

        all_games += selected_games

    total_game_count = len(all_games)
    with open("output/batch_output.yaml", "w+") as file:
        for i, game in enumerate(all_games, 1):
            game_dict = {**player_header, **game_data[game]}
            yaml.dump(game_dict, file)

            if i == total_game_count:
                break

            file.write("\n---\n\n")

    print("Wrote yaml file to `./output/batch_output.yaml`")


if __name__ == "__main__":
    main()
