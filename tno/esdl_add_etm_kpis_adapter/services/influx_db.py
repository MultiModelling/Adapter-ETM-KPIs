from datetime import datetime
from esdl import esdl
from influxdb import InfluxDBClient
from uuid import uuid4

from tno.esdl_add_etm_kpis_adapter.types import InfluxDBConfig

class InfluxDBService:
    INFLUXDB_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:00+0000"

    def __init__(self, config: InfluxDBConfig) -> None:
        self.config = config

    def upload_profile(self, profile_array):
        """Uploads the price profile to the influx DB"""
        use_ssl = self.config.host.startswith('https')
        if self.config.host.startswith('http'):     # matches http or https
            host_without_protocol = self.config.host.split('://')[1]
        else:
            host_without_protocol = self.config.host

        client = InfluxDBClient(
            host=host_without_protocol,
            port=self.config.port,
            username=self.config.username,
            password=self.config.password,
            database=self.config.database,
            ssl=use_ssl
        )
        if self.config.database not in client.get_list_database():
            client.create_database(self.config.database)

        json_body = []

        for profile_element in profile_array:
            fields = dict()
            fields[self.config.field] = float(profile_element[1])

            json_body.append({
                "measurement": self.config.measurement,
                "time": datetime.strftime(profile_element[0], self.INFLUXDB_DATETIME_FORMAT),
                "fields": fields
            })

        client.write_points(points=json_body, database=self.config.database, batch_size=100)

    def create_esdl_influxdb_profile(self, profile_array) -> esdl.InfluxDBProfile:
        '''Create an ESDL asset linked to the influx DB, to be instered in the ESDL'''
        profile = esdl.InfluxDBProfile(
            id=str(uuid4()),
            host=self.config.esdl_host if self.config.esdl_host else self.config.host,
            port=self.config.esdl_port if self.config.esdl_port else self.config.portrt,
            database=self.config.database,
            measurement=self.config.measurement,
            field=self.config.field,
            startDate=profile_array[0][0],
            endDate=profile_array[-1][0],
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
