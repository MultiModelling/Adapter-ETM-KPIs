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


### Global configs

@dataclass
class ETMConfig:
    server: str
    scenario_ID: int


@dataclass
class InfluxDBConfig:
    host: Optional[str] = None
    port: Optional[int] = None
    esdl_host: Optional[str] = None
    esdl_port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    measurement: Optional[str] = None
    field: Optional[str] = None


### Individual adapter configs

@dataclass
class CreateETMScenarioFromESDLWithContextConfig:
    base_path: Optional[str] = None
    input_esdl_start_situation_file_path: Optional[str] = None
    input_esdl_end_situation_file_path: Optional[str] = None


@dataclass
class CreateETMScenarioFromESDLConfig:
    base_path: Optional[str] = None
    input_esdl_file_path: Optional[str] = None


@dataclass
class ESDLAddETMKPIsAdapterConfig:
    KPI_area: str
    input_esdl_file_path: Optional[str] = None
    output_file_path: Optional[str] = None
    base_path: Optional[str] = None

@dataclass
class ExportESDLAdapterConfig:
    input_esdl_file_path: Optional[str] = None
    output_file_path: Optional[str] = None
    base_path: Optional[str] = None


@dataclass
class AddProfileFromETMAdapterConfig:
    "For now we only add electricity price"
    input_esdl_file_path: Optional[str] = None
    output_file_path: Optional[str] = None
    base_path: Optional[str] = None
    # profile: str = "electricity_price"
    influx_db_config: Optional[InfluxDBConfig] = None
    replace_year: Optional[int] = None


@dataclass
class ActionConfig:
    add_kpis: Optional[ESDLAddETMKPIsAdapterConfig]
    create_with_context:  Optional[CreateETMScenarioFromESDLWithContextConfig]
    create: Optional[CreateETMScenarioFromESDLConfig]
    export: Optional[ExportESDLAdapterConfig]
    add_profile: Optional[AddProfileFromETMAdapterConfig]


### Main configs used by API

@dataclass
class ETMAdapterConfig:
    etm_config: ETMConfig
    action_config: ActionConfig
    action: Literal['add_kpis', 'add_profile', 'create_with_context', 'create', 'export'] = 'add_kpis'


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
