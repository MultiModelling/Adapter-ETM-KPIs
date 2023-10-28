import requests

from .etm_service import ETMService

from tno.shared.log import get_logger
logger = get_logger(__name__)
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
        logger.debug(f"server: {self.url(server)}")
        logger.debug(f"headers: {headers}")
        logger.debug(f"data: {data}")
        r = requests.post(self.url(server), headers=headers, data=data)
        logger.debug(r.request.body)
        return self._handle_response(r)

    def _format_response(self, response):
        return response.json()['scenario_id']
