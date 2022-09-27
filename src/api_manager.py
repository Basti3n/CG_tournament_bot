import logging
from dataclasses import dataclass, field
from typing import List

import requests

o_logger = logging.getLogger(__name__)


@dataclass
class ApiManager:
    s_base_url: str = field(init=False,
                            default='https://www.codingame.com/services/ClashOfCode/findClashReportInfoByHandle')

    def get_results(self, s_exercise_id: str) -> List[str]:

        l_body = [s_exercise_id]
        o_response = requests.post(self.s_base_url, json=l_body)
        if o_response.status_code == 200:
            dc_response = o_response.json()
            if dc_response.get('finished'):
                return [dc_player['codingamerNickname'] for dc_player in dc_response['players']]
        else:
            o_logger.error(f'Error while getting results for exercise {s_exercise_id}')
