import streamlit as st
import requests
import pandas as pd

st.title("⚽ Élő meccsek - SportDB.dev Flashscore")

API_KEY = "YOUR_API_KEY"  # ide írd a kulcsodat
url = "https://api.sportdb.dev/api/flashscore/"

headers = {"X-API-Key": API_KEY}
response = requests.get(url, headers=headers)
data = response.json()

matches_list = []
for match in data.get("data", []):
    matches_list.append({
        "Hazai": match["home_team"]["name"],
        "Vendég": match["away_team"]["name"],
        "Perc": match.get("minute", 0),
        "Gól": f"{match.get('home_score',0)} - {match.get('away_score',0)}"
    })

df = pd.DataFrame(matches_list)

st.subheader("📊 Élő meccsek")
st.dataframe(df)
