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