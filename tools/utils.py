import re
import time
import json
from urllib.parse import unquote
from html import unescape


def standard_json_str(json_str):
    """
    去除json字符串首尾杂质
    :param json_str:
    :return:
    """
    if json_str.startswith('{'):
        if json_str.endswith('}'):
            result = json_str
        elif '}' in json_str:
            result = json_str[: json_str.rfind('}') + 1]
        else:
            return False
    else:
        result = json_str[json_str.find('{'): json_str.rfind('}') + 1]
    while True:
        last_open = result.rfind('{')
        if last_open > result.rfind('}', 0, -1) and last_open > 0:
            result = result[: result.rfind('}', 0, -1) + 1]
        else:
            break
    return result


def extract_media(html_str):
    """
    提取html字符串中的媒体（图片和视频）信息
    :param content:
    :return:
    """
    media = dict(
        photos=[],
        videos=[]
    )
    if not html_str or not isinstance(html_str, str):
        return media

    content = unescape(html_str)
    img_tags = re.findall(r'<img .+?>', str(content), re.IGNORECASE)
    video_tags = re.findall(r'<video .+?>', str(content), re.IGNORECASE)

    for tag in img_tags:
        match_url = re.search(r'(src=\"|\')(.*?)\"|\'', tag, re.IGNORECASE)
        match_width = re.search(r'width=\'?\"?(\d+)', tag, re.IGNORECASE)
        match_height = re.search(r'height=\'?\"?(\d+)', tag, re.IGNORECASE)
        if match_url is None:
            continue
        else:
            url = match_url.group(2)

        width = match_width.group(1) if match_width else 0
        height = match_height.group(1) if match_height else 0

        photo = dict(
            html=tag,
            url=unquote(url),
            width=int(width),
            height=int(height),
        )
        media['photos'].append(photo)

    for tag in video_tags:
        match_url = re.search(r'(src=\"|\')(.*?)\"|\'', tag, re.IGNORECASE)
        match_width = re.search(r'width=\'?\"?(\d+)', tag, re.IGNORECASE)
        match_height = re.search(r'height=\'?\"?(\d+)', tag, re.IGNORECASE)
        match_size = re.search(r'size=\'?\"?(\d+)', tag, re.IGNORECASE)
        match_duration = re.search(r'duration=\'?\"?(\d+)', tag, re.IGNORECASE)
        match_definition = re.search(r'definition=\'?\"?(\d+)', tag, re.IGNORECASE)
        match_cover_photo = re.search(r'cover_photo=\'?\"?(\d+)', tag, re.IGNORECASE)
        if match_url is None:
            continue

        width = match_width.group(1) if match_width else 0
        height = match_height.group(1) if match_height else 0
        size = match_size.group(1) if match_size else 0
        duration = match_duration.group(1) if match_duration else 0
        definition = match_definition.group(1) if match_definition else ''
        cover_photo = match_cover_photo.group(1) if match_cover_photo else ''

        url = match_url.group(2)
        video = dict(
            html=tag,
            url=unquote(url),
            width=int(width),
            height=int(height),
            size=int(size),
            duration=int(duration),
            definition=definition,
            cover_photo=cover_photo,
        )
        media['videos'].append(video)

    return media


def process_time_str(time_str, to_timestamp=False):
    """
    将常见的时间格式转化为格林威治时间
    :param time_str:
    :param to_timestamp:
    :return:
    """
    year = time.strftime('%Y', time.localtime(time.time()))
    month = time.strftime('%m', time.localtime(time.time()))
    if isinstance(time_str, int):
        timestamp = time_str
    elif isinstance(time_str, float):
        timestamp = int(time_str)
    elif time_str.isdigit() and len(time_str) == 10:
        timestamp = int(time_str)
    elif re.search(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', time_str):
        time_str = re.search(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', time_str).group()
        timestamp = int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S')))
    elif re.search(r'\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', time_str):
        time_str = year[2:] + '-' + re.search(r'\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', time_str).group()
        timestamp = int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S')))
    elif re.search(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', time_str):
        year = year if time_str.split('-')[0] <= month else str(int(year) - 1)
        time_str = year + '-' + re.search(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', time_str).group()
        timestamp = int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S')))
    elif re.search(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}', time_str):
        time_str = re.search(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}', time_str).group()
        timestamp = int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M')))
    elif re.search(r'\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}', time_str):
        time_str = year[2:] + '-' + re.search(r'\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}', time_str).group()
        timestamp = int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M')))
    elif re.search(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}', time_str):
        year = year if time_str.split('-')[0] <= month else str(int(year) - 1)
        time_str = year + '-' + re.search(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}', time_str).group()
        timestamp = int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M')))
    else:
        timestamp = None

    if to_timestamp:
        return timestamp
    else:
        gmt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        return gmt


if __name__ == '__main__':
    s = '1602389662'
    print(process_time_str(s))