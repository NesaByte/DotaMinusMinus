"""
    Script used to retrieve player stats from DotaBuff website.
    Created: Jan 18, 2021.
"""
import argparse  # parsing command line arguments
import sys  # command line arguments
import requests  # url validating
from bs4 import BeautifulSoup
from collections import Counter

temp = []


def getplayer(player):
    print("Retrieving data from: " + player)

    # Set the URL for user
    url = "https://www.dotabuff.com/players/" + player + "/matches"

    # Connect to the URL. User agent is to prevent the browser to give the 429 response (too many requests)
    response = requests.get(url, headers={'User-agent': 'your bot 0.1'})

    soup = BeautifulSoup(response.text, 'html.parser')
    match = soup.findAll("td", class_='cell-icon')
    if len(match) > 0:
        for game in match:
            value = game.find("a", href=True)['href']
            newvalue = value.replace("/heroes/", "")
            temp.append(newvalue)
        count = Counter(temp)
        cc = sorted(count.items(), key=lambda item: item[1], reverse=True)
        for k, v in cc:
            if v > 1:
                print(v, k)
    else:
        print("Player " + player + " does not exist.")


def version():
    print("DotaMinusMinus Version 0.1")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=" ~ Welcome to DotaMinusMinus! ~",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-v', '--version', help="display installed version", action="store_true")
    parser.add_argument('-f', '--find', help="display player")

    args = parser.parse_args()

    if args.version:
        version()
    elif args.find:
        getplayer(args.find)
    else:
        parser.print_help(sys.stderr)

    sys.exit(1)