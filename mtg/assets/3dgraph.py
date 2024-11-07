import duckdb
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from IPython.display import display

if __name__ == "__main__":
    # Get DB
    load_dotenv()
    DB = os.getenv("DUCKDB_PATH")

    connection = duckdb.connect(DB)

    card_name = "Slime Against Humanity"

    # Fetch data from DuckDB
    df = connection.sql(
        f"SELECT * FROM avg_price_of_cards WHERE Name LIKE '%{card_name}%'"
    ).df()

    # Creation of Figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(121, projection="3d")

    # Describing desired colors per card finish
    colors = {
        "foil": (255 / 255, 0, 0),
        "nonfoil": (0, 0, 255 / 255),
        "etched": (93 / 255, 63 / 255, 211 / 255),
    }

    # Get unique dates and finishes
    x_dates = df["date"].unique()
    x = np.arange(len(x_dates))

    # Grab unique finishes
    unique_finishes = df["finish"].unique()

    # Grab the finishes that are present in unique_finishes
    desired_order = [
        finish for finish in ["nonfoil", "etched", "foil"] if finish in unique_finishes
    ]
    df["finish"] = pd.Categorical(df["finish"], categories=desired_order, ordered=True)
    df["finish_code"] = df["finish"].cat.codes

    # Set heights of the bars based on average prices for each finish
    z = df.groupby(["date", "finish"])["avg"].mean().unstack(fill_value=0)

    # Enumerating on desired_ordered.
    # i is the y-value associated with the finish
    # We will then plot the date(x), then z(z[finish].values) which is are price.
    # zs = i is setting the y values to i.
    # zdir is telling it to plot zs on the y-axis
    for i, finish in enumerate(desired_order):

        ax.plot(x, z[finish].values, zs=i, zdir="y", alpha=0.7, color=colors[finish])

    # Set x-tick labels to dates
    ax.set_xticks(x)
    ax.set_xticklabels(x_dates.strftime("%Y-%m-%d"), rotation=45, ha="right")

    # Set y-tick labels to finish labels
    ax.set_yticks(np.arange(len(desired_order)))
    ax.set_yticklabels(desired_order)

    plt.show()
