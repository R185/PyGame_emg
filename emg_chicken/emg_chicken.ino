int emg0 = 0; //переменные для хранения значений с датчиков
int emg1 = 0;
int amp0 = 0; //переменные для хранения значений амплитуды ЭМГ-сигнала
int amp1 = 0;
int min0 = 255; //переменные для хранения минимальных и максимальных значений ЭМГ-сигнала
int max0 = 0;
int min1 = 255;
int max1 = 0;

void calc_amp(){  //функция для вычисления амплитуды ЭМГ-сигнала
  for (int k = 0; k < 32; k ++){  //выполняем нижеописанный алгоритм 32 раза
    emg0 = map(analogRead(A0), 0, 1023, 0, 255);  //считываем значения с датчиков и приводим их в диапазон от 0 до 255
    emg1 = map(analogRead(A1), 0, 1023, 0, 255);
    if (emg0 < min0) min0 = emg0;   //находим минимальные и максимальные значения ЭМГ-сигнала
    if (emg0 > max0) max0 = emg0;
    if (emg1 < min1) min1 = emg1;
    if (emg1 > max1) max1 = emg1;
  }
  amp0 = 0.3 * amp0 + 0.7 * (max0 - min0);  //вычисляем амплитуду ЭМГ-сигнала, также учитываем предыдущее значение для сглаживания сигнала
  amp1 = 0.3 * amp1 + 0.7 * (max1 - min1);  
  //Serial.print(amp0);  //выводим значения амлитуды в Serial порт
  //Serial.print("   ");
  //Serial.println(amp1);
  min0 = 255;   //приводим максимальные и минимальные значения в изначальное состояние 
  max0 = 0;
  min1 = 255;
  max1 = 0;
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  calc_amp();
  if(amp1 > 30) {
    Serial.println("2.1");
  }
  else {
    Serial.println("2.0");

  }
  if(amp0 > 30) {
    Serial.println("1.1");
  }
  else {
    Serial.println("1.0");
  }
}
