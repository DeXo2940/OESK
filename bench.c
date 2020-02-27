#include <avr/io.h>
#include <util/delay.h>

#define OUTPUT 1
#define LED 2
#define INPUT 0

int checkInput();
void setOutput(int status);
void setLED(int status);

void setup();
void start();
void finish();
void bench();

int main(){
	setup();	
	while(1){
		start();
		benchmark();
		finish();
	}
}

int checkInput(){
	return PIND & (1 << INPUT);
}

void setOutput(int status){
	if(status) PORTD |= (1 << OUTPUT);
	else PORTD &= ~(1 << OUTPUT);
}

void setLED(int status){
	if(status) PORTD |= (1 << LED);
	else PORTD &= ~(1 << LED);
}

void setup(){
	DDRD = 0x00;
	PORTD = 0x00;
	DDRD |= (1<<OUTPUT);
	DDRD |= (1<<LED);
	DDRD &= ~(1<<INPUT);
	PORTD &= ~(1<<INPUT);
}

void start(){
	while( !checkInput()); //active wait for start signal
	setLED(1);
}

void finish(){
	setLED(0);
	setOutput(1);	//signal finished computing
	setOutput(0);
	while( checkInput()); //active wait for start signal diapear
}

void benchmark(){
	unsigned int primesArray[10000];
	unsigned int i, j, foundPrimes = 0, isNotPrime;
	for(i=2;i<65535;i++){
		isNotPrime = 0;

		for(j=0;j<foundPrimes;j++){
			if(i%primesArray[j] == 0){
				isNotPrime = 1;
				break;
			}
		}
		if(isNotPrime == 0){
			primesArray[foundPrimes] = i;
			foundPrimes++;
		}
	}
}
