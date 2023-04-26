import urllib.parse

from tno.esdl_add_etm_kpis_adapter.model.actions.base_action import BaseAction
from tno.esdl_add_etm_kpis_adapter.model.model import Model
from tno.esdl_add_etm_kpis_adapter.types import ESDLAddETMKPIsAdapterConfig
from tno.esdl_add_etm_kpis_adapter.services import AddKPISService

class AddKPIs(BaseAction):

    # TODO: adjust config to new style
    def run(self, config: ESDLAddETMKPIsAdapterConfig):
        path = self.process_path(config.input_esdl_file_path, config.base_path)

        return self._activate_service(
            config,
            urllib.parse.quote(
                # TODO: fix this one when MINIO is moved to its own class
                self.load_from_minio(path, self.model_run_id).decode('utf-8'),
                safe=''
            )
        )

    def _activate_service(self, config, input_esdl):
        result = AddKPISService(config).run(input_esdl)
        return Model.store_result(self, model_run_id=self.model_run_id, result=result)

