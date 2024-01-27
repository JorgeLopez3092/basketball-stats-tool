import constants
import copy
PLAYERS = constants.PLAYERS
TEAMS = constants.TEAMS

def clean_data(players):
    players_copy = copy.deepcopy(players)
    for player in players_copy:
        player['height'] = int(player['height'].split()[0])
        player['experience'] = True if player['experience'] == 'YES' else False
    return players_copy


def balance_teams(players, teams):
    # separate inexperienced and experienced players to recruit from
    inexperienced_players = [player for player in players if not player['experience']]
    experienced_players = [player for player in players if player['experience']]
    # print('INEXPERIENCED!', inexperienced_players)
    # print('Experienced', experienced_players)
    # set limit for how many experienced players and total players a team can have
    num_players_team = len(players) // len(teams)
    num_experienced_team = len(experienced_players) // len(teams)
    balanced_teams = []
    for team in teams:
        balanced_teams.append({ 'team_name': team, 'players': []})
    #distribute experienced players
    for team in balanced_teams:
        while len([player for player in team['players'] if player['experience']]) < num_experienced_team:
            player = experienced_players.pop() if len(experienced_players) > 0 else None
            if player:
                team['players'].append(player)
     # distribute inexperienced players and finish filling teams out       
    for team in balanced_teams:
        while len(team['players']) < num_players_team:
            player = inexperienced_players.pop() if len(inexperienced_players) > 0 else None
            if player:
                team['players'].append(player)
        print(len(team['players']))
    
    return balanced_teams
    
    
    




if __name__ == "__main__":
    # print('hello world!')
    # print(clean_data(PLAYERS))
    print(balance_teams(clean_data(PLAYERS), TEAMS))