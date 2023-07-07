from tno.esdl_add_etm_kpis_adapter.model.model import Model, ModelState
from tno.esdl_add_etm_kpis_adapter.types import ETMAdapterConfig, ModelRunInfo
from tno.esdl_add_etm_kpis_adapter.model.actions import AddKPIs, AddProfile, CreateWithContext, Create, Export

from tno.shared.log import get_logger
logger = get_logger(__name__)

class ETMESDL(Model):

    def run(self, model_run_id: str) -> ModelRunInfo:
        model_run_info = Model.run(self, model_run_id=model_run_id)

        if model_run_info.state == ModelState.ERROR:
            return model_run_info

        return getattr(self, self.model_run_dict[model_run_id].config.action)(model_run_id)

    def add_kpis(self, model_run_id) -> ModelRunInfo:
        return self.__activate(model_run_id, AddKPIs)

    def add_profile(self, model_run_id) -> ModelRunInfo:
        return self.__activate(model_run_id, AddProfile)

    def create_with_context(self, model_run_id) -> ModelRunInfo:
        return self.__activate(model_run_id, CreateWithContext)

    def create(self, model_run_id) -> ModelRunInfo:
        return self.__activate(model_run_id, Create)

    def export(self, model_run_id) -> ModelRunInfo:
        return self.__activate(model_run_id, Export)

    # private

    def __activate(self, model_run_id, action_klass) -> ModelRunInfo:
        config: ETMAdapterConfig = self.model_run_dict[model_run_id].config
        return self.__handle_result(model_run_id, action_klass(model_run_id).run(config))

    def __handle_result(self, model_run_id, result) -> ModelRunInfo:
        if isinstance(result, ModelRunInfo):
            return result

        self.model_run_dict[model_run_id].result = result
        return ModelRunInfo(
            model_run_id=model_run_id,
            state=ModelState.SUCCEEDED,
        )
