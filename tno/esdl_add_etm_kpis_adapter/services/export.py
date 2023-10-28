import requests

from tno.shared.log import get_logger
logger = get_logger(__name__)

from .etm_service import ETMService
class ExportService(ETMService):
    ENDPOINT = 'export_esdl'

    def run(self, input_esdl):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'session_id_min': self.data.etm_config.scenario_ID,
            'energy_system': input_esdl
        }
        if self.data.etm_config.scenario_ID_max is not None:
            data['session_id_max'] = self.data.etm_config.scenario_ID_max
        server = self.data.etm_config.server
        return self._handle_response(requests.post(self.url(server), headers=headers, data=data))

    def _format_response(self, response):
        return response.json()['energy_system']
