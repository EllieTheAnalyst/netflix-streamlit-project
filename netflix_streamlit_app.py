import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("netflix_data.csv")
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

# Title
st.title("🎬 Netflix 90s Movie Explorer")

# Sidebar filters
decade = st.sidebar.selectbox("Choose a decade", [1980, 1990, 2000, 2010])
type_filter = st.sidebar.radio("Type", ["Movie", "TV Show"])
actor = st.sidebar.text_input("Search for Actor (e.g. Tom Hanks)", "")
genre = st.sidebar.text_input("Search by Genre", "")

# Filter base
filtered = df[(df['type'] == type_filter) & 
              (df['release_year'] >= decade) & 
              (df['release_year'] < decade + 10)]

if actor:
    filtered = filtered[filtered['cast'].str.contains(actor, case=False, na=False)]

if genre:
    filtered = filtered[filtered['genre'].str.contains(genre, case=False, na=False)]

# Show filtered count
st.subheader(f"Found {len(filtered)} titles")
st.dataframe(filtered[['title', 'release_year', 'genre', 'country', 'date_added']].sort_values(by='release_year'))

# Plot: Year Added
st.subheader(f"📅 When were {decade}s titles added to Netflix?")
year_added_counts = filtered['date_added'].dt.year.value_counts().sort_index()

fig, ax = plt.subplots()
year_added_counts.plot(kind='bar', ax=ax, color='skyblue')
plt.xlabel("Year Added")
plt.ylabel("Number of Titles")
plt.title(f"{decade}s {type_filter}s Added Over Time")
st.pyplot(fig)
