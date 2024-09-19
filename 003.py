from datetime import datetime, timedelta
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import serial
from sklearn.linear_model import LinearRegression

# Configuração da porta serial
ser = serial.Serial('COM5', 9600)

# Função para ler dados de umidade do Arduino
def read_humidity_from_arduino():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"Lido: {line}")  # Para depuração
        try:
            return float(line) + float(1)  # Ajuste se necessário
        except ValueError:
            return None
    return None

# Função para prever a próxima umidade
def predict_next_humidity(model, X):
    future_time = np.array([[X[-1][0] + 60]])  # Prevendo a próxima hora (60 minutos)
    return model.predict(future_time)[0]

# Gerar dados de exemplo
start_time = datetime.now()
num_points = 12  # 1 hora com intervalo de 5 minutos
interval_minutes = 5

current_times = []
current_humidities = []
future_times = []
future_humidities = []

# Coletar leituras de umidade iniciais
for _ in range(num_points):
    humidity = read_humidity_from_arduino()
    if humidity is not None:
        current_humidities.append(humidity)
        current_times.append(start_time + timedelta(minutes=len(current_times) * interval_minutes))

# Inicializar o modelo se houver dados suficientes
model = None
if len(current_humidities) > 1:
    X = np.array([(i * interval_minutes) for i in range(len(current_humidities))]).reshape(-1, 1)
    y = np.array(current_humidities)
    model = LinearRegression().fit(X, y)

# Configurar o gráfico
fig, ax = plt.subplots()
line1, = ax.plot(current_times, current_humidities, label='Umidade Atual', color='blue')  # Linha de umidade atual
line2, = ax.plot([], [], label='Umidade Prevista', color='orange')  # Linha de umidade prevista
ax.legend()
ax.set_xlabel('Tempo')
ax.set_ylabel('Umidade (%)')
ax.set_title('Umidade Futuras e Atuais')

def update_plot(frame):
    global model  # Declare model as global

    new_humidity = read_humidity_from_arduino()
    if new_humidity is not None:
        # Atualiza o tempo e a umidade atuais
        if current_times:
            new_time = current_times[-1] + timedelta(minutes=interval_minutes)
        else:
            new_time = datetime.now()

        current_times.append(new_time)
        current_humidities.append(new_humidity)

        # Treinar o modelo se houver dados suficientes
        if model is None and len(current_humidities) > 1:
            X_new = np.array([(i * interval_minutes) for i in range(len(current_humidities))]).reshape(-1, 1)
            y_new = np.array(current_humidities)
            model = LinearRegression().fit(X_new, y_new)
        elif model is not None:
            X_new = np.array([(i * interval_minutes) for i in range(len(current_humidities))]).reshape(-1, 1)
            y_new = np.array(current_humidities)
            model.fit(X_new, y_new)

            # Atualiza a linha de umidade atual
            line1.set_xdata(current_times)
            line1.set_ydata(current_humidities)

            # Prever a próxima umidade
            next_humidity = predict_next_humidity(model, X_new)
            future_time = current_times[-1] + timedelta(minutes=interval_minutes)
            future_times.append(future_time)
            future_humidities.append(next_humidity)
            current_times.append(new_time)
            current_humidities.append(new_humidity)
            # Atualiza a linha de umidade prevista
            line2.set_xdata(future_times)
            line2.set_ydata(future_humidities)

    # Atualiza o gráfico
    ax.relim()
    ax.autoscale_view()

    return line1, line2

# Configura a animação
ani = animation.FuncAnimation(fig, update_plot, interval=1000, blit=True)

plt.show()
