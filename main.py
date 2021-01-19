
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os
from msvcrt import getch


def get_thread_name(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    name = soup.findAll("span", {"class": "subject"})[1].get_text()

    return name


def get_files(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    links = soup.findAll("div", {"class": "fileText"})

    files = []
    for link in links:
        filename = link.find("a").get_text()
        url = "https:" + link.find("a")["href"]
        files.append([filename, url])

    return files


def download(files, url):
    board = url.split(".org/")[1].split("/")[0]
    thread = url.split("/thread/")[1]
    
    get_thread_name(url)

    # Create folder
    folder = "threads/" + board + " - " + thread + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Download images
    for file in files:
        file_name = file[0]
        file_url = file[1]
        
        r = requests.get(file_url)
        open(folder + file_name, "wb").write(r.content)
    
    # Create file with info
    with open(folder + "info.txt", "w") as f:
        f.write(f"Board: /{board}/ \n")
        f.write(f"Thread Subject: {get_thread_name(url)} \n")

        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        f.write(f"Downloaded on: {date} \n")

        f.write(f"Images downloaded: {len(files)} ")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Thread URL: ")

    files = get_files(url)
    print(f"Downloading {len(files)} images/videos")
    download(files, url)

    print("Done!")
    print("Press any key to exit")
    getch()
