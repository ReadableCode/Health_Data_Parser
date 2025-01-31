# %%
# Imports #


from pathlib import Path

import pandas as pd

from utils.display_tools import pprint_df

# %%
# Variables #

samsung_health_path = Path("../health_data/Samsung Health").resolve()
print(f"Samsung Health Path: {samsung_health_path}")
ls_date_extraction_folders = [x for x in samsung_health_path.iterdir() if x.is_dir()]
path_most_recent_date_extraction = max(ls_date_extraction_folders)


print(f"Most Recent Date Extraction: {path_most_recent_date_extraction}")

ls_files_in_dir = [x for x in path_most_recent_date_extraction.iterdir() if x.is_file()]


# %%
# Functions #


def parse_offset(offset_str):
    """Convert UTC offset string (e.g., 'UTC-0600') to a pandas Timedelta"""
    if (
        pd.isna(offset_str)
        or not isinstance(offset_str, str)
        or not offset_str.startswith("UTC")
    ):
        return pd.Timedelta(0)  # Default to no offset if missing or invalid

    sign = -1 if "-" in offset_str else 1
    hours = int(offset_str[4:6])  # Extract HH part
    minutes = int(offset_str[6:8]) if len(offset_str) > 6 else 0  # Extract MM part

    return pd.Timedelta(hours=sign * hours, minutes=sign * minutes)


def get_df_from_csv(path_file):
    df_step_count = pd.read_csv(path_file, skiprows=1, index_col=False)
    return df_step_count


# %%
# Step Daily Trend #


def get_step_daily_trend():
    ls_files_in_dir = [
        x for x in path_most_recent_date_extraction.iterdir() if x.is_file()
    ]

    path_step_count_file = [
        x for x in ls_files_in_dir if "com.samsung.shealth.step_daily_trend." in x.name
    ][0]
    print(path_step_count_file)

    df_step_daily_trend = get_df_from_csv(path_step_count_file)

    df_step_daily_trend = df_step_daily_trend[df_step_daily_trend["source_type"] == -2]

    df_step_daily_trend["create_time"] = pd.to_datetime(
        df_step_daily_trend["create_time"]
    )

    df_step_daily_trend["date"] = df_step_daily_trend["create_time"].dt.date

    columns = [
        "date",
        "count",
        "speed",
        "distance",
        "calorie",
        # "binning_data",
        # "update_time",
        # "create_time",
        # "source_pkg_name",
        # "source_type",
        # "deviceuuid",
        # "pkg_name",
        # "datauuid",
        # "day_time",
    ]

    df_step_daily_trend = df_step_daily_trend[columns]

    return df_step_daily_trend


# %%
# Main #

if __name__ == "__main__":
    df_step_daily_trend_filtered = get_step_daily_trend()

    pprint_df(df_step_daily_trend_filtered.tail(50))
    print(df_step_daily_trend_filtered.columns.tolist())


# %%
