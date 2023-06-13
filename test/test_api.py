import requests

api_endpoint = "http://localhost:9202"


res = requests.get(api_endpoint + '/status')
if res.ok:
    print("Endpoint /status ok! ", res)
else:
    print("Endpoint /status not ok! ")
    exit(1)

model_run_id = None
res = requests.get(api_endpoint + '/model/request')
if res.ok:
    print("Endpoint /model/request ok!")
    result = res.json()
    print(result)
    model_run_id = result['model_run_id']
else:
    print("Endpoint /model/request not ok!")
    exit(1)

post_body = {
    "action": "add_kpis",
    "action_config": {
        "base_path": "/",
        "input_esdl_file_path": "test/Hybrid HeatPump.esdl",
        "output_file_path": "test/HHP_ETM_KPIs.esdl",
        "KPI_area": "Nederland",
    },
    "etm_config": {
        "server": "beta",
        "scenario_ID": 2187862,
    }
}

res = requests.post(api_endpoint + '/model/initialize/' + model_run_id, json=post_body)
if res.ok:
    print("Endpoint /model/initialize ok!")
    result = res.json()
    print(result)
else:
    print("Endpoint /model/initialize not ok!")
    print(res.content)
    exit(1)

res = requests.get(api_endpoint + '/model/run/' + model_run_id)
if res.ok:
    print("Endpoint /model/run ok!")
    result = res.json()
    print(result)
else:
    print("Endpoint /model/run not ok!")
    print(res.json())
    exit(1)

res = requests.get(api_endpoint + '/model/status/' + model_run_id)
if res.ok:
    print("Endpoint /model/status ok!")
    result = res.json()
    print(result)
else:
    print("Endpoint /model/status not ok!")
    exit(1)

res = requests.get(api_endpoint + '/model/results/' + model_run_id)
if res.ok:
    print("Endpoint /model/results ok!")
    result = res.json()
    print(result)
else:
    print("Endpoint /model/results not ok!")
    exit(1)

res = requests.get(api_endpoint + '/model/remove/' + model_run_id)
if res.ok:
    print("Endpoint /model/remove ok!")
    result = res.json()
    print(result)
else:
    print("Endpoint /model/remove not ok!")
    exit(1)




