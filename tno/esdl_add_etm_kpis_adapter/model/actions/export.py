import urllib.parse

from tno.esdl_add_etm_kpis_adapter.model.actions.base_action import BaseAction
from tno.esdl_add_etm_kpis_adapter.types import ETMAdapterConfig
from tno.esdl_add_etm_kpis_adapter.services import ExportService
from tno.esdl_add_etm_kpis_adapter.services.minio import MinioConnection

class Export(BaseAction):

    def run(self, config: ETMAdapterConfig):
        path = self.process_path(
            config.action_config.export.input_esdl_file_path,
            config.action_config.export.base_path
        )

        return self._handle_response(
            config,
            urllib.parse.quote(
                MinioConnection().load_from_path(path).decode('utf-8'),
                safe=''
            )
        )

    def _activate_service(self, config: ETMAdapterConfig, input_esdl):
        return MinioConnection().store_result(
            self.process_path(
                config.action_config.export.output_file_path,
                config.action_config.export.base_path
            ), result=ExportService(config).run(input_esdl)
        )

