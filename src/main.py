# %%
# Imports #


import matplotlib.pyplot as plt
import pandas as pd

from samsung_health import get_step_daily_trend
from utils.display_tools import pprint_df

# %%
# Variables #


# %%
# Functions #


def show_graph(df, columns, date_col_name = "date"):
    df[date_col_name] = pd.to_datetime(df[date_col_name])
    df.set_index(date_col_name, inplace=True)
    df[columns].plot()
    plt.show()


def get_steps():
    df_step_daily_trend = get_step_daily_trend()

    pprint_df(df_step_daily_trend)
    # print value counts of dates
    print(sorted(df_step_daily_trend["date"].unique().tolist()))

    return df_step_daily_trend

df_step_daily_trend = get_steps()

show_graph(df_step_daily_trend, ["count"])


# %%
# Display #


# %%
