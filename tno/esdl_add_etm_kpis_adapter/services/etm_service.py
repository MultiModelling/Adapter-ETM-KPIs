class ETMService:
    ENDPOINT = ""
    BASE_URL = "esdl.energytransitionmodel.com/api/v1/"

    def __init__(self, data):
        self.data = data

    def url(self, server):
        """Generates the url to sen teh request to"""
        if server == "beta":
            return f"https://beta-{self.BASE_URL}{self.ENDPOINT}"
        if server == "pro":
            return f"https://{self.BASE_URL}{self.ENDPOINT}"

        raise ETMConnectionError(f"Server {server} unknown, did you mean 'beta' or 'pro'?")

    def run(self, *args):
        pass

    def _handle_response(self, response):
        if response.ok:
            return self._format_response(response)

        raise ETMConnectionError(
            f"Error in ETM.run(): ETM API returned: {response.status_code} {response.reason}"
        )

    def _format_response(response):
        pass

class ETMConnectionError(BaseException):
    pass
