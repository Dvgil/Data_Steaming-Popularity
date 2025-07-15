import os 
from dotenv import load_dotenv
import pandas as pd
import requests


#load environment variables from .env file
load_dotenv()

#Reead the API key 
api_key = os.getenv("API_KEY")

url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"
response = requests.get(url)

if response.status_code != 200:
    print("Fail to fetch data from TMDb API")
    exit()

data = response.json()['results']
#
df = pd.DataFrame(data)

# Step 2: Clean and select useful columns
columns = ['title', 'popularity', 'vote_average', 'vote_count', 'release_date', 'original_language']
df = df[columns]

# Convert release_date to datetime
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Step 3: Analyze data

# 1. Most popular movie
most_popular = df.sort_values(by='popularity', ascending=False).head(1)

# 2. Highest rated (with at least 100 votes)
top_rated = df[df['vote_count'] > 100].sort_values(by='vote_average', ascending=False).head(1)

# 3. Average rating by language
avg_rating_by_lang = df.groupby('original_language')['vote_average'].mean().sort_values(ascending=False)

# Step 4: Output results
print("\n🎥 Most Popular Movie:\n", most_popular[['title', 'popularity']])
print("\n🏆 Highest Rated Movie (100+ votes):\n", top_rated[['title', 'vote_average', 'vote_count']])
print("\n🌐 Average Rating by Language:\n", avg_rating_by_lang)