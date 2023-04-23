"""
AutoImageDownloader (https://github.com/nbwzx/AutoImageDownloader)
Copyright (c) 2023 Zixing Wang <zixingwang.cn@gmail.com>
Licensed under MIT (https://github.com/nbwzx/AutoImageDownloader/blob/main/LICENSE)
"""
import json
import os
import time

import requests
from bs4 import BeautifulSoup


def download(search_term: str, num_images: int = 10, image_size: str = "500x500") -> None:
    """
    Downloads images from Google Images search results for the given search term.

    Args:
        search_term (str): The search term to use for the Google Images search.
        num_images (int, optional): The number of images to download (default is 10).
        image_size (str, optional): The size of images to search for in the format "widthxheight" 
            (default is "500x500").

    Returns:
        None
    """
    # Set the URL of the Google Images search results page
    url = f"https://www.google.com/search?q={search_term}+imagesize:{image_size}&tbm=isch"

    # Set the headers for the HTTP request to mimic a web browser
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Send an HTTP request to the Google Images search results page and parse the response with BeautifulSoup
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the image URLs in the search results and download the first `num_images` images
    image_urls = []
    for img in soup.find_all("img", class_="rg_i"):
        if len(image_urls) == num_images:
            break
        try:
            url = img["data-src"]
            response = requests.get(url, headers=headers)
            file_path = os.path.join(
                "images", f"{search_term}_{len(image_urls)}.jpg")
            with open(file_path, "wb") as f:
                f.write(response.content)
            image_urls.append(url)
        except:
            pass

        # Wait for 0.1 second to avoid being detected as a bot
        time.sleep(0.1)


if __name__ == "__main__":
    # Creates the "images" directory if it doesn't exist
    if not os.path.exists("images"):
        os.mkdir("images")

    with open(('Yifan Wang.json'), 'r', encoding='utf8') as filef:
        letter_pairs = json.load(filef)
    for index in letter_pairs:
        download(letter_pairs[index][0])
