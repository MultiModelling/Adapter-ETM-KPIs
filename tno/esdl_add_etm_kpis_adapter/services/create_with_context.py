import requests

from .etm_service import ETMService
class CreateWithContextService(ETMService):
    ENDPOINT = 'create_with_context'

    def run(self, input_esdl_start, input_esdl_end):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'scenario_id': self.data.etm_config.scenario_ID,
            "energy_system_start_situation": input_esdl_start,
            "energy_system_end_situation": input_esdl_end,
        }
        server = self.data.etm_config.server
        return self._handle_response(requests.post(self.url(server), headers=headers, data=data))

    def _format_response(self, response):
        return response.json()['scenario_id']
