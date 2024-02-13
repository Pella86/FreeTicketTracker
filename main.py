# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 11:55:07 2024

@author: maurop
"""


# needed to do the REST API queries
import requests

# =============================================================================
# Get the API KEY from
# https://developer.riotgames.com/ -> dashboard
# =============================================================================

# open the token from a separate file so it doesn't go in a public repository
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

# Store the possible options for the challenge level
levelEnum = {"MASTER": "MASTER",
             "GRANDMASTER" : "GRANDMASTER",
             "CHALLENGER" : "CHALLENGER"}

# there are possible servers to chose from
serverOriginEnum = {"EUW1": "euw1",
                    "BR1":"br1",
                    "EUN1":"eun1"
                    #...
                    }


# get the challenge id from the config query, and searcing the appropriate
# challenge, could be done automatically
challengeId = 101205

# set the level for the challenge
level = levelEnum["CHALLENGER"]

server_origin = serverOriginEnum["EUW1"]

# build the query url
riot_api_url = f"https://{server_origin}.api.riotgames.com"

api_section = f"/lol/challenges/v1/challenges/{challengeId}/leaderboards/by-level/{level}"

query_url = riot_api_url + api_section

print(f"Getting the leaderboard for the challenge {challengeId} at the level of {level} from the server {server_origin}")
print(query_url)

response = requests.get(query_url, headers=header)


# =============================================================================
# Elaborate the response
# =============================================================================

regionEnum = {"EUROPE":"europe",
              "AMERICAS":"americas",
              "ASIA":"asia",
              "ESPORTS":"esports"}


# 200 code means that the query was successful
if response.status_code == 200:
    
    # response format is an array of {'position': 1, 'puuid': 'r2OUJcdF5VtxQK4odyPsa_vAjx8ELJuDJMKn8rj0yfe2kgGJdqQVGdUmL_aL8qX5bzd8oWLOPQ7waw', 'value': 2417}
    leader_board = response.json()
    
    # show first x players
    n_players_shown = 30
    
    for line in  leader_board[:n_players_shown]:
        # for each player show the position, summoner name and the value
        
        # get the puuid from the table
        puuid = line["puuid"]
        
        #select the region
        region = regionEnum["EUROPE"]
        
        # build the url of the section for the accounts
        base_url = f"https://{region}.api.riotgames.com"
        api_section = f"/riot/account/v1/accounts/by-puuid/{puuid}"
        query_url = base_url + api_section
        
        # request the url
        response = requests.get(query_url, headers=header)
        
        if response.status_code == 200:
            
            # Response format
            #{"puuid": "cj4L_OlZ6ODqjyMAHXqvuDe7PPwrmB5AbiVjEgMm1EGOgUa0HjHEzjULDJoUo_eok6hP5_T9nj91nA", "gameName": "Suuyaa", "tagLine": "1337"}
            
            player = response.json()
            
            # get the name and the tag 
            gameName = player.get("gameName")
            tagLine = player.get("tagLine")
            
            # fuse them
            summonerName = f"{gameName}#{tagLine}"
            
            # show the 
            position = str(line["position"])
            value = str(line["value"])
            
            beauty_line = f"{position} {summonerName} {value}" 
            
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





