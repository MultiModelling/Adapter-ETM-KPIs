import datetime
import pytz
import requests

from .etm_service import ETMService, ETMConnectionError
from tno.shared.log import get_logger

logger = get_logger(__name__)

class GetETEProfile(ETMService):
    """For now locked on electricity price"""

    ETM_DATETIME_FORMAT = "%Y-%m-%d %H:%M"
    BASE_URL = "engine.energytransitionmodel.com/api/v3/scenarios/"
    ENDPOINT = "/curves/electricity_price.csv"

    def run(self):
        """Gets the profile from the engine and returns it as values"""
        return self._handle_response(requests.get(self.url(self.data.etm_config.server)))

    def url(self, server):
        """Generates the url to sen teh request to"""
        logger.info('Connecting to the ETM')

        if server == "beta":
            return f"https://beta-{self.BASE_URL}{self.data.etm_config.scenario_ID}{self.ENDPOINT}"
        if server == "pro":
            return f"https://{self.BASE_URL}{self.data.etm_config.scenario_ID}{self.ENDPOINT}"
        if server == "local":
            return f"http://localhost:3000/api/v3/scenarios/{self.data.etm_config.scenario_ID}{self.ENDPOINT}"

        raise ETMConnectionError(f"Server {server} unknown, did you mean 'beta' or 'pro'?")

    # Private

    def _format_response(self, response):
        return GetETEProfile.process_csv_bytes(
            response.content,
            self.data.action_config.add_profile.replace_year
        )

    # Static

    @staticmethod
    def parse_etm_datetime(dt_str):
        cet = pytz.timezone("Europe/Amsterdam")
        utc = pytz.timezone("UTC")


        dt = datetime.datetime.strptime(dt_str, GetETEProfile.ETM_DATETIME_FORMAT)
        cet_dt = cet.localize(dt)           # Assume CET timezone for dates returned by ETM
        utc_dt = cet_dt.astimezone(utc)     # Convert them to UTC...
        return utc_dt

    @staticmethod
    def process_csv_bytes(csv_bytes, replace_year) -> list[float]:
        csv_str = csv_bytes.decode('utf-8')

        curve_lines_str = csv_str.split('\n')
        curve_lines = [line.split(',') for line in curve_lines_str]
        curve_lines.pop(0)              # Remove header
        while curve_lines[-1] == ['']:  # Last line(s) can be empty
            curve_lines.pop(-1)

        if replace_year:
            curve_values = [[GetETEProfile.parse_etm_datetime(v[0].replace('2050', str(replace_year))), float(v[1])]
                            for v in curve_lines]
        else:
            curve_values = [[GetETEProfile.parse_etm_datetime(v[0]), float(v[1])] for v in curve_lines]
        return curve_values
