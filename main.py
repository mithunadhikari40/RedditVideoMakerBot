import time
from pathlib import Path

import pyttsx3
from mutagen.mp3 import MP3

from reddit.askreddit import get_askreddit_threads
from utils.console import print_markdown, print_step
from video_creation.background import download_background, chop_background_video
from video_creation.final_video import make_final_video
from video_creation.screenshot_downloader import download_screenshots_of_reddit_posts
from video_creation.voices import save_text_to_mp3

print_markdown(
    "### Thanks for using this tool! 😊 [Feel free to contribute to this project on GitHub!]("
    "https://lewismenelaws.com). If you have any questions, feel free to reach out to me on "
    "Twitter or submit a GitHub issue. "
)


def test_voice():
    print_step("Saving Text to MP3 files 🎶")
    music_len = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    # tts = gTTS(text=reddit_obj["thread_title"], lang="en", slow=False, tld="com")
    # tts.save(f"assets/mp3/title.mp3")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 125)
    file_path = f"assets/mp3/title.wav"
    engine.save_to_file("Why are men always paid more than woman even if the job is very much a "
                        "woman specific, like a nurse", file_path)

    engine.runAndWait()
    engine.stop()
    time.sleep(1)

    import soundfile as sf
    f = sf.SoundFile(file_path)
    print('samples = {}'.format(f.frames))
    print('sample rate = {}'.format(f.samplerate))
    print('seconds = {}'.format(f.frames / f.samplerate))

    file_exists = Path(file_path).exists()
    is_file = Path(file_path).is_file()

    # music_len += MP3(file_path).info.length
    print(f"The length of the music file is {music_len}")


# def test_method():
#     import pyttsx3
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     for voice in voices:
#         engine.setProperty('voice', voice.id)
#         engine.save_to_file('Hello World' , 'test.mp3')
#
#         print(voice.id)
#         engine.say('The quick brown fox jumped over the lazy dog.')
#     engine.runAndWait()


time.sleep(3)
# test_method()
# test_voice()
#
reddit_object = get_askreddit_threads()
length, number_of_comments = save_text_to_mp3(reddit_object)
download_screenshots_of_reddit_posts(reddit_object, number_of_comments)
download_background()
chop_background_video(length)
final_video = make_final_video(number_of_comments)
