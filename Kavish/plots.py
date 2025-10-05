import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
df = pd.read_csv("pune_dataset.csv")
df['datetime_UTC'] = pd.to_datetime(df['datetime_UTC'])

sns.set(style="whitegrid")

# 1. TIME-SERIES VISUALIZATIONS
# Line plots for pollutants
plt.figure(figsize=(12,6))
plt.plot(df['datetime_UTC'], df['PM2.5_ugm3'], marker='o', label='PM2.5')
plt.plot(df['datetime_UTC'], df['NO2_ppb'], marker='s', label='NO2')
plt.legend()
plt.title("Pollutants Over Time")
plt.xlabel("Time"); plt.ylabel("Concentration")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Rolling average
df['PM2.5_roll'] = df['PM2.5_ugm3'].rolling(3).mean()
plt.figure(figsize=(12,6))
plt.plot(df['datetime_UTC'], df['PM2.5_ugm3'], alpha=0.5, label="Original")
plt.plot(df['datetime_UTC'], df['PM2.5_roll'], color="red", label="3-hr Rolling Avg")
plt.title("PM2.5 Rolling Average")
plt.legend(); plt.show()

# 2. DISTRIBUTIONS
plt.figure(figsize=(10,6))
sns.histplot(df['NO2_ppb'], bins=8, kde=True, color="blue")
plt.title("Distribution of NO2")
plt.show()

sns.kdeplot(df['PM2.5_ugm3'], shade=True, color="red")
plt.title("KDE Curve of PM2.5")
plt.show()

# 3. COMPARISONS
plt.figure(figsize=(12,6))
sns.boxplot(x="RH_percent", y="PM2.5_ugm3", data=df)
plt.title("Boxplot: PM2.5 vs Humidity Levels")
plt.show()

plt.figure(figsize=(12,6))
sns.violinplot(x="RH_percent", y="NO2_ppb", data=df)
plt.title("Violin Plot: NO2 vs Humidity")
plt.show()

# 4. RELATIONSHIPS
sns.scatterplot(x='temp_C', y='PM2.5_ugm3', hue='RH_percent', data=df, palette="coolwarm", s=100)
plt.title("PM2.5 vs Temperature (Colored by Humidity)")
plt.show()

sns.lmplot(x='temp_C', y='NO2_ppb', data=df, height=6, aspect=1.2)
plt.title("Linear Regression: NO2 vs Temperature")
plt.show()

# 5. HEATMAP + PAIRPLOT
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

sns.pairplot(df[['PM2.5_ugm3','NO2_ppb','temp_C','RH_percent','wind_spd_ms','pressure_hPa']])
plt.show()

# 6. WIND ROSE (Polar Scatter)
plt.figure(figsize=(8,8))
ax = plt.subplot(111, polar=True)
theta = np.deg2rad(df['wind_dir_deg'])
r = df['wind_spd_ms']
ax.scatter(theta, r, c=r, cmap='viridis', s=120, alpha=0.7)
ax.set_title("Wind Rose (Direction vs Speed)")
plt.show()

# 7. ADVANCED VISUALIZATIONS (with Plotly for interactivity)
fig = px.line(df, x="datetime_UTC", y=["PM2.5_ugm3","NO2_ppb"], title="Interactive Pollutant Trends")
fig.show()

fig = px.scatter(df, x="temp_C", y="PM2.5_ugm3", size="RH_percent", color="NO2_ppb",
                 title="PM2.5 vs Temp (bubble size = Humidity, color = NO2)")
fig.show()

fig = px.density_heatmap(df, x="temp_C", y="PM2.5_ugm3", nbinsx=10, nbinsy=10,
                         title="Density Heatmap of PM2.5 vs Temperature")
fig.show()


#8
import folium
from folium.plugins import HeatMap
import plotly.express as px

# ✅ Plotly Scatter Map (Air Quality Levels on Pune Map)
fig = px.scatter_mapbox(
    df, lat="lat", lon="lon",
    color="PM2.5_ugm3",
    size="NO2_ppb",
    hover_name="datetime_UTC",
    hover_data={"temp_C": True, "RH_percent": True},
    color_continuous_scale="RdYlGn_r",
    size_max=30,
    zoom=10,
    title="Air Quality Map (PM2.5 color, NO2 size)"
)
fig.update_layout(mapbox_style="open-street-map")
fig.show()

# ✅ Folium Map: Simple Markers
pune_map = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=11)

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        color="red" if row['PM2.5_ugm3'] > 200 else "green",
        fill=True,
        popup=f"Time: {row['datetime_UTC']}<br>PM2.5: {row['PM2.5_ugm3']}<br>NO2: {row['NO2_ppb']}"
    ).add_to(pune_map)

# Save Folium map
pune_map.save("pune_air_quality_map.html")

# ✅ Folium Heatmap (PM2.5 hotspots)
heatmap_data = df[['lat','lon','PM2.5_ugm3']].values.tolist()
heatmap_map = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=11)
HeatMap(heatmap_data).add_to(heatmap_map)
heatmap_map.save("pune_air_quality_heatmap.html")
