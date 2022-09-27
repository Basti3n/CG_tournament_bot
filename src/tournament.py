from dataclasses import dataclass, field
from typing import List, Dict

from src.api_manager import ApiManager


@dataclass
class Tournament:
    b_is_running: bool = field(init=False, default=False)
    l_exercises: List[Dict[str, str]] = field(init=False, default_factory=list)
    o_api_manager: ApiManager = field(init=False, default=ApiManager())

    def start_tournament(self):
        self.b_is_running = True

    def end_tournament(self):
        self.b_is_running = False

    def add_exercise(self, s_exercise_url: str) -> str:
        s_exercise_id = s_exercise_url.split('/')[-1]
        self.l_exercises.append(
            {
                'exercise_id': s_exercise_id,
                'exercise_url': s_exercise_url
            }
        )
        return s_exercise_id

    def get_exercises(self) -> List[Dict[str, str]]:
        return self.l_exercises

    def get_current_score(self) -> List[str]:
        dc_players = {}
        for dc_exercise in self.l_exercises:
            l_exercise_result = self.o_api_manager.get_results(dc_exercise.get('exercise_id'))
            if l_exercise_result:
                dc_players_scores = self._calcul_points(l_exercise_result)
                for s_player_name, i_score in dc_players_scores.items():
                    dc_players[s_player_name] = dc_players.get(s_player_name, 0) + i_score

        dc_played_ordered = dict(sorted(dc_players.items(), key=lambda item: item[1], reverse=True))
        return [f'{s_player_name} : {i_score}' for s_player_name, i_score in dc_played_ordered.items()]

    @staticmethod
    def _calcul_points(l_exercise_result) -> Dict[str, int]:
        return {s_player_name: len(l_exercise_result) - i_score for i_score, s_player_name in
                enumerate(l_exercise_result)}
