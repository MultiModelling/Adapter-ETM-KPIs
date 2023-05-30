from tno.esdl_add_etm_kpis_adapter.model.model import Model, ModelState
from tno.esdl_add_etm_kpis_adapter.types import ETMAdapterConfig, ModelRunInfo
from tno.esdl_add_etm_kpis_adapter.model.actions import AddKPIs

from tno.shared.log import get_logger
logger = get_logger(__name__)

class ESDLAddKPIs(Model):

    def run(self, model_run_id: str) -> ModelRunInfo:
        model_run_info = Model.run(self, model_run_id=model_run_id)

        if model_run_info.state == ModelState.ERROR:
            return model_run_info

        # TODO: use a (public) send instead of an if
        if self.model_run_dict[model_run_id].config.action == 'add_kpis':
            return self.add_kpis(model_run_id)

    def add_kpis(self, model_run_id) -> ModelRunInfo:
        config: ETMAdapterConfig = self.model_run_dict[model_run_id].config
        self.model_run_dict[model_run_id].result = AddKPIs(model_run_id).run(config)
        return ModelRunInfo(
            model_run_id=model_run_id,
            state=ModelState.SUCCEEDED,
        )
