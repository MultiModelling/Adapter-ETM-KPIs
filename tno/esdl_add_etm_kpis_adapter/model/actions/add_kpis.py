import urllib.parse

from tno.esdl_add_etm_kpis_adapter.model.actions.base_action import BaseAction
from tno.esdl_add_etm_kpis_adapter.model.model import Model
from tno.esdl_add_etm_kpis_adapter.types import ESDLAddETMKPIsAdapterConfig
from tno.esdl_add_etm_kpis_adapter.services import AddKPISService
from tno.esdl_add_etm_kpis_adapter.services.minio import MinioConnection

class AddKPIs(BaseAction):

    # TODO: adjust config to new style
    def run(self, config: ESDLAddETMKPIsAdapterConfig):
        path = self.process_path(config.input_esdl_file_path, config.base_path)

        return self._activate_service(
            config,
            urllib.parse.quote(
                MinioConnection().load_from_path(path).decode('utf-8'),
                safe=''
            )
        )

    def _activate_service(self, config, input_esdl):
        return MinioConnection().store_result(
            self.process_path(config.output_file_path, config.base_path),
            result=AddKPISService(config).run(input_esdl)
        )

