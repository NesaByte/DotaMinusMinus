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
usr = ""
user = ""
username = ""

def getplayer(player):
    # Set the URL for user
    url_matches = "https://www.dotabuff.com/players/" + player + "/matches"

    # Connect to the URL. User agent is to prevent the browser to give the 429 response (too many requests)
    response_matches = requests.get(url_matches, headers={'User-agent': 'your bot 0.1'})

    # Parse entire html into a string
    soup_matches = BeautifulSoup(response_matches.text, 'html.parser')

    username = soup_matches.find("title")
    usr = str(username).replace(" - Matches - DOTABUFF - Dota 2 Stats</title>", "")
    user = usr.replace("<title>", "")
    print("* * * Retrieving data from: " + str(user) + " (" + player + ") * * *")

    match = soup_matches.findAll("td", class_='cell-icon')
    if len(match) > 0:

        # set url to find hero winrate percentage
        url_heroes = "https://www.dotabuff.com/players/" + player + "/heroes"

        # connect to usrl_matches
        response_heroes = requests.get(url_heroes, headers={'User-agent': 'your bot 0.1'})

        # Parse entire html into a string
        soup_heroes = BeautifulSoup(response_heroes.text, 'html.parser')

        for game in match:
            value = game.find("a", href=True)['href']
            newvalue = value.replace("/heroes/", "")
            temp.append(newvalue)
        count = Counter(temp)
        cc = sorted(count.items(), key=lambda item: item[1], reverse=True)
        print("Most played heroes from last 50games:")
        for k, v in cc:
            if v > 2:
                print("    " + str(v) + " " + k)
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