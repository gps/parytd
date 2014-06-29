#!/usr/bin/env python

import argparse
import logging
import multiprocessing
import youtube_dl


log = logging.getLogger(__name__)


def get_ydl():
    ydl = youtube_dl.YoutubeDL()
    ydl.add_default_info_extractors()
    return ydl


def get_urls_to_download(url):
    ydl = get_ydl()
    urls_to_dl = []
    res = ydl.extract_info(url, download=False)
    if 'entries' in res:
        urls_to_dl.extend(res['entries'])
    else:
        urls_to_dl.append(url)

    return urls_to_dl


def download_url(url):
    ydl = get_ydl()
    res = ydl.extract_info(url)


def main():
    argparser = argparse.ArgumentParser('Downloads videos')
    argparser.add_argument('-v', '--videos', required=True, help='File containing video urls')
    argparser.add_argument('-c', '--concurrency', type=int, default=10, help='Number of videos to download at a time')
    args = argparser.parse_args()

    logging.basicConfig(level=logging.INFO)

    with open(args.videos) as fin:
        urls = [l.strip() for l in fin.readlines()]

    pool = multiprocessing.Pool(args.concurrency)
    results = pool.map(get_urls_to_download, urls)

    urls_to_dl = []
    for res in results:
        urls_to_dl.extend(res)

    pool.map(download_url, urls_to_dl)


if __name__ == '__main__':
    main()
