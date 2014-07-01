from .base_test import BaseTest
import json

from app import app, db
from app.models import Game


class GamesTest(BaseTest):
    def _check_game(self, game):
        print "-" * 80
        print game
        print "-" * 80
        # make sure we have three players in each game
        assert len(game['players']) == 3

        for player in game['players']:
            # make sure we have 10 frames for each player
            assert len(player['frames']) == 10

            # now make sure that each frame doesn't have any rolls or scores
            for frame in player['frames']:
                assert frame['score'] == 0
                assert frame['rolls'] == []
        return game

    def test_create_games(self):
        response = self.client.post("/v1/games", data={'players': ['g1-player1', 'g1-player2', 'g1-player3']})
        self.assert200(response)
        self._check_game(response.json)

        response = self.client.post("/v1/games", data={'players': ['g2-player1', 'g2-player2', 'g2-player3']})
        self.assert200(response)
        self._check_game(response.json)

        response = self.client.get("/v1/games")
        self.assert200(response)
        games = response.json

        # make sure we have two games
        assert len(games) == 2

        for index, game in enumerate(games):
            # now make sure the game we get back from /games is exactly the same
            # as what we get back when creating the games
            self._check_game(game)

    def test_bad_games(self):
        response = self.client.post("/v1/games")
        self.assert400(response)

        response = self.client.post("/v1/games/21")
        self.assert405(response)

        response = self.client.put("/v1/games")
        self.assert405(response)

        response = self.client.post("/v1/games", data={'players': []})
        self.assert400(response)
