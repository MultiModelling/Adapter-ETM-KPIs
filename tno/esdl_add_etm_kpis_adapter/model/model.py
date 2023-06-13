from abc import ABC, abstractmethod
from io import BytesIO
from typing import Dict
from uuid import uuid4

from tno.esdl_add_etm_kpis_adapter.types import ModelRun, ModelState, ModelRunInfo
from tno.shared.log import get_logger

logger = get_logger(__name__)


class Model(ABC):
    def __init__(self):
        self.model_run_dict: Dict[str, ModelRun] = {}

    def request(self):
        model_run_id = str(uuid4())
        self.model_run_dict[model_run_id] = ModelRun(
            state=ModelState.ACCEPTED,
            config=None,
            result=None,
        )

        return ModelRunInfo(
            state=self.model_run_dict[model_run_id].state,
            model_run_id=model_run_id,
        )

    def initialize(self, model_run_id: str, config=None):
        if model_run_id in self.model_run_dict:
            self.model_run_dict[model_run_id].config = config
            self.model_run_dict[model_run_id].state = ModelState.READY
            return ModelRunInfo(
                state=self.model_run_dict[model_run_id].state,
                model_run_id=model_run_id,
            )
        else:
            return ModelRunInfo(
                model_run_id=model_run_id,
                state=ModelState.ERROR,
                reason="Error in Model.initialize(): model_run_id unknown"
            )

    def run(self, model_run_id: str):
        if model_run_id in self.model_run_dict:
            self.model_run_dict[model_run_id].state = ModelState.RUNNING
            return ModelRunInfo(
                state=self.model_run_dict[model_run_id].state,
                model_run_id=model_run_id,
            )
        else:
            return ModelRunInfo(
                model_run_id=model_run_id,
                state=ModelState.ERROR,
                reason="Error in Model.run(): model_run_id unknown"
            )

    def status(self, model_run_id: str):
        if model_run_id in self.model_run_dict:
            # Dummy behaviour: Query status once, to let finish model
            self.model_run_dict[model_run_id].state = ModelState.SUCCEEDED

            return ModelRunInfo(
                state=self.model_run_dict[model_run_id].state,
                model_run_id=model_run_id,
            )
        else:
            return ModelRunInfo(
                model_run_id=model_run_id,
                state=ModelState.ERROR,
                reason="Error in Model.status(): model_run_id unknown"
            )

    def results(self, model_run_id: str):
        if model_run_id in self.model_run_dict:
            return ModelRunInfo(
                state=self.model_run_dict[model_run_id].state,
                model_run_id=model_run_id,
                result=self.model_run_dict[model_run_id].result,
            )
        else:
            return ModelRunInfo(
                model_run_id=model_run_id,
                state=ModelState.ERROR,
                reason="Error in Model.results(): model_run_id unknown"
            )

    def remove(self, model_run_id: str):
        if model_run_id in self.model_run_dict:
            del self.model_run_dict[model_run_id]
            return ModelRunInfo(
                model_run_id=model_run_id,
                state=ModelState.UNKNOWN,
            )
        else:
            return ModelRunInfo(
                model_run_id=model_run_id,
                state=ModelState.ERROR,
                reason="Error in Model.remove(): model_run_id unknown"
            )
