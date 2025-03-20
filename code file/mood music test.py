#Install Python latest version on the device before running the code.
!pip install simpleaudio pygame requests #Install the dependencies on the device.

import simpleaudio as sa
import os
import random
import re
import requests
import io
import pygame
import tempfile

# GitHub repository details 
GITHUB_USER = "Channa027"
GITHUB_REPO = "music-mood-reop"
GITHUB_BRANCH = "main"  # or "master"

def get_file_list_from_github(folder=""):
    """Gets a list of files from a specified folder in a GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{folder}?ref={GITHUB_BRANCH}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching file list: {response.status_code}, URL: {url}") 
        return []
    
    try:
        files = response.json()
        return [f["name"] for f in files if isinstance(f, dict) and f.get("type") == "file"]
    except Exception as e:
        print(f"Error processing JSON response: {e}")
        return []

def download_file_from_github(filepath):
    """Downloads a file from a specified path in a GitHub repository."""
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{filepath}"
    response = requests.get(raw_url)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error downloading file: {response.status_code}, URL: {raw_url}")
        return None

def play_music(filename):
    """Plays an MP3 audio file."""
    try:
        audio_data = download_file_from_github(filename)
        if not audio_data:
            print(f"Could not download {filename}")
            return
        
        pygame.mixer.init()
        
        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_data)
            temp_filename = temp_file.name

        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()

        # Keep the program running until the music finishes
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(temp_filename)  # Delete the temp file after playing

    except pygame.error as e:
        print(f"Pygame error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_logic(sentence):
    """Processes a simple logic sentence and plays music."""
    sentence = sentence.lower()
    mood_match = re.search(r"mood is (\w+)", sentence)
    
    if mood_match:
        mood = mood_match.group(1)
        music_folder = mood  # Assuming music folders are named after moods
        
        music_files = get_file_list_from_github(music_folder) 
        
        if music_files:
            selected_file = random.choice(music_files)
            play_music(f"{music_folder}/{selected_file}")  # Use forward slash for GitHub paths
        else:
            print(f"No music found for mood: {mood}")
    else:
        print("Invalid sentence format. Please specify mood using 'mood is <mood>'")

# Example usage
sentence = input("Enter a logic sentence (e.g., 'mood is happy'): ") 
process_logic(sentence)
