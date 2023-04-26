import requests

from .etm_service import ETMService
class AddKPISService(ETMService):
    ENDPOINT = 'kpis'

    def run(self, input_esdl):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'scenario_id': self.data.etm_config.scenario_ID,
            "area_name": self.data.action_config.KPI_area,
            "energy_system": input_esdl
        }
        server = self.data.etm_config.server
        return self._handle_response(requests.post(self.url(server), headers=headers, data=data))

    def _format_response(self, response):
        return response.json()['energy_system']
