"""
API Connection Test Script
Tests connections to TMDB, OMDb, and YouTube APIs

Run this script to verify all API keys are working correctly.
"""

import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Load API keys
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def print_separator():
    """Print a visual separator"""
    print("\n" + "="*80 + "\n")

def test_tmdb_api():
    """Test TMDB API connection"""
    print("Testing TMDB API...")
    print(f"API Key loaded: {'✓' if TMDB_API_KEY else '✗'}")

    if not TMDB_API_KEY:
        print("❌ TMDB_API_KEY not found in .env file")
        return False

    # Test with Fight Club (movie ID: 550)
    url = f"https://api.themoviedb.org/3/movie/550?api_key={TMDB_API_KEY}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print("✅ TMDB API connection successful!")
            print(f"   Sample response - Title: {data.get('title')}")
            print(f"   Budget: ${data.get('budget'):,}")
            print(f"   Revenue: ${data.get('revenue'):,}")
            print(f"   Release Date: {data.get('release_date')}")
            return True
        elif response.status_code == 401:
            print("❌ TMDB API authentication failed - Invalid API key")
            return False
        else:
            print(f"❌ TMDB API request failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ TMDB API connection error: {e}")
        return False

def test_omdb_api():
    """Test OMDb API connection"""
    print("Testing OMDb API...")
    print(f"API Key loaded: {'✓' if OMDB_API_KEY else '✗'}")

    if not OMDB_API_KEY:
        print("❌ OMDB_API_KEY not found in .env file")
        return False

    # Test with Fight Club (IMDb ID: tt0137523)
    url = f"http://www.omdbapi.com/?i=tt0137523&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get('Response') == 'True':
                print("✅ OMDb API connection successful!")
                print(f"   Sample response - Title: {data.get('Title')}")
                print(f"   Year: {data.get('Year')}")
                print(f"   IMDb Rating: {data.get('imdbRating')}")
                print(f"   Genre: {data.get('Genre')}")
                return True
            else:
                print(f"❌ OMDb API error: {data.get('Error')}")
                return False
        else:
            print(f"❌ OMDb API request failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ OMDb API connection error: {e}")
        return False

def test_youtube_api():
    """Test YouTube Data API connection"""
    print("Testing YouTube Data API...")
    print(f"API Key loaded: {'✓' if YOUTUBE_API_KEY else '✗'}")

    if not YOUTUBE_API_KEY:
        print("❌ YOUTUBE_API_KEY not found in .env file")
        return False

    # Test with a simple search query
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=fight+club+trailer&type=video&maxResults=1&key={YOUTUBE_API_KEY}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if 'items' in data and len(data['items']) > 0:
                video = data['items'][0]
                print("✅ YouTube API connection successful!")
                print(f"   Sample response - Video Title: {video['snippet']['title']}")
                print(f"   Channel: {video['snippet']['channelTitle']}")
                print(f"   Video ID: {video['id']['videoId']}")
                return True
            else:
                print("❌ YouTube API returned no results")
                return False
        elif response.status_code == 403:
            print("❌ YouTube API authentication failed - Invalid API key or quota exceeded")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"❌ YouTube API request failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ YouTube API connection error: {e}")
        return False

def main():
    """Run all API tests"""
    print("\n" + "🎬 Movie Box Office Prediction - API Connection Test".center(80))
    print_separator()

    # Test each API
    tmdb_success = test_tmdb_api()
    print_separator()

    omdb_success = test_omdb_api()
    print_separator()

    youtube_success = test_youtube_api()
    print_separator()

    # Summary
    print("📊 Test Summary:")
    print(f"   TMDB API:    {'✅ Working' if tmdb_success else '❌ Failed'}")
    print(f"   OMDb API:    {'✅ Working' if omdb_success else '❌ Failed'}")
    print(f"   YouTube API: {'✅ Working' if youtube_success else '❌ Failed'}")
    print_separator()

    if tmdb_success and omdb_success and youtube_success:
        print("✅ All API connections successful! You're ready to collect data.")
    else:
        print("⚠️  Some API connections failed. Please check your API keys in the .env file.")
        print("\nTroubleshooting:")
        print("1. Verify API keys are correct in .env file")
        print("2. Check if you have internet connectivity")
        print("3. Ensure API keys are activated (some require email verification)")
        print("4. Check API quotas/rate limits")

    print()

if __name__ == "__main__":
    main()
