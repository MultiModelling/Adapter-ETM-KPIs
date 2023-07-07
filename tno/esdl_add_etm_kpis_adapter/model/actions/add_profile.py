import urllib.parse

from esdl import esdl
from esdl.esdl_handler import EnergySystemHandler
from uuid import uuid4

from tno.esdl_add_etm_kpis_adapter.model.actions.base_action import BaseAction
from tno.esdl_add_etm_kpis_adapter.types import ETMAdapterConfig
from tno.esdl_add_etm_kpis_adapter.services import GetETEProfile
from tno.esdl_add_etm_kpis_adapter.services.minio import MinioConnection
from tno.esdl_add_etm_kpis_adapter.services.influx_db import InfluxDBService
from tno.shared.log import get_logger

logger = get_logger(__name__)

class AddProfile(BaseAction):
    '''Adds a price curve from the ETM to an ESDL file'''

    def run(self, config: ETMAdapterConfig):
        path = self.process_path(
            config.action_config.add_profile.input_esdl_file_path,
            config.action_config.add_profile.base_path
        )

        return self._handle_response(
            config,
            urllib.parse.quote(
                MinioConnection().load_from_path(path).decode('utf-8'),
                safe=''
            )
        )

    def _activate_service(self, config: ETMAdapterConfig, input_esdl):
        return MinioConnection().store_result(
            self.process_path(
                config.action_config.add_profile.output_file_path,
                config.action_config.add_profile.base_path
            ), result=self._attach_profile(config, input_esdl)
        )

    def _attach_profile(self, config, input_esdl):
        '''Attach profile to the esdl'''
        profile = GetETEProfile(config).run()

        influx_db = None
        if config.add_profile.influxdb_config:
            influx_db = InfluxDBService(config.add_profile.influxdb_config)
            influx_db.upload_profile(profile)

        esh = EnergySystemHandler()
        es = esh.load_from_string(input_esdl)

        esi: esdl.EnergySystemInformation = es.energySystemInformation
        if esi:
            carrs: esdl.Carriers = esi.carriers
            for carr in carrs.carrier:
                if isinstance(carr, esdl.ElectricityCommodity):
                    if influx_db:
                        carr.cost = influx_db.create_esdl_influxdb_profile(profile)
                    else:
                        carr.cost = AddProfile.create_esdl_timeseries_profile(profile)
                    break
        else:
            logger.info('Could not attach profile: EnergySystemInformation missing')

        return esh.to_string()

    @staticmethod
    def create_esdl_timeseries_profile(profile_array):
        profile = esdl.TimeSeriesProfile(
            id=str(uuid4()),
            startDateTime=profile_array[0][0],
            timestep=3600,
            values=[v[1] for v in profile_array]
        )
        profile.profileQuantityAndUnit = esdl.QuantityAndUnitType(
            id=str(uuid4()),
            physicalQuantity=esdl.PhysicalQuantityEnum.COST,
            unit=esdl.UnitEnum.EURO,
            perMultiplier=esdl.MultiplierEnum.MEGA,
            perUnit=esdl.UnitEnum.WATTHOUR,
            description="COST in EUR/MWh"
        )

        return profile
