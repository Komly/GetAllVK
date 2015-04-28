#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os

API_URL = 'https://api.vk.com/method/wall.get?owner_id=-%s&extended=1&offset=%s&count=%s&v=5.30'

if len(sys.argv) < 2:
    print("Usage %s gid" % sys.argv[0])
    sys.exit(0)

gid = sys.argv[1]

def download_url(url, path):
    data = requests.get(url)
    with open(path, 'w') as f:
        f.write(data.content)    

def get_max_photo_url(photo):
    fields = ['photo_2560', 'photo_1280', 'photo_807', 'photo_604', 'photo_130', 'photo_75']
    for field in fields:
        url = photo.get(field, None)
        if url:
            return url
    return None

def get_all_posts(gid):
    offset = 0
    chunk = 100
    count = json.loads(requests.get(API_URL % (gid, '0', '1')).text)['response']['count']
    result = []
    while offset <= count:
        url = API_URL % (gid, str(offset), str(chunk))
        posts = json.loads(requests.get(url).text)['response']['items']
        result.extend(posts)
        print('Received %d posts' % len(posts))
        offset += chunk
    return result
        

posts = get_all_posts(gid)

path = os.path.join(os.getcwd(), 'img', gid)
try:
    os.makedirs(path)
except:
    pass

for post in posts:
    atts = post.get('attachments', None)
    if not atts:
        continue
    for att in atts:
        url = None
        if att['type'] == 'photo':
            url = get_max_photo_url(att['photo'])
        elif att['type'] == 'posted_photo':
            url = get_max_photo_url(att['posted_photo'])
        if not url:
            continue
        name = url.split('/')[-1]
        file_name = os.path.join(path, name)
        download_url(url, file_name)
        print(url)







