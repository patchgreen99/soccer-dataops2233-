import numpy as np
from venom import logger
from typing import List, Tuple, Dict, Any


class Possession:
    """
    Keeps track of the possession of the ball
    """

    def __init__(self):
        self.log = logger.get_or_create("possession", "INFO")
        self.possessing_player: Dict[str, Any] = {}
        self.possessing_player_by_ts: Dict[int, Dict[str, Any]] = {}
        self._possession_change_counter: int = 0
        self._possession_change_threshold: int = 7
        self._distance_possession_threshold: int = 2  # meter
        self._ball_speed_possession_threshold: int = 15  # Below 15 kmh counts as possession
        self.time_since_update: int = 0

    def update(
        self,
        utc_to_export: int,
        ball_track: Dict[int, Any],
        players_at_utc_to_export: Dict[str, List[Dict[str, Any]]],
        **kwargs,
    ) -> None:
        """update information and process data for utc_to_export.

        Args:
            utc_to_export (int): utc_to_export for data
            ball (Dict[str, Any]): ball position and speed
            players (List[Dict[str, Dict[str, Any]]]): players position and speed
        """

        ball_position, ball_speed = (
            ball_track.get(utc_to_export, {}).get("position", None),
            ball_track.get(utc_to_export, {}).get("speed", None),
        )

        players = [
            {**player, "team": team}
            for team, team_players in players_at_utc_to_export.items()
            for player in team_players
            if self._valid_player(team, player)
        ]

        if (
            ball_position is None
            or not len(players)
            or ball_speed is None
            or ball_speed > self._ball_speed_possession_threshold
        ):
            if self.time_since_update > self._possession_change_threshold:
                self.possessing_player = {}
                self._possession_change_counter = 0

            self.time_since_update += 1
        elif ball_speed < self._ball_speed_possession_threshold:
            closest_player, distance = self.closest_player_to_ball(players, ball_position)
            same_player = closest_player["track_id"] == self.possessing_player.get("track_id", -1)
            same_team = closest_player["team"] == self.possessing_player.get("team", None)
            if same_player and distance < self._distance_possession_threshold * 2:
                self._possession_change_counter = 0
            else:
                self._possession_change_counter += 1

            if self._possession_change_counter > self._possession_change_threshold:
                # Same team change (pass)
                if distance < self._distance_possession_threshold:
                    if (
                        same_team
                        or self.possessing_player.get("team", None) is None
                        or self._possession_change_counter > self._possession_change_threshold * 2
                    ):
                        self.possessing_player = closest_player
                        self._possession_change_counter = 0
                # No possessing player
                else:
                    self.possessing_player = {}
                    self._possession_change_counter = 0
            self.time_since_update = 0
        self.possessing_player_by_ts[utc_to_export] = self.possessing_player.copy()

        # Update ball track with possession
        if utc_to_export in ball_track:
            ball_track[utc_to_export].update(self.export(utc_to_export))

    def closest_player_to_ball(
        self, players: List[Dict[str, Any]], ball_position: List[float]
    ) -> Tuple[Dict[str, Any], float]:
        """Find player closest to ball and the distance

        Args:
            players (List[Dict[str, Any]]): list of players
            ball_position (List[float]): ball position

        Returns:
            Tuple[Dict[str, Any], float]: closest player and distance
        """
        ball_position = ball_position[:2]  # Only valid 2 coordinates
        positions = np.array([p["position"] for p in players])
        distances = np.linalg.norm(positions - ball_position, axis=1)
        player_idx = np.argmin(distances)
        return players[player_idx], distances[player_idx]

    def _valid_player(self, team: str, player: Dict[str, Any]) -> bool:
        """Check if player is valid for possessing the ball (ie. not referee, ...)

        Args:
            team (str): team label (home_team|away_team|referee)
            player (Dict[str, Any]): player information

        Returns:
            bool: if player is valid
        """
        if team == "referees":
            return False
        if not player.get("position", False):
            return False
        return True

    def export(self, utc_time: int) -> Dict[str, Any]:
        """export possessing team and player for timestamp.

        Args:
            utc_time (int): timestamp to export

        Returns:
            Dict[str, Any]: possessing player and team
        """
        player: Dict[str, Any] = self.possessing_player_by_ts.get(utc_time, {})
        return {
            "jersey_number": player.get("jersey_number", -1),
            "track_id": player.get("track_id", None),
            "team": player.get("team", None),
        }



p = Possession()

with open('fullMatch.json', 'r') as f:
    for line in f:
        utc_time = int(json.loads(line)["FrameCount"]/25)
        dataMatch = json.loads(line)["FrameData"][0]
        p.update(
          utc_to_export = utc_time
          ball_track = {"speed": dataMatch["BallPosition"][0]["Speed"], "positions": [dataMatch["BallPosition"][0]["X"],dataMatch["BallPosition"][0]["Y"]]}
          players_at_utc_to_export = [{"jersey_number": p["JerseyNumber"],"team": p["Team"],"speed": p["Speed"], "positions": [p["X"],p["Y"]]} for p in dataMatch["PlayerPositions"]]
        )
        print(p.export(utc_time))


