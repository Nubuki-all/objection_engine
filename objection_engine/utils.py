from .loading import load_music_data 
from collections import Counter
import os
import requests
import zipfile
import shutil
import json
from toml import dump
import re

try:
    import emoji
except ImportError:
    emoji = None

def strip_emojis(text):
    if emoji is not None:
        return emoji.replace_emoji(text, replace='')

    # Fallback to regex if emoji library is not installed
    # This regex matches characters outside the Basic Multilingual Plane (BMP)
    # which includes most emojis, but also some other characters.
    # It's a decent fallback.
    emoji_pattern = re.compile(r'[^\u0000-\u007F\u0080-\uFFFF]', flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def ensure_assets_are_available():
    from .loading import ASSETS_FOLDER
    if not os.path.exists(ASSETS_FOLDER) or not os.listdir(ASSETS_FOLDER):
        download_assets()
    else:
        # This is in case there are only some missing assets that have been added in updates
        if ASSETS_FOLDER == 'assets':
            detect_old_assets_format()

def download_assets():
    from .loading import ASSETS_FOLDER
    print(f'Assets for "{ASSETS_FOLDER}" not present. Downloading them')

    urls = {
        'assets': 'https://dl.luismayo.com/assetsv4.zip',
        'assets_v4': 'https://dl.luismayo.com/assetsv4.zip',
        'assets_aj': 'https://github.com/LuisMayo/objection_engine/releases/download/v3.5.1/assets_aj.zip',
    }

    url = urls.get(ASSETS_FOLDER)
    if url is None:
        print(f'Error: No download URL for asset pack "{ASSETS_FOLDER}"')
        return

    response = requests.get(url)
    zip_name = f'{ASSETS_FOLDER}.zip'
    with open(zip_name, 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        # If we extract directly into ASSETS_FOLDER, and the zip contains
        # a folder with the same name, we'll get nested folders.
        # Most of these zips (like assetsv4.zip) contain the folders
        # (characters/, music/, etc.) directly.
        # But our GitHub Action zips the folder itself.

        # To be safe, we extract to a temp folder and then move contents
        temp_extract_path = f'temp_{ASSETS_FOLDER}'
        zip_ref.extractall(temp_extract_path)

        # Check if the extracted folder contains exactly one folder that is named after the assets
        extracted_items = os.listdir(temp_extract_path)
        if len(extracted_items) == 1 and os.path.isdir(os.path.join(temp_extract_path, extracted_items[0])):
            src_path = os.path.join(temp_extract_path, extracted_items[0])
        else:
            src_path = temp_extract_path

        if not os.path.exists(ASSETS_FOLDER):
            os.makedirs(ASSETS_FOLDER)

        for item in os.listdir(src_path):
            s = os.path.join(src_path, item)
            d = os.path.join(ASSETS_FOLDER, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        shutil.rmtree(temp_extract_path)
    os.remove(zip_name)

def detect_old_assets_format():
    if os.path.exists('./Sprites-phoenix'):
        print("Old assets format detected. Moving assets folder to assets_old")
        os.rename("./assets", "./assets_old")
        download_assets()
        print("Migrating music (if any) to the new assets folder with the new assets config")
        for music_folder in os.listdir("./assets_old/music"):
            if not os.path.exists("./assets/music/" + music_folder):
                print("Migrating " + music_folder)
                try:
                    shutil.copytree("./assets_old/music/" + music_folder, "./assets/music/" + music_folder)
                except Exception as e:
                    print("Error while copying" + str(e))
                    continue 
                try:
                    with open("./assets/music/" + music_folder + "/config.json",'rt') as file_json:
                        old_config = json.load(file_json)
                        with open("./assets/music/" + music_folder + "/config.toml",'wt') as file_toml:
                            dump(old_config, file_toml)
                except Exception as e:
                    print("Error trying to convert the music format config file. Removing the folder")
                    try:
                        shutil.rmtree("./assets/music/" + music_folder)
                    except Exception as e2:
                        print("Error while trying to remove the folder. Music may be corrupted")
            else:
                print("Folder " + music_folder + " already existed on destination, omiting migration")

def get_all_music_available():
    ensure_assets_are_available()
    available_music = load_music_data()
    list = []
    for key in available_music.keys():
        list.append(key)
    list.append('rnd')
    return list

def is_music_available(music: str) -> bool:
    music = music.lower()
    available_music = get_all_music_available()
    available_music.append('rnd')
    return music in available_music
