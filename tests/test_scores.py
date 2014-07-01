from .base_test import BaseTest
from random import randrange


class ScoringTest(BaseTest):
    def _add_game(self):
        response = self.client.post("/v1/games", data={'players': ['g1-player1', 'g1-player2', 'g1-player3']})
        self.assert200(response)
        return response.json

    def _get_scores(self, game):
        response = self.client.get("/v1/games/{}".format(game['id']))
        self.assert200(response)
        return response.json

    def _send_roll(self, game, player, pins):
        response = self.client.put("/v1/games/{}/roll".format(game['id']), data={'player_id': player['id'], 'pins': pins})
        self.assert200(response)
        return response.json

    def _play_frame(self, game, player, frame_number=1, force_pins=None):
        rolls = []
        remainder = 10  # so we get a range of 0 - 10
        for turn in range(2):
            pins = force_pins if force_pins else randrange(remainder + 1)
            rolls.append(pins)
            self._send_roll(game, player, pins)
            remainder -= pins
            if pins == 10:  # strike
                break

        # if we get a strike on first shot
        # we have to roll two more times...
        if frame_number == 10 and rolls[0] == 10:
            pins = force_pins if force_pins else randrange(remainder + 1)
            rolls.append(pins)
            self._send_roll(game, player, pins)

            pins = force_pins if force_pins else randrange(remainder + 1)
            rolls.append(pins)
            self._send_roll(game, player, pins)

        print "FRAME[{}] Player {} Rolled {}".format(frame_number, player['name'], str(rolls))

    def test_add_score(self):
        game = self._add_game()

        players = game['players']

        for player in players:
            self._play_frame(game, player)

    def test_add_full_scores(self):
        game = self._add_game()
        players = game['players']

        for frame in range(10):
            for player in players:
                self._play_frame(game, player, frame+1)

    def test_add_all_strikes(self):
        game = self._add_game()
        players = game['players']

        for frame in range(10):
            for player in players:
                self._play_frame(game, player, frame+1, force_pins=10)

        scored_game = self._get_scores(game)
        for player in scored_game['players']:
            assert player['frames'][-1]['score'] == 300
