from enum import Enum
from typing import Dict, Optional, Any, ClassVar, Type, Literal
from marshmallow_dataclass import dataclass
from dataclasses import field

from marshmallow import Schema, fields, validates, ValidationError


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
class CreateETMScenarioFromESDLWithContextConfig:
    base_path: Optional[str] = None
    input_esdl_start_situation_file_path: Optional[str] = None
    input_esdl_end_situation_file_path: Optional[str] = None

@dataclass
class ESDLAddETMKPIsAdapterConfig:
    KPI_area: str
    input_esdl_file_path: Optional[str] = None
    output_file_path: Optional[str] = None
    base_path: Optional[str] = None


@dataclass
class ActionConfig:
    add_kpis: Optional[ESDLAddETMKPIsAdapterConfig]
    create_with_context:  Optional[CreateETMScenarioFromESDLWithContextConfig]


@dataclass
class ETMAdapterConfig:
    etm_config: ETMConfig
    action_config: ActionConfig
    action: Literal['add_kpis', 'create_with_context'] = 'add_kpis'


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
