import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
import time
import sys

def efecto_carga(etapa, delay=0.7):
    """Simula el efecto de carga con puntos suspensivos."""
    print(f"{etapa}..", end="")
    for _ in range(3):
        time.sleep(delay)
        print(".", end="", flush=True)
    print()

efecto_carga("🔄 Cargando los datos")
df = pd.read_csv('datos_transporte.csv')

df['trafico_normal'] = df['trafico'].apply(lambda x: 1 if x == 'normal' else 0)
df['trafico_moderado'] = df['trafico'].apply(lambda x: 1 if x == 'moderado' else 0)
df['trafico_colapsado'] = df['trafico'].apply(lambda x: 1 if x == 'colapsado' else 0)

X = df[['hora_num', 'cantidad_buses', 'trafico_normal', 'trafico_moderado', 'trafico_colapsado']]
y = df[['tiempo_viaje', 'cantidad_pasajeros']]


efecto_carga("🔧 Entrenando el modelo")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

efecto_carga("📊 Evaluando el modelo")
y_pred = modelo.predict(X_test)
mae_tiempo = mean_absolute_error(y_test['tiempo_viaje'], y_pred[:, 0])
mae_pasajeros = mean_absolute_error(y_test['cantidad_pasajeros'], y_pred[:, 1])

print("📊 Evaluación del Modelo:")
print(f"📉 Error medio absoluto (tiempo de viaje): {mae_tiempo:.2f} min")
print(f"👥 Error medio absoluto (cantidad de pasajeros): {mae_pasajeros:.2f} pasajeros")


efecto_carga("🔮 Realizando predicciones para cada hora")
resultados_prediccion = []

for hora in range(4, 23):  # De 4 AM a 11 PM
    if hora in range(6, 10) or hora in range(17, 20):
        # Hora pico
        buses = 25
        trafico = [0, 0, 1]
    elif hora in range(4, 6) or hora in range(22, 23):
        # Hora suave
        buses = 4
        trafico = [1, 0, 0]
    else:
        # Hora intermedia
        buses = 12
        trafico = [0, 1, 0]

    entrada = pd.DataFrame([[hora, buses, *trafico]], columns=[
        'hora_num', 'cantidad_buses', 'trafico_normal', 'trafico_moderado', 'trafico_colapsado'
    ])

    entrada_scaled = scaler.transform(entrada)
    pred = modelo.predict(entrada_scaled)

    pasajeros = pred[0][1]
    tiempo = pred[0][0]
    pasajeros_por_bus = round(pasajeros / buses)  
    score = tiempo + pasajeros_por_bus * 10

    resultados_prediccion.append({
        'hora': hora,
        'tiempo_viaje': round(tiempo), 
        'pasajeros': round(pasajeros), 
        'pasajeros_por_bus': pasajeros_por_bus,
        'score_total': score
    })

df_resultados = pd.DataFrame(resultados_prediccion)
mejor_hora = df_resultados.loc[df_resultados['score_total'].idxmin()]
peor_hora = df_resultados.loc[df_resultados['score_total'].idxmax()]

efecto_carga("📊 Analizando los resultados históricos")
resumen_historico = df.groupby('hora_num').agg({
    'cantidad_pasajeros': 'mean',
    'cantidad_buses': 'mean',
    'tiempo_viaje': 'mean'
}).reset_index()

resumen_historico['pasajeros_por_bus'] = resumen_historico['cantidad_pasajeros'] / resumen_historico['cantidad_buses']
resumen_historico['pasajeros_por_bus'] = resumen_historico['pasajeros_por_bus'].round()  # Redondeamos los pasajeros por bus
hora_pico = resumen_historico.loc[resumen_historico['pasajeros_por_bus'].idxmax()]
hora_suave = resumen_historico.loc[resumen_historico['pasajeros_por_bus'].idxmin()]

# ========== RESULTADOS ==========

def formatear_hora(h):
    from datetime import datetime
    h = int(h) 
    return datetime.strptime(str(h), "%H").strftime("%I:00 %p")

print("\n📈 Análisis Histórico del Sistema de Transporte:")
print(f"🔴 Hora más pico históricamente: {formatear_hora(hora_pico['hora_num'])}")
print(f"    - Pasajeros por bus: {hora_pico['pasajeros_por_bus']}")
print(f"    - Tiempo promedio de viaje: {round(hora_pico['tiempo_viaje'], 1)} min")

print(f"\n🟢 Hora más suave históricamente: {formatear_hora(hora_suave['hora_num'])}")
print(f"    - Pasajeros por bus: {hora_suave['pasajeros_por_bus']}")
print(f"    - Tiempo promedio de viaje: {round(hora_suave['tiempo_viaje'], 1)} min")

print("\n📅 Recomendación para el próximo día:")
print(f"✅ Mejor hora para viajar: {formatear_hora(mejor_hora['hora'])}")
print(f"    - Tiempo estimado: {round(mejor_hora['tiempo_viaje'], 1)} min")
print(f"    - Pasajeros por bus: {mejor_hora['pasajeros_por_bus']}")

print(f"\n⚠️ Peor hora para viajar: {formatear_hora(peor_hora['hora'])}")
print(f"    - Tiempo estimado: {round(peor_hora['tiempo_viaje'], 1)} min")
print(f"    - Pasajeros por bus: {peor_hora['pasajeros_por_bus']}")