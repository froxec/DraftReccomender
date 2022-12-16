import csv
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


def get_match_features(match):
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


def get_challenger_300():
    return cass.get_challenger_league(queue=cass.data.Queue("RANKED_SOLO_5x5"), region="EUW")


class Players:
    def __init__(self):
        self.players_in_dataset = {}
        self.players_ids = []

    def add_players_to_player_ids(self, match_participants):
        for participant in match_participants:
            summoner = participant.summoner
            if summoner.puuid not in self.players_ids:
                self.players_ids.append(summoner.puuid)
                self.players_in_dataset[summoner.puuid] = {"id": len(self.players_in_dataset),
                                                           "match_history":
                                                               [match for match in summoner.match_history]}


class Matches:
    def __init__(self):
        self.matches = []
        self.ids_in_dataset = []
        self.match_id = -1

    def add_match(self, players, match):
        self.ids_in_dataset.append(match.id)
        match_arr = [match.id, int(match.start.timestamp())]
        for user_num, participant in enumerate(match.participants):
            puuid = participant.summoner.puuid
            user_id = players.players_in_dataset[puuid]['id']
            history_id = current_match_to_history_index(match, players.players_in_dataset[puuid]["match_history"])
            match_arr.append((user_id, history_id))
        self.match_id += 1  # Dla optymalizacji nie robie len() i self.matches mozna tez oprozniac
        self.matches.append(match_arr)

        return self.match_id

    def is_filter_match(self, match):
        is_in_dataset = match.id in self.ids_in_dataset
        is_remake = match.is_remake
        return is_remake or is_in_dataset


def data_csv_save(match_features, match_id):
    data = list(match_features.values())

    with open('data.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        print('data', data)
        writer.writerow([match_id] + data)
    print(f"------------> Saved {match_id}")


def data_csv_init():
    header = ['', 'User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8', 'User9', 'User10']

    with open('data.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)


def save_train(data):
    header = ['', 'match_id', 'time', 'User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8', 'User9',
              'User10']

    with open('train.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i, x in enumerate(data):
            print(x)
            writer.writerow([i] + x)


def construct_matches_dataset():
    players = Players()
    matches = Matches()
    data_csv_init()
    challenger = get_challenger_300()

    for entry in challenger.entries[0:1]:
        for i, match in enumerate(entry.summoner.match_history):
            if matches.is_filter_match(match):
                continue

            players.add_players_to_player_ids(match.participants)
            match_id = matches.add_match(players, match)
            match_features = get_match_features(match)
            data_csv_save(match_features, matches.match_id)
            save_train(matches.matches)  # To wstawiłem tutaj a nie na koniec, żeby w dowolnym momenice móc przerwać
    return players, matches


def main():
    cass.set_riot_api_key("RGAPI-778b2985-d816-414a-b097-32b206234bde")
    construct_matches_dataset()


if __name__ == "__main__":
    main()
