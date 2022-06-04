import time
from pathlib import Path

import pyttsx3
import soundfile as sf
from rich.progress import track

from utils.console import print_step, print_substep


def _init_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 200)
    engine.runAndWait()
    return engine


def save_text_to_mp3(reddit_obj):
    """Saves Text to MP3 files.

    Args:
        reddit_obj : The reddit object you received from the reddit API in the askreddit.py file.
    """

    try:
        print_step("Saving Text to MP3 files 🎶")
        length = 0

        # Create a folder for the mp3 files.
        Path("assets/mp3").mkdir(parents=True, exist_ok=True)

        # tts = gTTS(text=reddit_obj["thread_title"], lang="en", slow=False, tld="com")
        # tts.save(f"assets/mp3/title.mp3")
        file_path = f"assets/mp3/title.wav"

        engine = _init_voice()
        engine.save_to_file(reddit_obj["thread_title"], file_path)
        engine.runAndWait()
        f = sf.SoundFile(file_path)
        len_in_sec = f.frames / f.samplerate
        print('seconds = {}'.format(f.frames / f.samplerate))

        # length += MP3(file_path).info.length
        length += len_in_sec

        for idx, comment in track(enumerate(reddit_obj["comments"]), "Saving..."):
            # ! Stop creating mp3 files if the length is greater than 50 seconds. This can be longer,
            # but this is just a good starting point
            if length > 50:
                break
            # tts = gTTS(text=comment["comment_body"], lang="en", slow=False, tld="com")
            # tts.save(f"assets/mp3/{idx}.mp3")
            subfile_path = f"assets/mp3/{idx}.wav"
            print(f"The comment body is {comment['comment_body']}")

            engine.save_to_file(comment["comment_body"], subfile_path)
            engine.runAndWait()

            f = sf.SoundFile(subfile_path)
            len_in_sec = f.frames / f.samplerate
            print(f"The file length is {len_in_sec}")
            # length += MP3(f"assets/mp3/{idx}.mp3").info.length
            length += len_in_sec

        print_substep("Saved Text to MP3 files Successfully.", style="bold green")
        # ! Return the index so we know how many screenshots of comments we need to make.
        engine.stop()
        return length, idx
    except Exception as e:
        print(f"The raised error {e}")
        return None, None
