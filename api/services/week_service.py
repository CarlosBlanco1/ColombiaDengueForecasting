import pandas as pd
import cdsapi


def compute_date_range(date: pd.Timestamp):
    nearest_past_saturday = date - pd.Timedelta((date.day_of_week + 2) % 7, unit="D")
    first_week_sunday = nearest_past_saturday - pd.Timedelta(55, unit="D")
    return (first_week_sunday, nearest_past_saturday)


def fetch_2m_temp_precip_date_range(start: pd.Timestamp, end: pd.Timestamp):

    months = pd.date_range(
        start=start.to_period("M").to_timestamp(), end=end, freq="MS"
    ).month.to_list()

    months_formatted = list(map(lambda x: str(x).zfill(2), months))

    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": ["2m_temperature", "total_precipitation"],
        "year": list(set([start.year, end.year])),
        "month": months_formatted,
        "day": [
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
        ],
        "time": [
            "00:00",
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
        ],
        "data_format": "grib",
        "download_format": "unarchived",
        "area": [14, -83, -5, -66],
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download(
        "./data/climate_data_store/era5_2016-01.grib"
    )
