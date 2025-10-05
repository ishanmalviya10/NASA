import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('/pune_dataset.csv', parse_dates=['datetime_UTC'])

# Set the datetime column as index for time series plots
data.set_index('datetime_UTC', inplace=True)

# Set plot style
sns.set(style="whitegrid")

# 1. Time Series Plot for PM2.5 and NO2
plt.figure(figsize=(14,6))
plt.plot(data.index, data['PM2.5_ugm3'], label='PM2.5 (ug/m3)', color='red')
plt.plot(data.index, data['NO2_ppb'], label='NO2 (ppb)', color='blue')
plt.title('Time Series of PM2.5 and NO2')
plt.xlabel('DateTime (UTC)')
plt.ylabel('Concentration')
plt.legend()
plt.show()

# 2. Distribution Plot for PM2.5
plt.figure(figsize=(8,5))
sns.histplot(data['PM2.5_ugm3'], bins=20, kde=True, color='red')
plt.title('Distribution of PM2.5 Concentration')
plt.xlabel('PM2.5 (ug/m3)')
plt.ylabel('Frequency')
plt.show()

# 3. Distribution Plot for NO2
plt.figure(figsize=(8,5))
sns.histplot(data['NO2_ppb'], bins=20, kde=True, color='blue')
plt.title('Distribution of NO2 Concentration')
plt.xlabel('NO2 (ppb)')
plt.ylabel('Frequency')
plt.show()

# 4. Scatter Plot: PM2.5 vs NO2
plt.figure(figsize=(8,6))
sns.scatterplot(x='NO2_ppb', y='PM2.5_ugm3', data=data, hue='temp_C', palette='coolwarm')
plt.title('Scatter Plot of PM2.5 vs NO2 with Temperature Hue')
plt.xlabel('NO2 (ppb)')
plt.ylabel('PM2.5 (ug/m3)')
plt.colorbar(label='Temperature (C)')
plt.show()

# 5. Correlation Heatmap of all numeric variables
plt.figure(figsize=(10,8))
corr = data.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

# 6. Line plot for Temperature and Relative Humidity over time
plt.figure(figsize=(14,6))
plt.plot(data.index, data['temp_C'], label='Temperature (C)', color='orange')
plt.plot(data.index, data['RH_percent'], label='Relative Humidity (%)', color='green')
plt.title('Temperature and Relative Humidity Over Time')
plt.xlabel('DateTime (UTC)')
plt.ylabel('Value')
plt.legend()
plt.show()

# 7. Wind Speed and Wind Direction Polar Plot
plt.figure(figsize=(8,8))
ax = plt.subplot(111, polar=True)
# Convert wind direction degrees to radians
wind_dir_rad = data['wind_dir_deg'] * (3.14159265 / 180)
sc = ax.scatter(wind_dir_rad, data['wind_spd_ms'], c=data['PM2.5_ugm3'], cmap='Reds', alpha=0.75)
plt.title('Wind Speed and Direction with PM2.5 Intensity')
cbar = plt.colorbar(sc, pad=0.1)
cbar.set_label('PM2.5 (ug/m3)')
plt.show()

# 8. Boxplot of PM2.5 by Hour of Day
data['hour'] = data.index.hour
plt.figure(figsize=(12,6))
sns.boxplot(x='hour', y='PM2.5_ugm3', data=data, palette='Reds')
plt.title('Boxplot of PM2.5 Concentration by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('PM2.5 (ug/m3)')
plt.show()

# 9. Line plot for Boundary Layer Height (BLH) and AOD_MODIS over time
plt.figure(figsize=(14,6))
plt.plot(data.index, data['BLH_m'], label='Boundary Layer Height (m)', color='purple')
plt.plot(data.index, data['AOD_MODIS'], label='AOD MODIS', color='brown')
plt.title('Boundary Layer Height and AOD MODIS Over Time')
plt.xlabel('DateTime (UTC)')
plt.ylabel('Value')
plt.legend()
plt.show()

# 10. Pairplot for selected variables
sns.pairplot(data[['PM2.5_ugm3', 'NO2_ppb', 'temp_C', 'RH_percent', 'wind_spd_ms']])
plt.suptitle('Pairplot of Selected Variables', y=1.02)
plt.show()
