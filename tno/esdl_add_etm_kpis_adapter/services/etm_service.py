from tno.shared.log import get_logger
import requests

logger = get_logger(__name__)

class ETMService:
    ENDPOINT = ""
    BASE_URL = "esdl.energytransitionmodel.com/api/v1/"

    def __init__(self, data):
        self.data = data

    def url(self, server):
        """Generates the url to sen teh request to"""
        logger.info('Connecting to the ETM')

        if server == "beta":
            return f"https://beta-{self.BASE_URL}{self.ENDPOINT}"
        if server == "pro":
            return f"https://{self.BASE_URL}{self.ENDPOINT}"
        if server == "local":
            return f"http://host.docker.internal:5001/api/v1/{self.ENDPOINT}"

        raise ETMConnectionError(f"Server {server} unknown, did you mean 'beta' or 'pro'?")

    def run(self, *args):
        pass

    def _handle_response(self, response):
        if response.ok:
            return self._format_response(response)

        try:
            message = response.json().get('message', 'unknown')
            if message == 'unknown':
                message = response.json().get('errors', 'unknown')
        except requests.exceptions.JSONDecodeError:
            message = ''
        raise ETMConnectionError(
            f"Error in ETM.run(): ETM API returned: {response.status_code}: {message}"
        )

    def _format_response(response):
        pass

class ETMConnectionError(BaseException):
    pass
