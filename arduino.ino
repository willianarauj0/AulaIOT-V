#include <DHT.h>

#define DHTPIN 2          // Pino de dados do sensor DHT
#define DHTTYPE DHT11     // Tipo do sensor (DHT11 ou DHT22)

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature(); // Lê a temperatura em Celsius

  if (isnan(temperature)) {
    Serial.println("Erro ao ler o sensor.");
  } else {
    Serial.println(temperature);
  }

  delay(5000); // Aguarda 5 segundos antes de ler novamente
}
