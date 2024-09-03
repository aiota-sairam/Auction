import json
from firebase_admin import credentials, initialize_app, db

cred_obj = credentials.Certificate(r"auction_admin-main\app\auction-cde8d-firebase-adminsdk-z0lr1-a55fcecad6.json")
app = initialize_app(cred_obj, {
    'databaseURL': 'https://auction-cde8d-default-rtdb.firebaseio.com/'
})

root_ref = db.reference()

with open(r'auction_admin-main\app\players.json', 'r') as json_file:
    players = json.load(json_file)

with open(r'auction_admin-main\app\pval.json', 'r') as json_file:
    pointdata = json.load(json_file)

def getplayername(code):
    print(players[0][code])
    return players[0][code]

def getplayerpoint(code):
    print(pointdata[0][code])
    return pointdata[0][code]

def soldat(team, code, amount):
    team_ref = root_ref.child(f'team{team}')
    if not team_ref.get():
        return "Team does not exist"

    teamdata = team_ref.get()
    if not teamdata:
        return "Error fetching team data"

    prev_balance = teamdata.get('balance', 0)
    if prev_balance < amount:
        return "Insufficient balance"

    new_balance = prev_balance - amount
    teamdata['balance'] = new_balance

    if 'players' not in teamdata:
        teamdata['players'] = []
    playertemp = [getplayername(code), amount]
    teamdata['players'].append(playertemp)

    with open(r"auction_admin-main\app\points.json", 'r+') as pointchange:
        try:
            points = json.load(pointchange)
        except json.JSONDecodeError:
            return "Error decoding points data"
        player_points = getplayerpoint(code)
        if player_points is None:
            return "Player points not found"
        points[0][f"team{team}"] += player_points
        pointchange.seek(0)
        json.dump(points, pointchange, indent=4)

    teamdata[code[:2].lower()] += 1

    try:
        team_ref.set(teamdata)
    except Exception as e:
        return f"Error updating team data: {e}"

    return "Success"

while 1:
    team = input("\nEnter Team: ").strip()
    code = input("Enter Code: ").strip()
    amt = input("Enter Amt: ").strip()
    print()
    print(soldat(team,code.upper(),int(amt)))