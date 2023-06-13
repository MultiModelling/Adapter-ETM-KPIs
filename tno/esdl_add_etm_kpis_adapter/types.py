from enum import Enum
from typing import Dict, Optional, Any, ClassVar, Type, Literal
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

@dataclass
class ETMConfig:
    server: str
    scenario_ID: int



@dataclass
class ActionConfig:
    pass
    # ADD_KPIS = ESDLAddETMKPIsAdapterConfig


@dataclass
class ESDLAddETMKPIsAdapterConfig(ActionConfig):
    KPI_area: str
    input_esdl_file_path: Optional[str] = None
    output_file_path: Optional[str] = None
    base_path: Optional[str] = None


@dataclass
class ETMAdapterConfig:
    etm_config: ETMConfig
    action_config: ActionConfig
    action: Literal['add_kpis', 'other action'] = 'add_kpis'


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
