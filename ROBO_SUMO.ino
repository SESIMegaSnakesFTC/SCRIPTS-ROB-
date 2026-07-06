#include <ESP8266WiFi.h>
#include <WifiServer.h>
#include <ESP8266mDNS.h>

#define SSID "MegaSnakes"
#define PASS "Sesisp@31879"

//>>>MOTORES<<<

  //LeftMotor
const int IN1 = D1;
const int IN2 = D7;

  //RightMotor
const int IN3 = D6;
const int IN4 = D5;


WiFiServer Servidor(80);

void setup(){

  //>>>CONFIGURANDO ENTRADAS<<<
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT); 


  Serial.begin(115200);

  while(!Serial){
    delay(550);
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);

  while(WiFi.status() != WL_CONNECTED){

    Serial.print("*");
    delay(500);

  }

  Serial.println();
  Serial.print("Conectado com sucesso no IP:");
  Serial.println(WiFi.localIP());
  MDNS.begin("=>ESP8266<=");

}

void loop(){

  //>>>VERIFICAÇÃO DE CONEXÃO<<<

  WiFiClient cliente = Servidor.available();

  if(cliente){

    char value_func = cliente.read();

    Serial.println(value_func);

    cliente.flush();


    while (true){

    //>>>CONTROLAR ROBÔ<<<


      //>>>AVANÇAR<<<
      if( value_func == 'A'){

        advance();        

      }


      //>>>RECUAR<<<
      else if(value_func == 'B'){

        go_back();

      }


      //>>>DIREITA<<<
      else if(value_func == 'C'){

        Right();

      }


      //>>>ESQUERDA<<<
      else if(value_func == 'D'){

        Left();

      }

      //>>>PARAR<<<
      else{

        Stop();

      }

    }
  };
}


void advance(){

  //leftMotor
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  //RightMotor
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  delay(1000);

}

void go_back(){

  //leftMotor
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  //RightMotor
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  delay(1000);
  
}

void Right(){

  //leftMotor
  digitalWrite(IN1, LOW );
  digitalWrite(IN2, HIGH);

  //RightMotor
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  delay(700);

}

void Left(){

  //leftMotor
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  //RightMotor
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  delay(700);

}

void Stop(){

  //leftMotor
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  //RightMotor
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  delay(1000);
}
