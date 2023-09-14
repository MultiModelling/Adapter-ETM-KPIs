import urllib.parse

from esdl import esdl
from esdl.esdl_handler import EnergySystemHandler
from uuid import uuid4

from tno.esdl_add_etm_kpis_adapter.model.actions.base_action import BaseAction
from tno.esdl_add_etm_kpis_adapter.types import ETMAdapterConfig
from tno.esdl_add_etm_kpis_adapter.services import GetETEProfile, GetETEQueries
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
        # Price profile
        profile = GetETEProfile(config).run()
        # Other curves
        curves = GetETEQueries(config).run()

        influx_db = None
        if config.add_profile.influxdb_config:
            influx_db = InfluxDBService(config.add_profile.influxdb_config)
            influx_db.upload_profile(profile)

        esh = EnergySystemHandler()
        es = esh.load_from_string(input_esdl)

        # Price profile
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

        # Add curves
        all_assets = es.instance.area.asset

        for asset in all_assets:
            if isinstance(asset, esdl.WindTurbine):
                self._add_curve_to_inport(influx_db, asset, curves['capacity_of_energy_power_wind_turbine_inland_curve'])
            elif isinstance(asset, esdl.Battery):
                self._add_curve_to_inport(influx_db, asset, curves['capacity_of_energy_flexibility_mv_batteries_electricity_output_curve'])
            elif isinstance(asset, esdl.Electrolyzer):
                self._add_curve_to_inport(influx_db, asset, curves['capacity_of_energy_hydrogen_flexibility_p2g_electricity_output_curve'])
            elif isinstance(asset, esdl.GasConversion):
                self._add_curve_to_inport(influx_db, asset, curves['capacity_of_energy_hydrogen_steam_methane_reformer_output_curve'])
            elif isinstance(asset, esdl.PVInstallation):
                self._add_curve_to_inport(influx_db, asset, curves['capacity_of_energy_power_solar_pv_solar_radiation_curve'])
            elif isinstance(asset, esdl.MobilityDemand) and asset.fuelType == esdl.MobilityFuelTypeEnum.ELECTRICITY:
                if asset.type == esdl.VehicleTypeEnum.CAR:
                    self._add_curve_to_inport(influx_db, asset, curves['capacity_of_transport_car_using_electricity_curve'])
                elif asset.type == esdl.VehicleTypeEnum.TRUCK:
                    self._add_curve_to_inport(influx_db, asset, curves['capacity_of_transport_truck_using_electricity_curve'])
                elif asset.type == esdl.VehicleTypeEnum.VAN:
                    self._add_curve_to_inport(influx_db, asset, curves['capacity_of_transport_van_using_electricity_curve'])
            elif isinstance(asset, esdl.Powerplant):
                if asset.type == esdl.PowerPlantTypeEnum.NUCLEAR_2ND_GENERATION:
                    self._add_curve_to_inport(influx_db, asset, curves['capacity_of_energy_power_nuclear_gen2_uranium_oxide_output_curve'])
                elif asset.type == esdl.PowerPlantTypeEnum.NUCLEAR_3RD_GENERATION:
                    self._add_curve_to_inport(influx_db, asset, curves['capacity_of_energy_power_nuclear_gen3_uranium_oxide_output_curve'])


        return esh.to_string()

    def _add_curve_to_inport(self, influx_db, asset, curve):
        if influx_db:
            asset.port[0].profile = influx_db.create_esdl_influxdb_profile(curve)
        else:
            asset.port[0].profile = AddProfile.create_esdl_timeseries_profile(curve)

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
