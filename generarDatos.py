import pandas as pd
import random
from datetime import datetime

###### Actividad 3 - Métodos de aprendizaje supervisado #######
#### Jorge Eduardo Amaya Narvaez #####
#### Wilson Fabian Fonnegra Gomez #####
#### Jorge Asdrubal Ortega Gonzalez #####

n_dias = 30
horas_operativas = list(range(4, 24))
origenes = ['Terminal Norte', 'Terminal Sur', 'Centro', 'Estación Este', 'Estación Oeste']
destinos = ['Zona Industrial', 'Universidad', 'Aeropuerto', 'Estación Central', 'Barrio Alto']
condiciones_trafico = ['normal', 'moderado', 'colapsado']

datos = []

for dia in range(n_dias):
    for hora_num in horas_operativas:
        hora_formateada = datetime.strptime(str(hora_num), "%H").strftime("%I:00 %p")

        if hora_num in range(6, 10) or hora_num in range(17, 20):
            trafico = random.choices(condiciones_trafico, weights=[0.1, 0.3, 0.6])[0]
            cantidad_pasajeros = random.randint(700, 1700)
            cantidad_buses = random.randint(20, 30)
        elif hora_num in range(4, 6) or hora_num in range(22, 24):
            trafico = random.choices(condiciones_trafico, weights=[0.7, 0.2, 0.1])[0]
            cantidad_pasajeros = random.randint(150, 300)
            cantidad_buses = random.randint(5, 10)
        else:
            trafico = random.choices(condiciones_trafico, weights=[0.4, 0.4, 0.2])[0]
            cantidad_pasajeros = random.randint(300, 700)
            cantidad_buses = random.randint(8, 20)

        if trafico == 'normal':
            tiempo_viaje = random.randint(20, 30)
        elif trafico == 'moderado':
            tiempo_viaje = random.randint(30, 45)
        else:  # colapsado
            tiempo_viaje = random.randint(45, 70)

        origen = random.choice(origenes)
        destino = random.choice([d for d in destinos if d != origen])

        datos.append({
            'dia': dia + 1,
            'hora': hora_formateada,
            'hora_num': hora_num,
            'trafico': trafico,
            'cantidad_buses': cantidad_buses,
            'cantidad_pasajeros': cantidad_pasajeros,
            'tiempo_viaje': tiempo_viaje,
            'origen': origen,
            'destino': destino
        })

df = pd.DataFrame(datos)
df.to_csv("datos_transporte.csv", index=False)
print("✅ Nuevo dataset generado y guardado como 'datos_transporte.csv'")