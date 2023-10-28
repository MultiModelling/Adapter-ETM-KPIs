import urllib.parse

from tno.esdl_add_etm_kpis_adapter.model.actions.base_action import BaseAction
from tno.esdl_add_etm_kpis_adapter.types import ETMAdapterConfig
from tno.esdl_add_etm_kpis_adapter.services import CreateWithContextService
from tno.esdl_add_etm_kpis_adapter.services.minio import MinioConnection

from tno.shared.log import get_logger
logger = get_logger(__name__)

class CreateWithContext(BaseAction):

    def run(self, config: ETMAdapterConfig):
        path_start = self.process_path(
            config.action_config.create_with_context.input_esdl_start_situation_file_path,
            config.base_path
        )
        logger.info(f"file_path: {config.action_config.create_with_context.input_esdl_start_situation_file_path}")
        logger.info(f"base_path: {config.base_path}")
        logger.info(f"path_start: {path_start}")

        path_end = self.process_path(
            config.action_config.create_with_context.input_esdl_end_situation_file_path,
            config.base_path
        )

        return self._handle_response(
            config,
            MinioConnection().load_from_path(path_start).decode('utf-8'),
            MinioConnection().load_from_path(path_end).decode('utf-8')
        )

    def _activate_service(self, config: ETMAdapterConfig, input_esdl_start, input_esdl_end):
        return CreateWithContextService(config).run(input_esdl_start, input_esdl_end)

