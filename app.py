import constants
import copy
PLAYERS = constants.PLAYERS
TEAMS = constants.TEAMS

# Define color codes for enhancing console text readability
class Colors:
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# Calculate the average of a list of numbers
def average(list):
    return sum(list) / len(list)


# Combine and format a 2D list of strings into a single comma-separated string
def combine_and_format_guardians(list):
    # Flatten the list of guardians and join with commas
    new_list = []
    for item in list:
        new_list.extend(item)
    return ', '.join(new_list)
    

# Clean and prepare player data from constants
def clean_data(players):
    # Use deepcopy to avoid modifying the original player data
    players_copy = copy.deepcopy(players)
    for player in players_copy:
        # Convert height to integer and experience to boolean
        player['height'] = int(player['height'].split()[0])
        player['experience'] = True if player['experience'] == 'YES' else False
        # Split guardians string into a list
        player['guardians'] = player['guardians'].split(' and ')
    return players_copy


# Balance players across teams
def balance_teams(players, teams):
    # separate inexperienced and experienced players to recruit from
    inexperienced_players = [player for player in players if not player['experience']]
    experienced_players = [player for player in players if player['experience']]
    
    # set limit for how many experienced players and total players a team can have
    num_players_team = len(players) // len(teams)
    num_experienced_team = len(experienced_players) // len(teams)
    
    # Initialize empty teams
    balanced_teams = [{'team_name': team, 'players': []} for team in teams]
    
    # Distribute experienced players
    for team in balanced_teams:
        while len([player for player in team['players'] if player['experience']]) < num_experienced_team:
            player = experienced_players.pop() if len(experienced_players) > 0 else None
            if player:
                team['players'].append(player)
     # Fill remaining slots with inexperienced players      
    for team in balanced_teams:
        while len(team['players']) < num_players_team:
            player = inexperienced_players.pop() if len(inexperienced_players) > 0 else None
            if player:
                team['players'].append(player)
    
    return balanced_teams
    
    
# Command Line Interface for the Basketball Team Stats tool
def cli(clean_balanced_teams):
    # Display main menu
    print("\nBASKETBALL TEAM STATS TOOL\n\n ----MENU----\n\n")
    print(f"Here are your choices:\n")
    choice = input("A) Display Team Stats\nB) Quit\n\nEnter an option: ")
    
    # Input validation for main menu
    while choice.lower() not in 'ab' or len(choice) < 1:
        print(f"\n{Colors.RED}Choice must be either A or B\n{Colors.RESET}")
        choice = input("A) Display Team Stats\nB) Quit\n\nEnter an option: ")
    
    # Exit if user chooses to quit
    if choice.lower() == 'b':
        exit()

    # Display team options for stats
    print()
    i = ord('A') # Start with ASCII value of 'A' for team labeling
    team_options = ''
    
    # Generate team options based on team names
    for team_name in [team['team_name'] for team in clean_balanced_teams]:
        team_options += f"{chr(i).upper()}: {team_name}\n" # Convert ASCII value back to character for labeling
        i+=1
        # Stop if all of alphabet is used.  (Would change if it was possible to have more than 26 pickable teams) 
        if i == ord('Z'):
            break
        
    print(team_options)

    # User input for team choice
    team_choice = input('Enter an option: ')
    choice_length = range(ord('A'), i)

    # Input validation for team selection
    while not team_choice or ord(team_choice[0].upper()) not in choice_length:
            print(f"\n{Colors.RED}Must enter a listed option\n{Colors.RESET}")
            print(team_options)
            team_choice = input('\nEnter an option: ')

    # Convert team choice to index
    team_choice = ord(team_choice[0].upper())
    # Convert user's choice from letter to index (e.g., 'A' -> 0, 'B' -> 1)
    team_index = team_choice - ord('A')

    # Display team stats
    print(f"""
Team: {clean_balanced_teams[team_index]['team_name']} Stats
--------------------
Total players: {len(clean_balanced_teams[team_index]['players'])}
Total experienced: {len([player for player in clean_balanced_teams[team_index]['players'] if player['experience']])}
Total inexperienced: {len([player for player in clean_balanced_teams[team_index]['players'] if not player['experience']])}
Average height: {average([player['height'] for player in clean_balanced_teams[team_index]['players']])}

Players on Team:
    {', '.join([player['name'] for player in clean_balanced_teams[team_index]['players']])}

Guardians:
    {combine_and_format_guardians([player['guardians'] for player in clean_balanced_teams[team_index]['players']])}\n""")

    input(f'Press ENTER to {Colors.CYAN}continue{Colors.RESET}...')
    cli(clean_balanced_teams)

if __name__ == "__main__":
    cli(balance_teams(clean_data(PLAYERS), TEAMS))