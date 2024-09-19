// Definir o pino analógico onde o sensor de umidade do solo está conectado
const int sensorPin = A0;

// Definir o pino do relé onde a bomba está conectada
const int bombaPin = 7;

// Variável para armazenar o valor lido do sensor
int sensorValue = 0;

void setup() {
  // Iniciar a comunicação serial a 9600 bps
  Serial.begin(9600);
  // Configurar o pino da bomba como saída
  pinMode(bombaPin, OUTPUT);
}

void loop() {
  // Ler o valor analógico do sensor de umidade do solo
  sensorValue = analogRead(sensorPin);
  // Mapear os valores: 302 (seco) -> 0% e 172 (molhado) -> 100%
  int humidityPercent = map(sensorValue, 1023, 580, 0, 100);

  // Limitar os valores entre 0% e 100% para evitar valores fora da faixa
  humidityPercent = constrain(humidityPercent, 0, 100);

  // Exibir o valor do sensor no monitor serial
  Serial.println(humidityPercent);

  // Condição para ativar a bomba se a umidade estiver abaixo de um certo nível
  if (humidityPercent <= 30) {  // Defina o nível de umidade que você deseja
    digitalWrite(bombaPin, HIGH); // Ativar a bomba
  } else {
    digitalWrite(bombaPin, LOW);
  }

  // Aguardar um pouco antes da próxima leitura
  delay(1000);
}
