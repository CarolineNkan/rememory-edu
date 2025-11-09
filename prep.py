
import os
import pandas as pd

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def clean_dataset(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"⚠️ Skipping {filename} — not found.")
        return

    df = pd.read_csv(path)

    # Normalize column names
    df.columns = [c.strip().capitalize() for c in df.columns]

    # Rename variants (case-insensitive)
    rename_map = {}
    for col in df.columns:
        low = col.lower()
        if "country" in low:
            rename_map[col] = "Country"
        elif "location" in low:
            rename_map[col] = "Country"
        elif "year" in low:
            rename_map[col] = "Year"
        elif "impact" in low or "affected" in low or "deaths" in low:
            rename_map[col] = "Impact"
    df = df.rename(columns=rename_map)

    # Fill & clean
    if "Country" not in df.columns:
        df["Country"] = "Unknown"
    if "Year" not in df.columns:
        df["Year"] = None
    if "Impact" not in df.columns:
        df["Impact"] = 0

    df["Country"] = df["Country"].fillna("Unknown").astype(str).str.strip().replace("nan", "Unknown")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["Impact"] = pd.to_numeric(df["Impact"], errors="coerce").fillna(0).astype(int)

    # Drop rows with missing or empty countries
    df = df[df["Country"].notna() & (df["Country"] != "Unknown") & (df["Country"].str.strip() != "")]
    df = df.drop_duplicates().reset_index(drop=True)

    # Save back
    df.to_csv(path, index=False)
    print(f"✅ Cleaned {filename} — {len(df)} rows.")

def main():
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            clean_dataset(file)

if __name__ == "__main__":
    main()
