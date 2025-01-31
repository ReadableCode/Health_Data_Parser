# %%
# Imports #


from datetime import date  # noqa: F401
from pathlib import Path

import pandas as pd

from utils.display_tools import pprint_df, pprint_dict, pprint_ls  # noqa: F401

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
    file_name_part = "com.samsung.shealth.step_daily_trend."
    ls_files_in_dir = [
        x for x in path_most_recent_date_extraction.iterdir() if x.is_file()
    ]

    path_step_count_file = [x for x in ls_files_in_dir if file_name_part in x.name][0]

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
# Pedometer #


def get_daily_ped(include_offset=True):
    file_name_part = "com.samsung.shealth.tracker.pedometer_day_summary."
    ls_files_in_dir = [
        x for x in path_most_recent_date_extraction.iterdir() if x.is_file()
    ]

    path_pedometer_file = [x for x in ls_files_in_dir if file_name_part in x.name][0]

    df_pedometer_data = get_df_from_csv(path_pedometer_file)

    df_pedometer_data = df_pedometer_data.dropna(subset=["source_info"])

    df_pedometer_data["create_time"] = pd.to_datetime(df_pedometer_data["create_time"])

    # Apply offset conversion
    df_pedometer_data["time_offset_timedelta"] = parse_offset("UTC-0600")

    if include_offset:
        # Apply the offset to create_time
        df_pedometer_data["create_time"] += df_pedometer_data["time_offset_timedelta"]

    df_pedometer_data["date"] = df_pedometer_data["create_time"].dt.date

    print("df_pedometer_data filters")
    pprint_df(
        df_pedometer_data[df_pedometer_data["date"].isin(ls_test_dates)].tail(100)
    )

    # ✅ Ensure sorting before `idxmax()` (Sort by date and create_time in ascending order)
    df_pedometer_data = df_pedometer_data.sort_values(["date", "create_time"])

    # ✅ Keep only the row with the **latest create_time** per date
    df_pedometer_data = df_pedometer_data.loc[
        df_pedometer_data.groupby("date")["create_time"].idxmax()
    ].reset_index(drop=True)

    columns = [
        "date",
        # "create_sh_ver",
        "step_count",
        # "binning_data",
        "active_time",
        # "recommendation",
        # "modify_sh_ver",
        "run_step_count",
        # "update_time",
        # "source_package_name",
        # "create_time",
        # "source_info",
        # "speed",
        "distance",
        "calorie",
        "walk_step_count",
        # "deviceuuid",
        # "pkg_name",
        # "healthy_step",
        # "achievement",
        # "datauuid",
        # "day_time",
    ]

    df_pedometer_data = df_pedometer_data[columns]

    return df_pedometer_data


# %%
# Main #

if __name__ == "__main__":
    ls_test_dates = [
        # date(2018, 6, 17),
        # date(2019, 3, 24),
        # date(2021, 11, 21),
        date(2023, 1, 3),
        # date(2023, 1, 4),
        # date(2023, 1, 2),
        # date(2023, 1, 5),
    ]

    df_step_daily_trend = get_step_daily_trend()

    print("df_step_daily_trend")
    pprint_df(df_step_daily_trend.tail(10))

    include_offset = True
    df_pedometer_data = get_daily_ped(include_offset=include_offset)

    print("df_pedometer_data")
    pprint_df(df_pedometer_data.tail(10))

    print("df_step_daily_trend filters")
    pprint_df(
        df_step_daily_trend[df_step_daily_trend["date"].isin(ls_test_dates)].tail(100)
    )
    print("df_pedometer_data filters")
    pprint_df(
        df_pedometer_data[df_pedometer_data["date"].isin(ls_test_dates)].tail(100)
    )

# 1/3/2023 should be 177

# %%
