import streamlit as st
import pandas as pd

st.set_page_config(page_title="Élő Gólstratégia", layout="wide")
st.title("⚽ Élő Gólstratégia - Online Streamlit App")

# Dummy meccsadatok
matches = pd.DataFrame([
    {"Hazai": "Team A", "Vendég": "Team B", "Perc": 22, "Lövések": 12, "Kapura": 5, "Gól": "0 - 0"},
    {"Hazai": "Team C", "Vendég": "Team D", "Perc": 38, "Lövések": 6,  "Kapura": 1, "Gól": "1 - 0"},
    {"Hazai": "Team E", "Vendég": "Team F", "Perc": 18, "Lövések": 15, "Kapura": 7, "Gól": "0 - 1"},
    {"Hazai": "Team G", "Vendég": "Team H", "Perc": 10, "Lövések": 20, "Kapura": 10, "Gól": "1 - 1"},
])

# Oldalsáv szűrők
st.sidebar.header("🔍 Szűrési beállítások")
min_shots = st.sidebar.slider("Minimum össz-lövésszám", 0, 30, 10)
min_on_target = st.sidebar.slider("Minimum kapura lövések", 0, 15, 4)
max_minute = st.sidebar.slider("Maximum perc", 1, 90, 35)

# Szűrés
filtered = matches[
    (matches["Lövések"] >= min_shots) &
    (matches["Kapura"] >= min_on_target) &
    (matches["Perc"] <= max_minute)
]

# Minden meccs
st.subheader("📊 Minden meccs")
st.dataframe(matches)

# Szűrt találatok
st.subheader("✔ Szűrt találatok")
if filtered.empty:
    st.info("Nincs találat a megadott feltételek alapján.")
else:
    st.success(f"Találatok száma: {len(filtered)}")
    st.dataframe(filtered)

# Extra stratégiai jelzés
st.subheader("🚨 Stratégiai jelzés")
for idx, row in filtered.iterrows():
    if int(row["Lövések"]) >= 10 and int(row["Kapura"]) >= 5:
        st.write(f"⚡ Erős jelzés: {row['Hazai']} vs {row['Vendég']} ({row['Gól']})")
