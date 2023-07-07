import requests

from .etm_service import ETMService
class ExportService(ETMService):
    ENDPOINT = 'export'

    def run(self, input_esdl):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'scenario_id': self.data.etm_config.scenario_ID,
            "energy_system": input_esdl
        }
        server = self.data.etm_config.server
        return self._handle_response(requests.post(self.url(server), headers=headers, data=data))

    def _format_response(self, response):
        return response.json()['energy_system']
