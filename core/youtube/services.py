import os
from datetime import datetime

import scrapetube
from aiogram.types import FSInputFile
from pytube import YouTube

channels_list = [
    "https://www.youtube.com/@ITHelpers170",
    "https://www.youtube.com/@getatru",
]
video_list = {
    "https://www.youtube.com/@ITHelpers170": "",
    "https://www.youtube.com/@getatru": "",
}


def get_mp3_from_youtube(url: str) -> FSInputFile:
    """Скачивание mp3 файла по ссылке Youtube"""
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=".")
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    audio = FSInputFile(path=f"{new_file}")
    return audio


def delete_saved_mp3(path: str) -> None:
    """Удаление сохраненного mp3 файла"""
    if os.path.isfile(path):
        os.remove(path)
        print("success " + str(datetime.now().time()))
    else:
        print("File doesn't exists!")


# def check_update(channels_list: list):
#     """Проверка обновления в выбранных каналах"""
#     for channel in channels_list:
#         videos = scrapetube.get_channel(channel_url=channel, limit=1)
#         id_last_video = list(videos)[0]["videoId"]
#         if video_list[channel] != id_last_video:
#             video_list[channel] = id_last_video
#             return f"https://www.youtube.com/watch?v={video_list[channel]}"


def get_last_video(channel: list):
    """Проверка обновления в выбранных каналах"""
    channel = f"https://www.youtube.com/{channel}"
    videos = scrapetube.get_channel(channel_url=channel, limit=1)
    id_last_video = list(videos)[0]["videoId"]
    return id_last_video


def video_data(channel: str) -> dict:
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


# print(video_data("https://www.youtube.com/@getatru"))
