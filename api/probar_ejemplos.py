import json
from pathlib import Path

import requests

URL = "http://127.0.0.1:8000"

ejemplos = json.loads((Path(__file__).parent / "ejemplos.json").read_text(encoding="utf-8"))

print("health:", requests.get(f"{URL}/health").json())

for nombre, empleado in ejemplos.items():
    respuesta = requests.post(f"{URL}/predict", json=empleado).json()
    print(nombre, "->", respuesta)
