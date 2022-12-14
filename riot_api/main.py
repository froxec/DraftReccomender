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
        participants_features[key] = {feature_name: participant.stats.__getattribute__(feature_name) for feature_name in
                                      match_features_names}
    return participants_features


def get_player_history(player_name, region):
    player = cass.Summoner(name=player_name, region=region)
    return player.match_history


def current_match_to_history_index(current_match, match_history):
    for match_num, match in enumerate(match_history):
        if current_match.id == match.id:
            return match_num


def create_data_array(player_records):
    # input -> player records
    # output -> array of shape (Number of users, number_of_features, max_history_lenght)
    NotImplementedError


def construct_matches_dataset():
    ids_in_dataset = []
    players_in_dataset = {}
    players_ids = []
    matches = {}
    challanger = cass.get_challenger_league(queue=cass.data.Queue("RANKED_SOLO_5x5"), region="EUW")
    for entry in challanger.entries[0:1]:
        player = entry.summoner
        player_match_history = player.match_history
        for i, match in enumerate(player_match_history[0:2]):
            if match.id in ids_in_dataset:
                continue
            else:
                match_index = len(matches)
                matches[str(match_index)] = {}
                for user_num, participant in enumerate(match.participants):
                    summoner = participant.summoner
                    if summoner.puuid not in players_ids:
                        summoner_match_history = summoner.match_history
                        # print("Adding summoner {} to dataset".format(summoner.name))
                        # print("Match {curren  t_match} is {match_num} in {summ_name} history".format(current_match=match.id,
                        #                                                                            match_num=current_match_to_history_index(match, summoner.match_history),
                        #                                                                            summ_name=summoner.name))
                        players_ids.append(summoner.puuid)
                        players_in_dataset[summoner.puuid] = {"id": len(players_in_dataset),
                                                              "match_history": [match for match in
                                                                                summoner_match_history]}
                    matches[str(match_index)]["User" + str(user_num)] = (players_in_dataset[summoner.puuid]["id"],
                                                                         current_match_to_history_index(match,
                                                                                                        players_in_dataset[
                                                                                                            summoner.puuid][
                                                                                                            "match_history"]))
                    print('matches', matches)
                # matches[str(match_index)] = {"id" : match.id, "match": match}
                ids_in_dataset.append(match.id)
                print('ids_in_dataset', ids_in_dataset)
    return matches


def getAPI_key():
    file = open("API_key.txt")
    return file.read()


cass.set_riot_api_key("RGAPI-3fe686f2-d295-41d2-b0fb-97f13a95f0f4")

# player_history = get_player_history("MDP Froxec", "EUW")
# match = player_history[0]
# print(get_match_participants_features(match)['User4'])
matches_dataset = construct_matches_dataset()
print(matches_dataset)
