import constants
import copy
PLAYERS = constants.PLAYERS
TEAMS = constants.TEAMS

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

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
    
    return balanced_teams
    
    
def cli(clean_balanced_teams):
    print("\nBASKETBALL TEAM STATS TOOL\n\n ----MENU----\n\n")
    print(f"Here are your choices:\n")
    choice = input("A) Display Team Stats\nB) Quit\n\nEnter an option: ")
    
    while choice.lower() not in 'ab':
        print(f"{Colors.RED}Choice must be either A or B\n{Colors.RESET}")
        choice = input("A) Display Team Stats\nB) Quit\n\nEnter an option: ")
    
    if choice.lower() == 'b':
        exit()

    print()
    i = ord('a')
    for team_name in [team['team_name'] for team in clean_balanced_teams]:
        print(f"{chr(i).upper()}: {team_name}")
        i+=1
        if i == 27:
            break
    print(i)
    team_choice = ord(input('\nEnter an option: \n').lower())
    choice_length = range(ord('a'), i)
    while team_choice not in choice_length:
        print(f"\n{Colors.RED}Must enter a listed option\n{Colors.RESET}")
        team_choice = ord(input('\nEnter an option: \n').lower())



if __name__ == "__main__":
    # print('hello world!')
    # print(clean_data(PLAYERS))
    # print(balance_teams(clean_data(PLAYERS), TEAMS))
    cli(balance_teams(clean_data(PLAYERS), TEAMS))