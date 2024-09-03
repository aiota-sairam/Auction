def soldat(team, code, amount):
    team_ref = root_ref.child(f'team{team}')
    teamdata = team_ref.get()

    prev_balance = teamdata['balance']

    if prev_balance < amount:
        return "Balance Error"

    else:

        new_balance = prev_balance - amount
        teamdata['balance'] = new_balance

        if not teamdata.get('players'):
            teamdata['players'] = []
        playertemp = []
        print("\nPlayer:",getplayername(code))    
        playertemp.append(getplayername(code))
        playertemp.append(amount)
        teamdata['players'].append(playertemp)
        with open("points.json",'r+') as pointchange:
            points = json.load(pointchange)
            print("Point:",getplayerpoint(code))
            points[0][f"team{team}"] += getplayerpoint(code)
            pointchange.seek(0)
            json.dump(points, pointchange, indent=4)
        teamdata[code[0:2].lower()] += 1
        team_ref.set(teamdata)
        return "Success"