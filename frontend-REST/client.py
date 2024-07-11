import os
import requests
import datetime
import json

import time

def main():
    time.sleep(10)
    # JSON a enviar al servidor
    data_dict = {"Texto":"the big lebowski", "FechaHora": datetime.datetime.now(), "Sistema": "REST", "Estado":0}
    # Request GET de prueba (no hace nada)
    requests.get('http://' + os.environ['SERVER_HOSTNAME'] + ':5000/')
    # Request POST para enviar el diccionario convertido a JSON hacia el servidor Flask
    requests.post('http://' + os.environ['SERVER_HOSTNAME'] + ':5000/', json=json.dumps(data_dict, indent=4, sort_keys=True, default=str))

if __name__ == "__main__":
    main()
