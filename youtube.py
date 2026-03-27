#!/usr/bin/env python3
# encoding: utf-8

import yt_dlp

def download_youtube_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = input("請輸入 YouTube 網址: ")
    download_youtube_video(video_url)


