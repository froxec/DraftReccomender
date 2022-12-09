import cassiopeia as cass
from parameters import match_features_names
## TODO filter for remakes, use AI for role recognition

def display_player_info(player_name, region):
    player = cass.Summoner(name=player_name, region=region)
    print("{name}  is a level {level} summoner on the {region} server".format(name=player.name,
                                                                              level=player.level,
                                                                              region=player.region))
    great_with = player.champion_masteries.filter(lambda cm: cm.level >= 6)
    print("{name} is good with:".format(name=player.name))
    print([cm.champion.name for cm in great_with])

def get_match_participants_features(match):
    participants_features = {}
    for i, participant in enumerate(match.participants):
        key = "User" + str(i)
        participants_features[key] =  {feature_name: participant.stats.__getattribute__(feature_name) for feature_name in match_features_names}
    return participants_features

def get_player_history(player_name, region):
    player = cass.Summoner(name=player_name, region=region)
    return player.match_history

def getAPI_key():
    file = open("API_key.txt")
    return file.read()
cass.set_riot_api_key("RGAPI-dc1b2169-925a-4b22-99eb-4ea6b6e2d8dd")

player_history = get_player_history("MDP Froxec", "EUW")
match = player_history[0]
print(get_match_participants_features(match)['User4'])
