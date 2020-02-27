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
	setOutput(1);	//signal finished counting
	setOutput(0);
	while( checkInput()); //active wait for start signal diapear
}

void benchmark(){
	int i;	
	_delay_ms(3000);	
}