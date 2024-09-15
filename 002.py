import random
from datetime import datetime, timedelta

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


# Função para gerar temperaturas atuais
def generate_current_temperatures(start_time, num_points, interval_minutes):
    times = [start_time + timedelta(minutes=i * interval_minutes) for i in range(num_points)]
    temperatures = [random.uniform(15, 25) for _ in range(num_points)]  # Temperaturas simuladas
    return times, temperatures

# Função para prever a próxima temperatura
def predict_next_temperature(model, X):
    
    future_time = np.array([[X[-1][0] + 60]])  # Prevendo a próxima hora (60 minutos)
    return model.predict(future_time)[0]

# Gerar dados de exemplo
start_time = datetime.now()
num_points = 12  # 1 hora com intervalo de 5 minutos
interval_minutes = 5

current_times, current_temps = generate_current_temperatures(start_time, num_points, interval_minutes)

# Treinar um modelo simples para previsão usando temperaturas atuais
X = np.array([(i * interval_minutes) for i in range(num_points)]).reshape(-1, 1)
y = np.array(current_temps)
model = LinearRegression().fit(X, y)

# Configurar o gráfico
fig, ax = plt.subplots()
line1, = ax.plot(current_times, current_temps, label='Temperaturas Atuais')
line2, = ax.plot([], [], label='Temperaturas Futuras')
ax.legend()
ax.set_xlabel('Tempo')
ax.set_ylabel('Temperatura (°C)')
ax.set_title('Temperatura Futuras e Atuais')

def update_plot(frame):
    # Atualiza as temperaturas atuais
    new_current_times, new_current_temps = generate_current_temperatures(start_time, num_points, interval_minutes)
    
    # Treinar o modelo com novas temperaturas atuais
    X_new = np.array([(i * interval_minutes) for i in range(num_points)]).reshape(-1, 1)
    y_new = np.array(new_current_temps)
    model.fit(X_new, y_new)
    
    line1.set_xdata(new_current_times)
    line1.set_ydata(new_current_temps)
    
    # Prever a próxima temperatura
    next_temp = predict_next_temperature(model, X_new)
    future_time = current_times[-1] + timedelta(minutes=interval_minutes)
    current_times.append(future_time)
    current_temps.append(next_temp)
    
    line2.set_xdata(current_times)
    line2.set_ydata(current_temps)
    
    # Atualiza o gráfico
    ax.relim()
    ax.autoscale_view()
    
    return line1, line2

# Configura a animação
ani = animation.FuncAnimation(fig, update_plot, interval=1000, blit=True)

plt.show()
