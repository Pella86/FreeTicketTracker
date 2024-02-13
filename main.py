# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 11:55:07 2024

@author: maurop
"""

import requests

# =============================================================================
# Get the API KEY from
# https://developer.riotgames.com/ -> dashboard
# =============================================================================


with open("./api_token/api_token.txt") as f:
    line = f.readline()
    _, part = line.split("=")
    api_key = part.strip()
    
# store information in the header
header = {
    "User-Agent": "Personal tracker",
    "Accept-Language": "en-GB,en;q=0.9,it-IT;q=0.8,it;q=0.7,en-US;q=0.6,de;q=0.5",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "*",
    "X-Riot-Token": api_key
}

# =============================================================================
# Query the leaderboard
# =============================================================================

# import enum
# levelEnum = enum.Enum("Level", ["MASTER", "GRANDMASTER", "CHALLENGER"])

# class Level:
#     MASTER = "MASTER"
#     GRANDMASTER = "GRANDMASTER"
#     CHALLENGER = "CHALLENGER"

levelEnum = {"MASTER": "MASTER",
         "GRANDMASTER" : "GRANDMASTER",
         "CHALLENGER" : "CHALLENGER"}


# get the challenge id
challengeId = 101205
level = levelEnum["CHALLENGER"]

# build the query url
riot_api_url = "https://euw1.api.riotgames.com"


api_section = f"/lol/challenges/v1/challenges/{challengeId}/leaderboards/by-level/{level}"


query_url = riot_api_url + api_section

print(query_url)

response = requests.get(query_url, headers=header)


# =============================================================================
# Elaborate the response
# =============================================================================

# 200 code means ok, 
if response.status_code == 200:
    print("Response OK")
    # response format is an array of {'position': 1, 'puuid': 'r2OUJcdF5VtxQK4odyPsa_vAjx8ELJuDJMKn8rj0yfe2kgGJdqQVGdUmL_aL8qX5bzd8oWLOPQ7waw', 'value': 2417}
    leader_board = response.json()
    
    # show first 50 players
    n_players_shown = 30
    
    for line in  leader_board[:n_players_shown]:
        # query the player summoner name from the puuid
        puuid = line["puuid"]
        
        base_url = "https://europe.api.riotgames.com"
        # build the url of the section for the accounts
        api_section = f"/riot/account/v1/accounts/by-puuid/{puuid}"
        
        query_url = base_url + api_section
        
        response = requests.get(query_url, headers=header)
        
        if response.status_code == 200:
            
            # Response format
            #{"puuid": "cj4L_OlZ6ODqjyMAHXqvuDe7PPwrmB5AbiVjEgMm1EGOgUa0HjHEzjULDJoUo_eok6hP5_T9nj91nA", "gameName": "Suuyaa", "tagLine": "1337"}
            
            player = response.json()
            
            gameName = player.get("gameName")
            tagLine = player.get("tagLine")
            
            summonerName = f"{gameName}#{tagLine}"
            
            beauty_line = str(line["position"]) + " " + summonerName + " " + str(line["value"])
            
            if "babalaas" in summonerName:
                print("--- " + beauty_line + " ---")
            else:
                print(beauty_line)
                
        else:
            print("Query failed")
            print(response)
            print(response.status_code)
            print(response.json())            


else:
    print("Query failed")
    print(response)
    print(response.status_code)
    print(response.json())





