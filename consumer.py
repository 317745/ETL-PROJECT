from kafka import KafkaConsumer
from json import loads
import json
import time

consumer = KafkaConsumer(
    'streaming-dash',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: loads(v.decode('utf-8')),
    key_deserializer=lambda k: k.decode('utf-8') if k else None
)

# Archivo 
STATE_FILE = "stream_state.json"


state = {
    "investment-region": [],
    "investment-type": [],
    "investment-total-type": [],
    "total-discount-fnce": [],
    "avg-investment-year": [],
    "avg-investment-year-max": []
}

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

for message in consumer:
    key = message.key
    value = message.value

    # Si la key existe en el state → acumular el valor
    if key in state:
        state[key].append(value)   
        save_state()               

   
    if key == 'investment-region':
        print("Investment by Region:", value)

    elif key == 'investment-type':
        print("Investment by Type:", value)

    elif key == 'investment-total-type':
        print("Investment total by type:", value)

    elif key == 'total-discount-fnce':
        print("Total discount fnce:", value)

    elif key == "avg-investment-year":
        print("Avg investment by year:", value)

    elif key == "avg-investment-year-max":
        print("Max avg investment by year:", value)

    else:
        print(value)

    time.sleep(0.01)
