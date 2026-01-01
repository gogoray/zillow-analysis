import pandas as pd
from datetime import datetime

DATA_PATH = "data/sales.csv"

PRIMARY_ZIPS = [30513]
SECONDARY_ZIPS = [30560, 30522, 30540, 30541]
MARKET_ZIPS = PRIMARY_ZIPS + SECONDARY_ZIPS


def load_data(path=DATA_PATH):
    df = pd.read_csv(path)

    df["Sold date"] = pd.to_datetime(
        df["Sold date (MM/DD/YYYY)"], errors="coerce"
    )

    df["Living area"] = pd.to_numeric(df["Living area"], errors="coerce")
    df["Bedrooms"] = pd.to_numeric(df["Bedrooms"], errors="coerce")
    df["Bathrooms"] = pd.to_numeric(df["Bathrooms"], errors="coerce")
    df["Lot acres"] = pd.to_numeric(df["Lot/land area"], errors="coerce")

    df["$/sf"] = df["Property price (USD)"] / df["Living area"]
    df["$/acre"] = df["Property price (USD)"] / df["Lot acres"]

    return df


def filter_improved(
    df,
    min_sf=1200,
    max_sf=1800,
    min_beds=3,
    max_beds=4,
    min_acres=0.75,
    max_acres=3.0,
    months_back=24,
    zips=MARKET_ZIPS
):
    cutoff = pd.Timestamp.today() - pd.DateOffset(months=months_back)

    return df[
        (df["Property type"].str.contains("Single", case=False, na=False)) &
        (df["Living area"].between(min_sf, max_sf)) &
        (df["Bedrooms"].between(min_beds, max_beds)) &
        (df["Lot acres"].between(min_acres, max_acres)) &
        (df["Sold date"] >= cutoff) &
        (df["Zip"].isin(zips))
    ].copy()


def filter_land(
    df,
    min_acres=1.5,
    max_acres=6.5,
    months_back=36,
    zips=MARKET_ZIPS
):
    cutoff = pd.Timestamp.today() - pd.DateOffset(months=months_back)

    return df[
        (df["Property type"].str.contains("Land|Lot", case=False, na=False)) &
        (df["Lot acres"].between(min_acres, max_acres)) &
        (df["Sold date"] >= cutoff) &
        (df["Zip"].isin(zips))
    ].copy()


def summarize(df):
    return {
        "Count": int(len(df)),
        "Median Price": float(df["Property price (USD)"].median()),
        "Mean Price": float(df["Property price (USD)"].mean()),
        "Median $/sf": float(df["$/sf"].median()),
        "Median Acres": float(df["Lot acres"].median())
    }


if __name__ == "__main__":
    df = load_data()

    improved = filter_improved(df)
    land = filter_land(df)

    print("IMPROVED SUMMARY")
    print(summarize(improved))
    print()

    print("LAND SUMMARY")
    print(summarize(land))
