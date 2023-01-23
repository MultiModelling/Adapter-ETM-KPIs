import requests

from tno.esdl_add_etm_kpis_adapter.model.model import Model, ModelState
from tno.esdl_add_etm_kpis_adapter.types import ESDLAddETMKPIsAdapterConfig, ModelRunInfo

# from esdl import esdl
# from esdl.esdl_handler import EnergySystemHandler

class ESDLAddKPIs(Model):

    def process_results(self, result):
        if self.minio_client:
            return result
        else:
            # TODO: human readable result
            return ''

    def run(self, model_run_id: str):
        model_run_info = Model.run(self, model_run_id=model_run_id)

        if model_run_info.state == ModelState.ERROR:
            return model_run_info

        config: ESDLAddETMKPIsAdapterConfig = self.model_run_dict[model_run_id].config

        input_esdl_bytes = self.load_from_minio(config.base_path + config.input_esdl_file_path)
        input_esdl = input_esdl_bytes.decode('utf-8')

        url = config.etm_config.endpoint + config.etm_config.path
        response = requests.post(
            url,
            headers={'Content-Type': 'multipart/form-data'},
            # files={"energy_system": ('my_file', input_esdl)},
            data={
                'scenario_id': config.scenario_ID,
                "area_name": config.KPI_area,
                "energy_system": input_esdl
            }
        )

        if response.ok:
            esdl_str = response.json()['energy_system']
            model_run_info = Model.store_result(self, model_run_id=model_run_id, result=esdl_str)
            return model_run_info
        else:
            return ModelRunInfo(
                model_run_id=model_run_id,
                state=ModelState.ERROR,
                reason=f"Error in ETM.run(): ETM API returned: {response.status_code} {response.reason}"
            )
