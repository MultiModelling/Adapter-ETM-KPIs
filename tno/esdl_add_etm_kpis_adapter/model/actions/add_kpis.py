import urllib.parse

from tno.esdl_add_etm_kpis_adapter.model.actions.base_action import BaseAction
from tno.esdl_add_etm_kpis_adapter.types import ETMAdapterConfig
from tno.esdl_add_etm_kpis_adapter.services import AddKPISService
from tno.esdl_add_etm_kpis_adapter.services.minio import MinioConnection

class AddKPIs(BaseAction):

    def run(self, config: ETMAdapterConfig):
        path = self.process_path(
            config.action_config.add_kpis.input_esdl_file_path,
            config.base_path
        )

        return self._handle_response(
            config,
            MinioConnection().load_from_path(path).decode('utf-8')
        )

    def _activate_service(self, config: ETMAdapterConfig, input_esdl):
        return MinioConnection().store_result(
            self.process_path(
                config.action_config.add_kpis.output_file_path,
                config.base_path
            ), result=AddKPISService(config).run(input_esdl)
        )

