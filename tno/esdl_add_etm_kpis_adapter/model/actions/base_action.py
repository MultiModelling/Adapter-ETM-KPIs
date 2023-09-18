from tno.esdl_add_etm_kpis_adapter.model.model import ModelState
from tno.esdl_add_etm_kpis_adapter.types import ModelRunInfo
from tno.esdl_add_etm_kpis_adapter.services import ETMConnectionError

class BaseAction:
    def __init__(self, model_run_id: str) -> None:
        self.model_run_id = model_run_id

    def run(self):
        """Runs the action, returns a ModelRunInfo with the results"""
        pass

    def process_results(self, result):
        if self.minio_client:
            return result
        else:
            # TODO: human readable result
            return ''

    def process_path(self, path: str, base_path: str) -> str:
        if path[0] == '.':
            return base_path + path.lstrip('./')
        else:
            return path.lstrip('./')

    def _activate_service(self, *args):
        """Runs the applicable ETMService and returns the results"""
        pass

    def _handle_response(self, *args):
        try:
            return self._activate_service(*args)
        except (ETMConnectionError, ESDLError) as e:
            return ModelRunInfo(
                model_run_id=self.model_run_id,
                state=ModelState.ERROR,
                reason=getattr(e, 'message', repr(e))
            )

class ESDLError(BaseException):
    pass
