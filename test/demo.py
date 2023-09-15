import requests

api_endpoint = "http://localhost:9202"

export_post_body = {
    "action": "export",
    "action_config": {
        "export": {
            "base_path": "/",
            "input_esdl_file_path": "test/MACRO_input.esdl",
            "output_file_path": "test/MACRO_output.esdl",
        },
    },
    "etm_config": {
        "server": "beta",
        "scenario_ID": 2361577,
    }
}

create_post_body = {
    "action": "create",
    "action_config": {
        "create": {
            "base_path": "/",
            "input_esdl_file_path": "test/MACRO_input.esdl",
        },
    },
    "etm_config": {
        "server": "local",
        "scenario_ID": 2361577,
    }
}

export_two_post_body = {
    "action": "export",
    "action_config": {
        "export": {
            "base_path": "/",
            "input_esdl_file_path": "test/MACRO_input.esdl",
            "output_file_path": "test/MACRO_opera_output_with_etm.esdl",
        },
    },
    "etm_config": {
        "server": "local",
        "scenario_ID": 2361577,
    }
}

add_profile_post_body = {
    "action": "add_profile",
    "action_config": {
        "add_profile": {
            "base_path": "/",
            "input_esdl_file_path": "test/MACRO_opera_output_with_etm.esdl",
            "output_file_path": "test/MACRO_opera_output_with_etm_profiles.esdl",
            "replace_year": 2050,
        },
    },
    "etm_config": {
        "server": "beta",
        "scenario_ID": 2361577,
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

# print('\nEXPORT')
# test_complete_run(export_post_body)

# print('\nCREATE')
# test_complete_run(create_post_body)

# print('\nEXPORT')
# test_complete_run(export_two_post_body)


print('\nADD PROFILE')
test_complete_run(add_profile_post_body)
