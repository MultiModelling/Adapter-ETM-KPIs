import urllib.parse

from tno.esdl_add_etm_kpis_adapter.model.actions.base_action import BaseAction
from tno.esdl_add_etm_kpis_adapter.types import ETMAdapterConfig
from tno.esdl_add_etm_kpis_adapter.services import CreateWithContextService
from tno.esdl_add_etm_kpis_adapter.services.minio import MinioConnection

class CreateWithContext(BaseAction):

    def run(self, config: ETMAdapterConfig):
        path_start = self.process_path(
            config.action_config.create_with_context.input_esdl_start_situation_file_path,
            config.action_config.create_with_context.base_path
        )

        path_end = self.process_path(
            config.action_config.create_with_context.input_esdl_end_situation_file_path,
            config.action_config.create_with_context.base_path
        )

        return self._handle_response(
            config,
            urllib.parse.quote(
                MinioConnection().load_from_path(path_start).decode('utf-8'),
                safe=''
            ),
            urllib.parse.quote(
                MinioConnection().load_from_path(path_end).decode('utf-8'),
                safe=''
            )
        )

    def _activate_service(self, config: ETMAdapterConfig, input_esdl_start, input_esdl_end):
        return CreateWithContextService(config).run(input_esdl_start, input_esdl_end)

