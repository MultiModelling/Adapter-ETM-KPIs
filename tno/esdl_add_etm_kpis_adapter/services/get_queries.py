from datetime import datetime, timedelta
import requests

from .etm_service import ETMService, ETMConnectionError
from tno.shared.log import get_logger

logger = get_logger(__name__)

class GetETEQueries(ETMService):
    """For now locked on electricity price"""

    ETM_DATETIME_FORMAT = "%Y-%m-%d %H:%M"
    BASE_URL = "engine.energytransitionmodel.com/api/v3/scenarios/"
    ENDPOINT = ""
    GQUERIES = {
        "gqueries": [
            'capacity_of_energy_power_wind_turbine_inland_curve',
            # 'capacity_of_energy_flexibility_mv_batteries_electricity_output_curve',
            'capacity_of_energy_hydrogen_flexibility_p2g_electricity_output_curve',
            'capacity_of_energy_hydrogen_steam_methane_reformer_output_curve',
            'capacity_of_energy_power_solar_pv_solar_radiation_curve',
            'capacity_of_transport_car_using_electricity_curve',
            'capacity_of_transport_truck_using_electricity_curve',
            'capacity_of_transport_van_using_electricity_curve',
            'capacity_of_energy_power_nuclear_gen2_uranium_oxide_output_curve',
            'capacity_of_energy_power_nuclear_gen3_uranium_oxide_output_curve'
        ]
    }

    def run(self):
        """Gets the profile from the engine and returns it as values"""
        return self._handle_response(requests.put(self.url(self.data.etm_config.server), json=GetETEQueries.GQUERIES))

    def url(self, server):
        """Generates the url to sen teh request to"""
        logger.info('Connecting to the ETM')

        if server == "beta":
            return f"https://beta-{self.BASE_URL}{self.data.etm_config.scenario_ID}{self.ENDPOINT}"
        if server == "pro":
            return f"https://{self.BASE_URL}{self.data.etm_config.scenario_ID}{self.ENDPOINT}"
        if server == "local":
            return f"http://localhost:3000/api/v3/scenarios/{self.data.etm_config.scenario_ID}"

        raise ETMConnectionError(f"Server {server} unknown, did you mean 'beta' or 'pro'?")

    # Private

    def _format_response(self, response):
        return {
            key: GetETEQueries.format_result(
                self.data.action_config.add_profile.replace_year,
                results['future']
            )
            for key, results in response.json()['gqueries'].items()
        }

    # Static
    @staticmethod
    def format_result(year, curve):
        date = GetETEQueries.gen_days(year)
        return [[next(date), float(value)] for value in curve]


    @staticmethod
    def gen_days( year ):
        start_date=datetime( year, 1, 1 )
        end_date=datetime( year + 1 , 1, 1 )
        d=start_date
        yield start_date
        while d < end_date:
            d += timedelta(hours=1)
            yield d
