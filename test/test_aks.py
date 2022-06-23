import json
import requests
import statistics
import time

url = "http://YOUR_K8S_EXTERNAL_IP/predict"

def simulate_requests(n_call_cycles = 1):

    sample_payload_healthy = {
        "ID": 12312312,
        "AN3": 3423423,
        "AN4": 0.8558,
        "AN5": 1.7265,
        "AN6": "666",
        "AN7": "-224234234",
        "AN8": "-323423423.2137",
        "AN9": "-23423",
        "AN10": "-23423",
        "SPEED": "-2345",
        "TORQUE": "1000",
        "TIMESTAMP": "2022-05-23T10:05:05"
    }

    sample_payload_damaged = {
        "ID": 500,
        "AN3": -0.683120,
        "AN4": -1.059300,
        "AN5": 0.996200,
        "AN6": -0.88845,
        "AN7": 0.164590,
        "AN8": -1.224400,
        "AN9": 0.645990,
        "AN10": 1.577600,
        "SPEED": 0.000641,
        "TORQUE": None,
        "TIMESTAMP": "2020-06-06 14:09:22"
    }

    call_times = []

    for i in range(0, n_call_cycles):

        print(f"🚀 Making POST request 1 to {url}...")
        print(f"⬆️  Request data: {sample_payload_healthy}")
        start_time = time.time()
        response_healthy = requests.post(url, data = json.dumps(sample_payload_healthy))
        end_time = time.time()
        print(f"⬇️  Response: {response_healthy.text}")
        call_times.append(end_time - start_time)

        print("\n#######################################################\n")

        print(f"🚀 Making POST request 2 to {url}...")
        print(f"⬆️  Request data: {sample_payload_damaged}")
        start_time = time.time()
        response_damaged = requests.post(url, data = json.dumps(sample_payload_damaged))
        end_time = time.time()
        print(f"⬇️  Response: {response_damaged.text}")
        call_times.append(end_time - start_time)

    print(f"Average request time: {statistics.mean(call_times)} seconds")

simulate_requests(100)