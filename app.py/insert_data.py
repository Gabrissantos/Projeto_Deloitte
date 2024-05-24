import requests
from datetime import datetime, timedelta
import random
import time

url = 'http://localhost:5000/api/data'

# Função para gerar dados simulados
def generate_data(imei, status, offset_minutes):
    return {
        "imei": imei,
        "status": status,
        "last_report_minutes_ago": offset_minutes
    }

# Lista de IMEIs simulados
imeis = [f"1234567890{i:02d}" for i in range(1, 11)]

while True:
    data = []
    current_time = datetime.utcnow()

    for imei in imeis:
        rand_choice = random.randint(1, 5)
        if rand_choice == 1:
            # Inserir dados de poweron (0 a 30 minutos)
            data.append(generate_data(imei, "poweron", offset_minutes=random.randint(0, 30)))
        elif rand_choice == 2:
            # Inserir dados de poweroff (0 a 30 minutos)
            data.append(generate_data(imei, "poweroff", offset_minutes=random.randint(0, 30)))
        elif rand_choice == 3:
            # Inserir dados de inactive (31 minutos a 12 horas)
            data.append(generate_data(imei, "inactive", offset_minutes=random.randint(31, 720)))
        elif rand_choice == 4:
            # Inserir dados de warning (12 a 24 horas)
            data.append(generate_data(imei, "warning", offset_minutes=random.randint(721, 1440)))
        else:
            # Inserir dados de critical (mais de 24 horas)
            data.append(generate_data(imei, "critical", offset_minutes=random.randint(1441, 2880)))

    # Enviar todos os dados em uma única requisição
    response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    if response.status_code == 201:
        print("Data inserted successfully.")
    else:
        print("Failed to insert data.")
        print(f"Response code: {response.status_code}")
        print(f"Response content: {response.content}")

    print("Data insertion complete.")

    # Esperar por um período antes de inserir novos dados (por exemplo, 10 segundos)
    time.sleep(10)



