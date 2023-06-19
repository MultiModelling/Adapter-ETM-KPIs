import requests

api_endpoint = "http://localhost:9202"

kpis_post_body = {
    "action": "add_kpis",
    "action_config": {
        "add_kpis": {
            "base_path": "/",
            "input_esdl_file_path": "test/Hybrid HeatPump.esdl",
            "output_file_path": "test/HHP_ETM_KPIs.esdl",
            "KPI_area": "Nederland",
        },
    },
    "etm_config": {
        "server": "beta",
        "scenario_ID": 2187862,
    }
}

create_context_post_body = {
    "action": "create_with_context",
    "action_config": {
        "create_with_context": {
            "base_path": "/",
            "input_esdl_start_situation_file_path": "test/MICRO_input1.esdl",
            "input_esdl_end_situation_file_path": "test/MICRO_input2.esdl",
        },
    },
    "etm_config": {
        "server": "local",
        "scenario_ID": 2234938,
    }
}

create_post_body = {
    "action": "create",
    "action_config": {
        "create": {
            "base_path": "/",
            "input_esdl_file_path": "test/Hybrid HeatPump.esdl",
        },
    },
    "etm_config": {
        "server": "beta",
        "scenario_ID": 2187862,
    }
}

def test_complete_run(post_body):

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


    # TODO: add a test for create with context
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

# print('TEST KPIS')
# test_complete_run(kpis_post_body)

print('\nTEST CREATE')
test_complete_run(create_post_body)

# print('\nTEST CREATE WITH CONTEXT')
# test_complete_run(create_context_post_body)
