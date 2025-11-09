import pandas as pd
import plotly.express as px
import re

def load_dataset(filename):
    """Load and clean dataset from /data folder ensuring consistent columns and fallback country detection."""
    try:
        df = pd.read_csv(f"data/{filename}")
        df.columns = df.columns.str.strip()

        # Flexible column detection
        location_cols = ["Location", "Country", "Entity", "Region", "Nation", "Admin1", "Admin2"]
        year_cols = ["Year", "Start Year", "Start year", "Start", "year"]
        impact_cols = ["Impact", "Total Affected", "total_affected", "Affected", "Deaths", "Damage_USD", "Total Deaths"]

        # Identify best-matching columns
        loc_col = next((c for c in df.columns if c in location_cols), None)
        year_col = next((c for c in df.columns if c in year_cols), None)
        impact_col = next((c for c in df.columns if c in impact_cols), None)

        # Rename to standardized names
        rename_map = {}
        if loc_col: rename_map[loc_col] = "Country"
        if year_col: rename_map[year_col] = "Year"
        if impact_col: rename_map[impact_col] = "Impact"
        df.rename(columns=rename_map, inplace=True)

        # Add any missing columns
        for col in ["Country", "Year", "Impact"]:
            if col not in df.columns:
                df[col] = None

        #  Fallback: infer country from filename       
        code_map = {
            "bd": "Bangladesh",
            "ph": "Philippines",
            "gr": "Greece",
            "jm": "Jamaica",
            "sd": "Sudan",
            "ke": "Kenya",
            "jp": "Japan",
            "us": "United States of America"
        }

        if df["Country"].isna().all() or (df["Country"].astype(str).str.lower() == "nan").all():
            match = re.search(r"_([a-z]{2})\.csv$", filename)
            if match:
                code = match.group(1)
                fallback_country = code_map.get(code, None)
                if fallback_country:
                    df["Country"] = fallback_country
            else:
                # fallback if dataset name is just floods.csv, droughts.csv, etc.
                df["Country"] = "Global"

        # Cleanup 
        df = df.dropna(subset=["Year"], how="any")
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(0).astype(int)
        df["Impact"] = pd.to_numeric(df["Impact"], errors="coerce").fillna(0)
        df["Country"] = df["Country"].astype(str).str.strip()

        # Remove placeholder entries
        df = df[df["Country"].str.lower().isin(["nan", "none"]) == False]

        return df

    except Exception as e:
        raise RuntimeError(f"Failed to load dataset {filename}: {e}")


def make_trend_chart(df, title):
    """Generate interactive Plotly line chart showing disaster impact trends."""
    if df.empty:
        raise ValueError("Dataset is empty, cannot generate chart.")

    fig = px.line(
        df,
        x="Year",
        y="Impact",
        color="Country" if "Country" in df.columns else None,
        title=title,
        markers=True,
        labels={"Impact": "People Affected", "Year": "Year"},
        line_shape="spline"
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        xaxis_title="Year",
        yaxis_title="People Affected",
        title_x=0.5,
        title_font_size=20,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig
