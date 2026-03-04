import requests
import time
import json

def log_to_loki(label: str, trace_id: str, message: str):
    url = "http://localhost:3100/loki/api/v1/push"
    headers = {"Content-Type": "application/json"}
    log_entry = {
        "streams": [{
            "stream": { "app": label, "trace_id": trace_id },
            "values": [[str(int(time.time() * 1e9)), message]]
        }]
    }
    response = requests.post(url, data=json.dumps(log_entry), headers=headers)
    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == '__main__':
    log_to_loki("llm", "trace-123", "This is a test call for LOKI logging.")