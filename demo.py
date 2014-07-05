from requests import post, put, get, delete
from random import randrange


HOST = 'http://localhost:5000'
VERSION = 'v1'


def abs_url(part):
    return '/'.join([HOST, VERSION, part])


def new_game():
    """
    Create a new game using only requests
    """
    # delete any games currently in the system (not really neccessary)
    games = get(abs_url('games')).json()
    for game in games:
        delete(abs_url('games/{}'.format(game['id'])))

    return post(abs_url('games'), data={'players': ['Joe Johnson', 'James Anderson']}).json()


def send_roll(game, player, pins):
    """
    Send a new roll to the API server
    """
    return put(
        abs_url("games/{}/roll".format(game['id'])),
        data={'player_id': player['id'], 'pins': pins}).json()


def turn(game, player, frame, force_pins=None):
    """
    Simulate a players turn
    """
    rolls = []
    remainder = 10  # so we get a range of 0 - 10
    for turn in range(2):
        pins = force_pins if force_pins else randrange(remainder + 1)
        rolls.append(pins)
        send_roll(game, player, pins)
        remainder -= pins
        if pins == 10:  # strike
            break

    # if we get a strike on first shot
    # we have to roll two more times...
    if frame == 10 and rolls[0] == 10:
        pins = force_pins if force_pins else randrange(remainder + 1)
        send_roll(game, player, pins)

        pins = force_pins if force_pins else randrange(remainder + 1)
        send_roll(game, player, pins)


def print_scores(game):
    """
    Print out the scores for all the players in the game
    """
    print "score..."
    game = get(abs_url('games/{}'.format(game['id']))).json()
    players = game['players']

    fmt = "%-30s "
    for player in players:
        fmt += "%-20s "
    names = [p['name'] for p in players]
    print fmt % tuple([' '] + names)

    for frame in range(10):
        scores = []
        for player in players:
            scores.append(player['frames'][frame]['score'])

        print fmt % tuple(['Frame %d' % (frame + 1)] + scores)


if __name__ == '__main__':
    game = new_game()
    for player in game['players']:
        for frame in range(10):
            turn(game, player, frame + 1)

    print_scores(game)
