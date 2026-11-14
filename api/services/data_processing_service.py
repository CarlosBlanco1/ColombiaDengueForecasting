import xarray as xr
import pandas as pd
import numpy as np


def process_data_generate_df(
    start_date: pd.Timestamp, end_date: pd.Timestamp
) -> pd.DataFrame:

    dataset = xr.open_dataset(
        "./data/era5_2016-01.grib", engine="cfgrib", chunks={"time": 24}
    )

    points_with_indeces = pd.read_parquet(
        "./data/points_with_departments/point_indeces.parquet"
    )

    lat_i = xr.DataArray(
        points_with_indeces["lat_ind"].to_numpy(dtype="int64"), dims="points"
    )

    lon_i = xr.DataArray(
        points_with_indeces["lon_ind"].to_numpy(dtype="int64"), dims="points"
    )

    twom_temp_df = pre_process_temp_ds(
        dataset["t2m"].isel(latitude=lat_i, longitude=lon_i),
        points_with_indeces,
        start_date,
        end_date,
    )
    total_precip_df = pre_process_total_precip_ds(
        dataset["tp"].isel(latitude=lat_i, longitude=lon_i),
        points_with_indeces,
        start_date,
        end_date,
    )

    recent_week_cases = pd.read_json(
        "./data/dengue_cases/dengue_cases_2026_weeks_37_44.json"
    )

    keys = ["department", "epi_year", "epi_week"]

    weekly_features = twom_temp_df.merge(
        total_precip_df,
        on=keys,
        how="inner",
        validate="one_to_one",
    )

    cases_and_features_df = weekly_features.merge(
        recent_week_cases, on=keys, how="inner", validate="one_to_one"
    )

    cases_and_features_df = cases_and_features_df[
        ["case_count", "department", "epi_week", "epi_year", "2m_temperature", "tp"]
    ]

    cases_and_features_df = cases_and_features_df.sort_values(
        ["department", "epi_year", "epi_week"]
    ).reset_index(drop=True)

    feature_and_window_size = [
        ("2m_temperature", 2),
        ("2m_temperature", 4),
        ("2m_temperature", 8),
        ("tp", 2),
        ("tp", 4),
        ("tp", 8),
        ("case_count", 2),
        ("case_count", 4),
        ("case_count", 8),
    ]

    for f, s in feature_and_window_size:
        compute_x_week_rolling_avg_for_feature_in_df(s, f, cases_and_features_df)

    grouped_by_dpt = cases_and_features_df.groupby("department")

    cases_and_features_df["target_next_week_cases"] = grouped_by_dpt[
        "case_count"
    ].shift(-1)
    cases_and_features_df["target_epi_week"] = grouped_by_dpt["epi_week"].shift(-1)
    cases_and_features_df["target_epi_year"] = grouped_by_dpt["epi_year"].shift(-1)

    required_cols = [
        "2m_temperature",
        "2m_temperature_2_week_avg",
        "2m_temperature_4_week_avg",
        "2m_temperature_8_week_avg",
        "tp",
        "tp_2_week_avg",
        "tp_4_week_avg",
        "tp_8_week_avg",
        "case_count",
        "case_count_2_week_avg",
        "case_count_4_week_avg",
        "case_count_8_week_avg",
        "department",
        "target_epi_year",
        "target_epi_week",
    ]

    model_df = (
        cases_and_features_df.dropna(subset=required_cols)
        .sort_values(["target_epi_year", "target_epi_week", "department"])
        .reset_index(drop=True)
    )

    return model_df


def epi_calendar(start, end):
    days = pd.date_range(start, end, freq="D")
    sun = days - pd.to_timedelta((days.day_of_week + 1) % 7, unit="D")
    year = (sun + pd.Timedelta(days=3)).year

    def first_sunday(y):
        jan_1 = pd.Timestamp(y, 1, 1)
        s = jan_1 - pd.to_timedelta((jan_1.day_of_week + 1) % 7, unit="D")
        return s if (s + pd.Timedelta(days=3)).year == y else s + pd.Timedelta(days=7)

    first = pd.Series({y: first_sunday(y) for y in set(year)})
    week = ((sun - first.loc[year].values).days // 7) + 1
    return pd.DataFrame({"day": days, "epi_week": week, "epi_year": year})


def pre_process_temp_ds(
    temp_dataset: xr.DataArray,
    points_with_indeces: pd.DataFrame,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> pd.DataFrame:
    temp_dataset = temp_dataset.assign_coords(
        department=("points", points_with_indeces["dpto_ccdgo"].astype(str).to_numpy())
    )

    hourly_by_department = (
        (temp_dataset - 273.15)
        .groupby("department")
        .mean("points")
        .rename("2m_temperature")
    )

    daily_by_department = hourly_by_department.resample(time="D").mean()

    daily_by_department = daily_by_department.sel(
        time=(daily_by_department.time >= start_date)
        & (daily_by_department.time <= end_date)
    )

    epi_year_week_per_day_df = (
        epi_calendar(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    ).set_index("day")

    times = daily_by_department.get_index("time")

    daily_by_department = daily_by_department.assign_coords(
        epi_week=("time", epi_year_week_per_day_df.loc[times, "epi_week"].values),
        epi_year=("time", epi_year_week_per_day_df.loc[times, "epi_year"].values),
    )

    weekly_temp_by_department = daily_by_department.groupby(
        ["epi_week", "epi_year"]
    ).mean("time")

    weekly_temp_by_department_df = (
        weekly_temp_by_department.to_dataframe().reset_index()
    )

    weekly_temp_by_department_df = weekly_temp_by_department_df[
        weekly_temp_by_department_df["2m_temperature"].notnull()
    ]

    weekly_temp_by_department_df = weekly_temp_by_department_df[
        weekly_temp_by_department_df["department"] != "11"
    ]

    weekly_temp_by_department_df = weekly_temp_by_department_df.drop(
        ["step", "number", "surface"], axis=1
    )

    return weekly_temp_by_department_df


def pre_process_total_precip_ds(
    precip_dataset: xr.DataArray,
    points_with_indeces: pd.DataFrame,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> pd.DataFrame:

    precip_dataset = precip_dataset.assign_coords(
        department=("points", points_with_indeces["dpto_ccdgo"].astype(str).to_numpy())
    )

    hourly_precipitation_by_points = (
        precip_dataset.stack(t=("time", "step"))
        .reset_index("t", drop=True)
        .swap_dims(t="valid_time")
        .sortby("valid_time")
    )

    daily_precipitation_by_department = hourly_precipitation_by_points.resample(
        valid_time="1D"
    ).sum()

    daily_precipitation_by_department = daily_precipitation_by_department.reset_index(
        "points"
    )

    cell_weights = np.cos(np.deg2rad(daily_precipitation_by_department["latitude"]))

    department_codes = np.unique(daily_precipitation_by_department["department"].values)

    weighted_department_means = []

    for code in department_codes:
        is_in_department = daily_precipitation_by_department["department"] == code

        department_cells = daily_precipitation_by_department.where(
            is_in_department, drop=True
        )
        department_weights = cell_weights.where(is_in_department, drop=True)

        weighted_department_mean = department_cells.weighted(department_weights).mean(
            dim="points"
        )

        weighted_department_mean = weighted_department_mean.expand_dims(
            department=[code]
        )

        weighted_department_means.append(weighted_department_mean)

    daily_avg_p_by_department = xr.concat(weighted_department_means, dim="department")

    daily_avg_p_by_department = daily_avg_p_by_department.sel(
        valid_time=slice(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    )

    epi_year_week_per_day_df = (
        epi_calendar(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    ).set_index("day")

    times = daily_avg_p_by_department.get_index("valid_time")

    calendar = epi_year_week_per_day_df.reindex(times)

    if calendar[["epi_year", "epi_week"]].isna().any().any():
        raise ValueError("some precipitation dates are missing ther epi labels")

    daily_avg_p_by_department = daily_avg_p_by_department.assign_coords(
        epi_week=("valid_time", epi_year_week_per_day_df.loc[times, "epi_week"].values),
        epi_year=("valid_time", epi_year_week_per_day_df.loc[times, "epi_year"].values),
    )

    weekly_avg_p_by_department = daily_avg_p_by_department.groupby(
        ["epi_year", "epi_week"]
    ).sum(dim="valid_time")

    weekly_avg_p_dpt_df = weekly_avg_p_by_department.to_dataframe().reset_index()
    weekly_avg_p_dpt_df = weekly_avg_p_dpt_df[weekly_avg_p_dpt_df["department"] != "11"]

    return weekly_avg_p_dpt_df.dropna(subset=["tp"]).copy()


def compute_x_week_rolling_avg_for_feature_in_df(window_size, rolling_feature, df):
    df[f"{rolling_feature}_{window_size}_week_avg"] = df.groupby("department")[
        rolling_feature
    ].transform(lambda x: x.rolling(window_size).mean())
