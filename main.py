from colorama import Fore, init
from bs4 import BeautifulSoup
import colorama
import requests
import argparse
import sys
import re

class bing_parser():
    def __init__(self, file, pages):
        self.file = file
        self.pages = pages

    def search(self):
        blocked = re.compile(r"\bmicrosoft|bing|wikipedia\b", flags=re.I | re.X)
        with open(self.file, "r") as file:
            content = file.readlines()
        content = [a.strip() for a in content] 
        for a in content:
            for i in range(0, self.pages):
                a = requests.get(f"https://www.bing.com/search?q={a}&first={self.pages}1", headers={"User-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})
                soup = BeautifulSoup(a.content, 'html.parser')
                items = soup.select('a[href^="http"]')
                with open("urls.txt", "a+") as file:
                    for item in items:
                        real = item['href']
                        if re.match(blocked, real):
                            pass
                        else:
                            file.write(str(real).split("/")[2] + "\n")
                    sites = []
                    with open(file, "r") as file:
                        for i in file.readlines():
                            sites.append(i.strip())
                        file.close()
                    remove = list(dict.fromkeys(sites))
                    with open("dupliremove.txt", "a+") as file:
                        for i in remove:
                            file.write(i + "\n")
                        file.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='file', action='store_true', help="usage: python3 main.py --file [keywords.txt] --pages [5]")
    parser.add_argument('-p', '--pages', dest='pages')
    args = parser.parse_args()

    if args.file:
        parser = bing_parser(args.file, args.pages)
        parser.search()

    if len(sys.argv) >= 2:
        pass
    else:
        print(f"{Fore.RED}Do -h or --help")

if __name__ == "__main__":
    main()
