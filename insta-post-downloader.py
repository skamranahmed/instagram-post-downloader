import requests
from requests_html import HTML
from tqdm import tqdm
import re

POST_URL = input("Enter the url of the instagram post: \n")

#   matching the input url with the instagram's default post url pattern
url_pattern = re.compile(r'https?://(www\.)?instagram.com/p/\w+')
match = url_pattern.match(POST_URL.strip())

if match:
    chunk_size = 1024
    response = requests.get(POST_URL.strip())
    r_html = HTML(html = response.text)
    meta_tag = r_html.find('meta')
    no_of_meta_elements = len(meta_tag)

    if no_of_meta_elements > 25:
        download_url = meta_tag[24].attrs['content']
    else:
        download_url = meta_tag[10].attrs['content']

    #   if the download url is fetched
    download_url_pattern = re.compile(r'https?://instagram\.\w+')
    is_download_url = download_url_pattern.match(download_url)      # this returns either True or False

    if is_download_url:
        r = requests.get(download_url, stream=True)
        total_size = int(r.headers['Content-Length'])
        content_type = r.headers['Content-Type']

        filename = ''

        if content_type.startswith('image'):
            filename = str(input('Enter filename for the image (without extension): \n') + ".jpeg")
        elif content_type.startswith('video'):
            filename = str(input('Enter filename for the video (without extension): \n') + ".mp4")

        print("Downloading.....")

        with open(filename, "wb") as f:
            #   this piece of code is for the tqdm downloading bar
            for data in tqdm(iterable =r.iter_content(chunk_size = chunk_size), total = total_size/chunk_size, unit = 'KB'):
                f.write(data)

        print(f"Filename: {filename}\nDownload Completed!")

    #   if the download url is not fetched
    else:
        print("The post is of a private account.")

else:
    print("OOPS, there seems to be something wrong with the post url. Please check.")