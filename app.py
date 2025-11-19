import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="⚽ Élő Gólstratégia", layout="wide")
st.title("⚽ Élő Gólstratégia - API-Football")

API_KEY = "038b24c76b12fe2f19de30f7e5556088"  # a te kulcsod
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Élő meccs adatok lekérése
response = requests.get(url, headers=headers)
data = response.json()

matches_list = []

for match in data.get('response', []):
    fixture = match['fixture']
    teams = match['teams']
    score = match['goals']
    matches_list.append({
        "Hazai": teams['home']['name'],
        "Vendég": teams['away']['name'],
        "Perc": fixture['status']['elapsed'] or 0,
        "Gól": f"{score['home']} - {score['away']}",
        "Lövések": 5,  # dummy érték
        "Kapura": 2    # dummy érték
    })

matches = pd.DataFrame(matches_list)

# Oldalsáv szűrők
st.sidebar.header("🔍 Szűrési beállítások")
min_shots = st.sidebar.slider("Minimum lövések", 0, 30, 5)
min_on_target = st.sidebar.slider("Minimum kapura", 0, 15, 2)
max_minute = st.sidebar.slider("Maximum perc", 0, 90, 45)

# Szűrt meccsek
filtered = matches[
    (matches["Lövések"] >= min_shots) &
    (matches["Kapura"] >= min_on_target) &
    (matches["Perc"] <= max_minute)
]

st.subheader("📊 Szűrt meccsek")
if filtered.empty:
    st.info("Nincs találat a szűrőfeltételek szerint")
else:
    st.dataframe(filtered)

# Stratégiai jelzés
st.subheader("🚨 Jelzések")
for idx, row in filtered.iterrows():
    if row["Lövések"] >= 10 and row["Kapura"] >= 5:
        st.write(f"⚡ Erős jelzés: {row['Hazai']} vs {row['Vendég']} ({row['Gól']})")
