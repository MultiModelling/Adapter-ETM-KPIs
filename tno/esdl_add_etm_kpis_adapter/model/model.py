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

        # TODO: move to other class -> we can make it a singleton if we want :)
        # self.minio_client = None
        # if EnvSettings.minio_endpoint():
        #     logger.info(f"Connecting to Minio Object Store at {EnvSettings.minio_endpoint()}")
        #     self.minio_client = Minio(
        #         endpoint=EnvSettings.minio_endpoint(),
        #         secure=EnvSettings.minio_secure(),
        #         access_key=EnvSettings.minio_access_key(),
        #         secret_key=EnvSettings.minio_secret_key()
        #     )
        # else:
        #     logger.info("No Minio Object Store configured")

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

    def process_path(self, path: str, base_path: str) -> str:
        if path[0] == '.':
            return base_path + path.lstrip('./')
        else:
            return path.lstrip('./')

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
