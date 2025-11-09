import os
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(page_title="ReMemory  — Decode the Past", page_icon="🌍", layout="wide")

CSS = """
<style>
:root{
  --bg:#F7FAFC;
  --card:#FFFFFF;
  --ink:#1F2937;
  --muted:#6B7280;
  --blue:#1B4E9B;
  --aqua:#00A8E8;
  --ring:rgba(27,78,155,0.12);
}
html, body, .stApp {background:var(--bg);}
.rem-card{
  background:var(--card);border-radius:14px;padding:18px;
  border:1px solid #E5E7EB;box-shadow:0 6px 14px rgba(0,0,0,0.04);
}
h1,h2,h3{color:var(--ink);}
.rem-tip{background:#E6F0FB;border-radius:12px;padding:12px;font-size:0.9rem;color:#1B4E9B;}
.rem-section{margin-top:1.5rem;margin-bottom:0.5rem;font-weight:700;color:var(--ink);display:flex;align-items:center;gap:8px;}
.rem-section span{width:10px;height:10px;background:var(--aqua);border-radius:50%;box-shadow:0 0 0 4px var(--ring);}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

DATA_DIR = "data"
LOGO_PATH = "logo.png"

# ----------------------------------
# LOADERS
# ----------------------------------
@st.cache_data(show_spinner=False)
def load_csv(filename):
    """Clean and normalize individual EM-DAT CSV files."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return pd.DataFrame(columns=["Country", "Year", "Impact"])

    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    loc_col = next((c for c in df.columns if c in ["country", "location", "region", "place", "city", "admin"]), None)
    if loc_col:
        df.rename(columns={loc_col: "Country"}, inplace=True)
    else:
        df["Country"] = "Unknown"

    year_col = next((c for c in df.columns if "year" in c), None)
    if year_col:
        df.rename(columns={year_col: "Year"}, inplace=True)
    else:
        df["Year"] = None

    impact_col = next((c for c in df.columns if "impact" in c or "affected" in c), None)
    if impact_col:
        df.rename(columns={impact_col: "Impact"}, inplace=True)
    else:
        df["Impact"] = 0

    df["Country"] = df["Country"].astype(str).str.strip()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Impact"] = pd.to_numeric(df["Impact"], errors="coerce").fillna(0)
    df = df[df["Country"].ne("")].drop_duplicates(subset=["Country", "Year", "Impact"]).reset_index(drop=True)
    return df


@st.cache_data(show_spinner=False)
def build_country_list():
    """Combine all countries across EM-DAT datasets."""
    all_csvs = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    all_countries = set()
    for f in all_csvs:
        df = load_csv(f)
        all_countries.update(df["Country"].unique().tolist())
    return all_csvs, sorted([c for c in all_countries if c and c != "Unknown"])


def load_contacts():
    """Load universal emergency + donation contacts."""
    path = os.path.join(DATA_DIR, "contacts.json")
    universal = {
        "emergency_numbers": [
            {"label": "112 — Europe (EU standard)"},
            {"label": "911 — USA, Canada, Caribbean"},
            {"label": "999 — UK, Hong Kong, Malaysia"},
            {"label": "119 — Japan, South Korea"},
        ],
        "global_ops": {"name": "WHO Emergency Operations", "url": "https://www.who.int/emergencies"},
        "donations": [
            ("IFRC Disaster Relief Fund", "https://www.ifrc.org/donate"),
            ("UN OCHA Crisis Relief", "https://crisisrelief.un.org/"),
            ("GlobalGiving Disaster Response", "https://www.globalgiving.org/disasters/"),
            ("CARE Emergency Programs", "https://www.care.org/get-involved/donate/"),
        ],
        "cta": "Even if local data is limited, you can help protect the future — donate or share trusted disaster resources globally.",
    }
    if not os.path.exists(path):
        return {"universal": universal}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    data["universal"] = data.get("universal", universal)
    return data


def ai_preparedness_text(disaster, country, years=None, data_available=False):
    """Adaptive preparedness summary."""
    period = f" based on {years[0]}–{years[1]}" if years else ""
    if data_available:
        header = f"<b>Preparedness & Early Recovery Brief for {disaster.lower()}s in {country}{period}</b>"
    else:
        header = f"<b>No historical EM-DAT records found for {country}. Here's how to stay prepared for {disaster.lower()}s:</b>"

    return f"""
<div class="rem-card" style="line-height:1.7; font-size:0.96rem;">
  <p>{header}</p>
  <ul style="margin-top:0.6rem;">
    <li>🧺 <b>Before:</b> Prepare emergency kits (water, meds, IDs, flashlights, chargers).</li>
    <li>🚦 <b>During:</b> Follow official alerts, move to safe zones or higher ground.</li>
    <li>🏠 <b>After:</b> Assess structure safety, document losses, sanitize water.</li>
    <li>🤝 <b>Community:</b> Stay connected with neighbors, support recovery programs.</li>
  </ul>
  <p style="margin-top:0.8rem; font-style:italic;">Even when data is scarce, preparedness saves lives. 🌍</p>
</div>
"""

# ----------------------------------
# SIDEBAR
# ----------------------------------
st.sidebar.markdown("### 💧 Choose Disaster & Location")

all_csvs, all_countries = build_country_list()

disaster = st.sidebar.selectbox("Disaster Type", ["Flood", "Hurricane", "Wildfire", "Drought", "Earthquake"])
dataset = st.sidebar.selectbox("Dataset File", [f for f in all_csvs if disaster.lower() in f.lower()] or all_csvs)
df = load_csv(dataset)

country = st.sidebar.selectbox("Filter by Country", all_countries)
st.sidebar.markdown('<div class="rem-tip">🌍 Powered by EM-DAT (2000–2025). Covering 100+ nations and 5 disaster types.</div>', unsafe_allow_html=True)

# ----------------------------------
# MAIN CONTENT
# ----------------------------------
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=90)

st.markdown("## ReMemory : Decoding the Past to Protect the Future")
st.caption("Built for Code the Past 2025 | Expanded for Build-a-thon 2025 — Education ✕ Green Tech ✕ Resilience")
st.write("Using historical disaster data to uncover lessons that safeguard our future.")

# DATA SUMMARY
st.markdown('<div class="rem-section"><span></span><h3>Dataset Summary</h3></div>', unsafe_allow_html=True)

if not df.empty:
    dsub = df[df["Country"].str.lower() == country.lower()]
else:
    dsub = pd.DataFrame()

if not dsub.empty:
    valid_years = dsub["Year"].dropna()
    if not valid_years.empty:
        y_min, y_max = int(valid_years.min()), int(valid_years.max())
        years = (y_min, y_max)
        st.write(f"**Records:** {len(dsub)} | **Years:** {y_min}–{y_max} | **Total Affected:** {int(dsub['Impact'].sum()):,}")
    else:
        st.write(f"**Records:** {len(dsub)} | **Years:** Not available | **Total Affected:** {int(dsub['Impact'].sum()):,}")
        years = None

    dsub_clean = dsub.dropna(subset=["Year"])
    if not dsub_clean.empty:
        chart = px.line(
            dsub_clean,
            x="Year",
            y="Impact",
            markers=True,
            title=f"{disaster} Impact Trends ({country})"
        )
        chart.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis_title="Year",
            yaxis_title="People Affected",
            template="plotly_white"
        )
        st.plotly_chart(chart, width="stretch")
    else:
        st.info("No valid year data available for this location.")
else:
    st.warning("No EM-DAT records found for this country in the selected dataset.")
    years = None

# PREPAREDNESS
st.markdown('<div class="rem-section"><span></span><h3>Preparedness & Early Recovery</h3></div>', unsafe_allow_html=True)
st.markdown(ai_preparedness_text(disaster, country, years, data_available=not dsub.empty), unsafe_allow_html=True)

# RESPONSE NETWORK
st.markdown('<div class="rem-section"><span></span><h3>Response Network</h3></div>', unsafe_allow_html=True)
contacts = load_contacts()
universal = contacts.get("universal", {})

# Emergency
st.markdown("### 🆘 Emergency & Recovery Resources")
st.markdown('<div class="rem-card">', unsafe_allow_html=True)
for num in universal.get("emergency_numbers", []):
    st.markdown(f"- {num['label']}")
ops = universal.get("global_ops", {})
if ops:
    st.markdown(f"**Coordination:** [{ops['name']}]({ops['url']})")
st.markdown("</div>", unsafe_allow_html=True)

# Donations
st.markdown("### 🌍 Global Relief & Recovery Support")
st.markdown('<div class="rem-card">', unsafe_allow_html=True)
for n, u in universal.get("donations", []):
    st.markdown(f"- [{n}]({u})")
if universal.get("cta"):
    st.markdown(f"---\n🌍 *{universal['cta']}*")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("ReMemory EDU — Using the past to safeguard the future.")
