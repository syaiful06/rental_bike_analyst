import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_total_bike_rentals(df):
    total_bike_df = df.groupby(by="mnth").cnt.sum().reset_index()
    return total_bike_df

def create_season_bike_rentals(df):
    season_bike_df = df.groupby("season").cnt.sum().reset_index()
    return season_bike_df

def create_user_bike_rentals(df):
    user_bike_df = df.groupby("yr").agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()
    return user_bike_df

def create_rfm_analysis(df):
    last_date = df['dteday'].max()

    recency_df = df.groupby('mnth')['dteday'].max().reset_index()
    recency_df['Recency'] = (last_date - recency_df['dteday']).dt.days
    recency_df = recency_df[['mnth', 'Recency']]

    frequency_df = df.groupby('mnth')['cnt'].count().reset_index()
    frequency_df.columns = ['mnth', 'Frequency']

    monetary_df = df.groupby('mnth')['cnt'].sum().reset_index()
    monetary_df.columns = ['mnth', 'Monetary']

    rfm_df = recency_df.merge(frequency_df, on='mnth')
    rfm_df = rfm_df.merge(monetary_df, on='mnth')

    return rfm_df

all_df = pd.read_csv("C:/Users/TOSHIBA/submission/dashboard/main_data.csv")

all_df['dteday'] = pd.to_datetime(all_df['dteday'])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                  (all_df["dteday"] <= str(end_date))]

# Generate dataframes for analysis
total_bike_df = create_total_bike_rentals(main_df)
season_bike_df = create_season_bike_rentals(main_df)
user_bike_df = create_user_bike_rentals(main_df)
rfm_df = create_rfm_analysis(main_df)

st.header('Bike Rentals Dashboard :sparkles:')

st.subheader('Total Penyewa Sepeda Berdasarkan Bulan')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(total_bike_df["mnth"], total_bike_df["cnt"], marker='o', color="blueviolet")
ax.set_xticks(total_bike_df["mnth"])
ax.set_xticklabels(['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                   'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'])
ax.set_title("Total Penyewa Sepeda Per Tahun")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewa Sepeda")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

st.subheader('Persentase Penyewa Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(6, 6))
sizes = season_bike_df["cnt"]
labels = ['Musim semi', 'Musim panas', 'Musim gugur', 'Musim dingin']
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen', 'lightcoral', 'lightsalmon'])
ax.set_title("Persentase Penyewa Sepeda Berdasarkan Musim")
ax.axis('equal')
st.pyplot(fig)

st.subheader('Total Penyewa Sepeda Berdasarkan Jenis Pengguna')
years = user_bike_df["yr"]
casual = user_bike_df["casual"]
registered = user_bike_df["registered"]

bar_width = 0.35
x = np.arange(len(years))

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - bar_width/2, casual, width=bar_width, label='Casual', color='salmon')
bars2 = ax.bar(x + bar_width/2, registered, width=bar_width, label='Registered', color='blueviolet')

ax.set_title("Total Penyewa Sepeda Berdasarkan Jenis Pengguna")
ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Penyewa Sepeda")
ax.set_xticks(user_bike_df['yr'])
ax.set_xticklabels(['2011', '2012'])
ax.legend()

for bar in bars1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:,}', ha='center', va='bottom')

for bar in bars2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:,}', ha='center', va='bottom')

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.subheader('Tren Nilai RFM Penyewa Sepeda Dari Bulan Ke Bulan')

plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
sns.barplot(x='mnth', y='Recency', data=rfm_df, palette='viridis')
plt.title('Recency berdasarkan Bulan')
plt.xlabel('Bulan')
plt.ylabel('Recency (hari)')
plt.xticks(rotation=45)

plt.subplot(1, 3, 2)
sns.barplot(x='mnth', y='Frequency', data=rfm_df, palette='magma')
plt.title('Frequency berdasarkan Bulan')
plt.xlabel('Bulan')
plt.ylabel('Frequency')
plt.xticks(rotation=45)

plt.subplot(1, 3, 3)
sns.barplot(x='mnth', y='Monetary', data=rfm_df, palette='cividis')
plt.title('Monetary berdasarkan Bulan')
plt.xlabel('Bulan')
plt.ylabel('Monetary')
plt.xticks(rotation=45)

plt.tight_layout()
st.pyplot(plt)
plt.clf()
