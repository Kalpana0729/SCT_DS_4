#!/usr/bin/env python
# coding: utf-8

# In[5]:


get_ipython().system('pip install folium')

import kagglehub
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium

# Download dataset from Kaggle
path = kagglehub.dataset_download("sobhanmoosavi/us-accidents")

print("Dataset downloaded to:", path)

# Define the CSV path
csv_path = f"{path}/US_Accidents_March23.csv"

# Load dataset
df = pd.read_csv(csv_path, low_memory=False)

# Display dataset shape and first few rows
print("Shape:", df.shape)
print(df.head())


# In[6]:


cols = ["Severity", "Start_Time", "Start_Lat", "Start_Lng", 
        "Weather_Condition", "Temperature(F)", "Visibility(mi)", 
        "Wind_Speed(mph)", "Precipitation(in)", "Sunrise_Sunset"]
df = df[cols]

# Convert Start_Time to datetime
df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")

# Extract useful time features
df["Hour"] = df["Start_Time"].dt.hour
df["DayOfWeek"] = df["Start_Time"].dt.day_name()

# Drop rows with too many missing values
df = df.dropna(subset=["Start_Lat", "Start_Lng", "Weather_Condition"])


# In[7]:


# a) By road/weather conditions
plt.figure(figsize=(12,5))
sns.countplot(data=df, x="Weather_Condition", order=df["Weather_Condition"].value_counts().iloc[:10].index)
plt.title("Top 10 Weather Conditions During Accidents")
plt.xticks(rotation=45)
plt.show()

# b) By time of day (hourly pattern)
plt.figure(figsize=(10,5))
sns.histplot(df["Hour"], bins=24, kde=False)
plt.title("Accidents by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Accidents")
plt.show()

# c) By day of week
plt.figure(figsize=(10,5))
sns.countplot(data=df, x="DayOfWeek", order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
plt.title("Accidents by Day of Week")
plt.show()


# In[8]:


sample_df = df.sample(2000, random_state=42)

map_center = [sample_df["Start_Lat"].mean(), sample_df["Start_Lng"].mean()]
accident_map = folium.Map(location=map_center, zoom_start=4)

for _, row in sample_df.iterrows():
    folium.CircleMarker(
        location=[row["Start_Lat"], row["Start_Lng"]],
        radius=2,
        color="red",
        fill=True,
        fill_opacity=0.6
    ).add_to(accident_map)

accident_map


# In[ ]:




