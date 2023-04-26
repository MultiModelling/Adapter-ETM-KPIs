from enum import Enum
from typing import Dict, Optional, Any, ClassVar, Type
from marshmallow_dataclass import dataclass
from dataclasses import field

from marshmallow import Schema, fields


class ModelState(str, Enum):
    UNKNOWN = "UNKNOWN"
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    QUEUED = "QUEUED"
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    ERROR = "ERROR"

class ActionTypes(str, Enum):
    ADD_KPIS = "add_kpis"

@dataclass
class ETMConfig:
    # TODO: beta or pro!
    server: str
    scenario_ID: int


@dataclass
class ActionConfig:
    pass


@dataclass
class ETMAdapterConfig:
    action: ActionTypes = field(default=ActionTypes.ADD_KPIS)
    etm_config: ETMConfig
    action_config: ActionConfig


@dataclass
class ESDLAddETMKPIsAdapterConfig(ActionConfig):
    KPI_area: str
    input_esdl_file_path: Optional[str] = None
    output_file_path: Optional[str] = None
    base_path: Optional[str] = None


@dataclass
class ModelRun:
    state: ModelState
    config: ETMAdapterConfig
    result: dict


@dataclass(order=True)
class ModelRunInfo:
    model_run_id: str
    state: ModelState = field(default=ModelState.UNKNOWN)
    result: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None

    # support for Schema generation in Marshmallow
    Schema: ClassVar[Type[Schema]] = Schema
