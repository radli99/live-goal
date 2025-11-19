import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="⚽ Élő meccsek", layout="wide")
st.title("⚽ Élő meccsek - API-Football")

API_KEY = "fc06e8b1b7mshf2cd68d9cffe46dp1ccaabjsn68c1329c3368"
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()

matches_list = []

# Ha nincs élő meccs, dummy adatok
if "response" not in data or len(data["response"]) == 0:
    st.info("Jelenleg nincs élő meccs, dummy adatokkal dolgozunk.")
    matches_list = [
        {"Hazai": "Manchester United", "Vendég": "Liverpool", "Perc": 34, "Gól": "1 - 0"},
        {"Hazai": "Barcelona", "Vendég": "Real Madrid", "Perc": 12, "Gól": "0 - 0"},
    ]
else:
    for match in data["response"]:
        fixture = match["fixture"]
        teams = match["teams"]
        score = match["goals"]
        matches_list.append({
            "Hazai": teams['home']['name'],
            "Vendég": teams['away']['name'],
            "Perc": fixture['status']['elapsed'] or 0,
            "Gól": f"{score['home']} - {score['away']}"
        })

df = pd.DataFrame(matches_list)

# Szűrők
st.sidebar.header("🔍 Szűrés")
max_minute = st.sidebar.slider("Maximum perc", 0, 120, 45)
min_goals = st.sidebar.slider("Minimum gól összesen", 0, 10, 0)

filtered = df[
    (df["Perc"] <= max_minute) &
    (df["Gól"].apply(lambda x: sum(int(i) for i in x.split(" - "))) >= min_goals)
]

st.subheader("📊 Élő meccsek")
st.dataframe(filtered)

# Jelzések
st.subheader("🚨 Jelzések")
for idx, row in filtered.iterrows():
    home_goals, away_goals = [int(i) for i in row["Gól"].split(" - ")]
    if home_goals + away_goals >= 2:
        st.write(f"⚡ Több gól lehet: {row['Hazai']} vs {row['Vendég']} ({row['Gól']})")
