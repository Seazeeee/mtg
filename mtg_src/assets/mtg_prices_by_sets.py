import numpy as np
import duckdb
import os
import pandas as pd
from dotenv import load_dotenv
from IPython.display import display


def get_prices_set() -> int:

    SET_CODE = "mh3"
    load_dotenv()
    DB = os.getenv("DUCKDB_PATH")

    connection = duckdb.connect(DB)

    total_cards = 14

    final_total = 0

    pack_total = get_cards()

    commons = connection.sql(
        f"SELECT DISTINCT date, name, price, rarity FROM card_names_prices_finishes WHERE set LIKE '{SET_CODE}' AND rarity LIKE 'common' AND finish LIKE '%nonfoil%'"
    ).df()
    uncommons = connection.sql(
        f"SELECT DISTINCT date, name, price, rarity FROM card_names_prices_finishes WHERE set LIKE '{SET_CODE}' AND rarity LIKE 'uncommon' AND finish LIKE '%nonfoil%'"
    ).df()
    rares = connection.sql(
        f"SELECT DISTINCT date, name, price, rarity FROM card_names_prices_finishes WHERE set LIKE '{SET_CODE}' AND rarity LIKE 'rare' AND finish LIKE '%nonfoil%'"
    ).df()
    mythics = connection.sql(
        f"SELECT DISTINCT date, name, price, rarity FROM card_names_prices_finishes WHERE set LIKE '{SET_CODE}' AND rarity LIKE 'mythic' AND finish LIKE '%nonfoil%'"
    ).df()

    total_in_pack = 0

    for nums in pack_total.values():
        total_in_pack += nums

    if total_in_pack != total_cards:
        get_prices_set()

    else:
        common = commons.sample(pack_total["commons"])
        uncommon = uncommons.sample(pack_total["uncommons"])
        rare = rares.sample(pack_total["rare"])
        mythic = mythics.sample(pack_total["mythic"])

        frames = [common, uncommon, rare, mythic]

        result = pd.concat(frames)

        display(result)

        total = result["price"].sum()

        print(f"Total pack value: ${total}")

        final_total += total

    return int(final_total)


def get_cards() -> dict:

    commons = 7
    uncommons = 3

    pack_total = {"commons": commons, "uncommons": uncommons, "rare": 0, "mythic": 0}

    big_bois = ["rare", "mythic"]
    probablity = [6.4 / 7.4, 1 / 7.4]
    choice = np.random.choice(big_bois, p=probablity)

    if choice == "rare":
        pack_total["rare"] = int(pack_total["rare"]) + 1
        choice = np.random.choice(big_bois, p=probablity)
    elif choice == "mythic":
        pack_total["mythic"] = int(pack_total["mythic"]) + 1
        choice = np.random.choice(big_bois, p=probablity)

    for _ in range(0, 3):
        if choice == "rare":
            pack_total["rare"] = int(pack_total["rare"]) + 1

            choice = np.random.choice(big_bois, p=probablity)
        elif choice == "mythic":
            pack_total["mythic"] = int(pack_total["mythic"]) + 1

            choice = np.random.choice(big_bois, p=probablity)

    print("Attempted")

    return pack_total


if __name__ == "__main__":

    total_cost = 80

    total_packs = 0

    for _ in range(0, 10):

        total_packs += get_prices_set()

    if total_packs > total_cost:
        print("WE MADE IT BIG!")
    else:
        print("SCAM LIKE ALWAYS")
