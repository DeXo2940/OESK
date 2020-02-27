#include <avr/io.h>
#include <util/delay.h>

#define OUTPUT 1
#define LED 2
#define INPUT 0

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
	
	setOutput(1);	//signal finished computing
	setLED(0);
	while( checkInput()); //active wait for start signal diapear
	setOutput(0);
}

void benchmark(){
	unsigned int primesArray[10000], i, j, foundPrimes = 0, isNotPrime;
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

int main(){
	unsigned int z;
	setup();	
	while(1){
		start();
		for(z=0;z<60000;z++) benchmark();
		finish();
	}
}
