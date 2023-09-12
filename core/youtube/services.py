import os
from datetime import datetime

import scrapetube
from aiogram.types import FSInputFile
from pytube import YouTube


def get_mp3_from_youtube(url: str) -> FSInputFile:
    """Download mp3 file from Youtube link"""
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=".")
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    audio = FSInputFile(path=f"{new_file}")
    return audio


def delete_saved_mp3(path: str) -> None:
    """Deleting a saved mp3 file"""
    if os.path.isfile(path):
        os.remove(path)
        print("success " + str(datetime.now().time()))
    else:
        print("File doesn't exists!")


def get_last_video(channel: list) -> str:
    """Getting the latest video on a channel"""
    channel = f"https://www.youtube.com/{channel}"
    videos = scrapetube.get_channel(channel_url=channel, limit=1)
    id_last_video = list(videos)[0]["videoId"]
    return id_last_video


def get_video_data(channel: str) -> dict:
    """Getting data from channel"""
    if channel.startswith("@"):
        channel = f"https://www.youtube.com/{channel}"
    data = {}
    videos = scrapetube.get_channel(channel_url=channel, limit=1)
    id_last_video = list(videos)[0]["videoId"]
    data["id_last_video"] = id_last_video
    full_name = f"https://www.youtube.com/watch?v={id_last_video}"
    channel_name = YouTube(full_name).author
    data["channel_name"] = channel_name
    for part in channel.split("/"):
        if part.startswith("@"):
            data["channel_id"] = part
    return data
