import sys, os
import json
import time
import pprint
import azlyrics as az
import spotipy
import spotipy.util as util

from colorama import init, Fore


def load_params_and_get_token():
    params = json.load(open("client_secrets.json"))
    auth_token = util.prompt_for_user_token(
        params["username"],
        params["scope"],
        client_id=params["client_id"],
        client_secret=params["client_secret"],
        redirect_uri=params["redirect_uri"],
    )
    return auth_token


def lyric_loop(curr_tr, sp):
    try:
        results = sp.currently_playing()
        artist_name = results["item"]["album"]["artists"][0]["name"]
        song_name = results["item"]["name"]
        current_progress = results["progress_ms"]
        total_duration = results["item"]["duration_ms"]
        progress = round((current_progress / total_duration) * 100, 2)
        if song_name != curr_tr:
            lyrics = az.extract_lyrics(artist_name, song_name)
            az.color_print_title([song_name, artist_name])
            az.pretty_print_lyrics(lyrics)
            az.color_print_progress(progress)
            return {
                "title": song_name,
                "cur_prog": current_progress,
                "tot_dur": total_duration,
            }
        else:
            az.color_print_progress(progress)
            return {
                "title": song_name,
                "cur_prog": current_progress,
                "tot_dur": total_duration,
            }
    except TypeError:
        print(Fore.RED + "\rNo Track is playing", end="")


if __name__ == "__main__":
    init(autoreset=True)
    curr_track = ""

    token = load_params_and_get_token()
    if token:
        sp = spotipy.Spotify(auth=token)
        while True:
            try:
                curr_track = lyric_loop(curr_track, sp)["title"]
                time.sleep(10)
            except KeyboardInterrupt:
                print("\b\b  \n\rShutting Down")
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
    else:
        print("Can't get token")
