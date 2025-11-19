import streamlit as st
import pandas as pd

st.set_page_config(page_title="Élő Gólstratégia", layout="wide")
st.title("⚽ Élő Gólstratégia - Online Streamlit App")

# Dummy adatok
matches = pd.DataFrame([
    {"Hazai": "Team A", "Vendég": "Team B", "Perc": 22, "Lövések": 12, "Kapura": 5, "Gól": "0 - 0"},
    {"Hazai": "Team C", "Vendég": "Team D", "Perc": 38, "Lövések": 6, "Kapura": 1, "Gól": "1 - 0"},
    {"Hazai": "Team E", "Vendég": "Team F", "Perc": 18, "Lövések": 15, "Kapura": 7, "Gól": "0 - 1"},
    {"Hazai": "Team G", "Vendég": "Team H", "Perc": 10, "Lövések": 20, "Kapura": 10, "Gól": "1 - 1"},
])

# Szűrők
st.sidebar.header("🔍 Szűrés")
min_shots = st.sidebar.slider("Minimum lövések", 0, 30, 10)
min_on_target = st.sidebar.slider("Minimum kapura", 0, 15, 4)
max_minute = st.sidebar.slider("Maximum perc", 1, 90, 35)

# Szűrés
filtered = matches[
    (matches["Lövések"] >= min_shots) &
    (matches["Kapura"] >= min_on_target) &
    (matches["Perc"] <= max_minute)
]

st.subheader("📊 Minden meccs")
st.dataframe(matches)

st.subheader("✔ Szűrt találatok")
if filtered.empty:
    st.info("Nincs találat a feltételek szerint")
else:
    st.dataframe(filtered)
    st.success(f"Találatok száma: {len(filtered)}")

# Stratégiai jelzés
st.subheader("🚨 Jelzések")
for idx, row in filtered.iterrows():

    
    if row["Lövések"] >= 10 and row["Kapura"] >= 5:
        st.write(f"⚡ Erős jelzés: {row['Hazai']} vs {row['Vendég']} ({row['Gól']})")
