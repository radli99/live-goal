import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="⚽ Élő meccsek", layout="wide")
st.title("⚽ Élő meccsek - SportDB.dev Live Fixtures")

API_KEY = "038b24c76b12fe2f19de30f7e5556088"  # a te kulcsod
url = "https://api.sportdb.dev/api/fixtures/live/"

headers = {"X-API-Key": API_KEY}
response = requests.get(url, headers=headers)
data = response.json()

# Ellenőrizzük, hogy van-e élő meccs
if "data" not in data or len(data["data"]) == 0:
    st.info("Jelenleg nincs élő meccs vagy a Free Tier nem ad adatot.")
else:
    matches_list = []
    for match in data["data"]:
        matches_list.append({
            "Hazai": match["home_team"]["name"],
            "Vendég": match["away_team"]["name"],
            "Perc": match.get("minute", 0),
            "Gól": f"{match.get('home_score', 0)} - {match.get('away_score', 0)}"
        })

    df = pd.DataFrame(matches_list)

    # Szűrők az oldalsávon
    st.sidebar.header("🔍 Szűrés")
    max_minute = st.sidebar.slider("Maximum perc", 0, 120, 45)
    min_goals = st.sidebar.slider("Minimum gól összesen", 0, 10, 0)

    filtered = df[
        (df["Perc"] <= max_minute) &
        (df["Gól"].apply(lambda x: sum(int(i) for i in x.split(" - "))) >= min_goals)
    ]

    st.subheader("📊 Élő meccsek")
    st.dataframe(filtered)

    # Jelzések (példa stratégia)
    st.subheader("🚨 Jelzések")
    for idx, row in filtered.iterrows():
        home_goals, away_goals = [int(i) for i in row["Gól"].split(" - ")]
        if home_goals + away_goals >= 2:
            st.write(f"⚡ Több gól lehet: {row['Hazai']} vs {row['Vendég']} ({row['Gól']})")
