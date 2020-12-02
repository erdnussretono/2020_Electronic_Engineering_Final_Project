#include <mega128.h>
#include <delay.h>
#include <stdio.h>

#ifndef RXB8
#define RXB8 1
#endif

#ifndef TXB8
#define TXB8 0
#endif

#ifndef UPE
#define UPE 2
#endif

#ifndef DOR
#define DOR 3
#endif

#ifndef FE
#define FE 4
#endif

#ifndef UDRE
#define UDRE 5
#endif

#ifndef RXC
#define RXC 7
#endif

#define FRAMING_ERROR (1<<FE)
#define PARITY_ERROR (1<<UPE)
#define DATA_OVERRUN (1<<DOR)
#define DATA_REGISTER_EMPTY (1<<UDRE)
#define RX_COMPLETE (1<<RXC)

#pragma used+
char getchar1(void)
{
char status,data;
while (1)
      {
      while (((status=UCSR1A) & RX_COMPLETE)==0);
      data=UDR1;
      if ((status & (FRAMING_ERROR | PARITY_ERROR | DATA_OVERRUN))==0)
         return data;
      }
}
#pragma used-

#pragma used+
void putchar1(char c)
{
while ((UCSR1A & DATA_REGISTER_EMPTY)==0);
UDR1=c;
}
#pragma used-

#define FIRST_ADC_INPUT 0
#define LAST_ADC_INPUT 1
unsigned int adc_data[LAST_ADC_INPUT-FIRST_ADC_INPUT+1];
#define ADC_VREF_TYPE 0x00

interrupt [ADC_INT] void adc_isr(void)
{
static unsigned char input_index=0;
adc_data[input_index]=ADCW;
if (++input_index > (LAST_ADC_INPUT-FIRST_ADC_INPUT))
   input_index=0;
ADMUX=(FIRST_ADC_INPUT | (ADC_VREF_TYPE & 0xff))+input_index;
delay_us(10);
ADCSRA|=0x40;
}
void main(void)
{
int LOW;
int HIGH;
PORTA=0x00;
DDRA=0x1E;

PORTB=0x00;
DDRB=0x14;

UCSR1A=0x00;
UCSR1B=0x18;
UCSR1C=0x06;
UBRR1H=0x00;
UBRR1L=0x67;

UCSR0A=0x00;
UCSR0B=0x18;
UCSR0C=0x06;
UBRR0H=0x00;
UBRR0L=0x67;

ADMUX=FIRST_ADC_INPUT | (ADC_VREF_TYPE & 0xff);
ADCSRA=0xCC;

#asm("sei")

PORTA=0x1E;

while (1)
      {
      LOW = adc_data[0];
      HIGH = adc_data[1];
        
      
      printf(" LOW LEVEL : %d , HIGH LEVEL : %d\n\r",LOW,HIGH);
                      
      LOW=adc_data[0];
      HIGH=adc_data[1];
       
      if(LOW < 50) 
      {
      PORTB=0x00;
      }
      if(HIGH>950)
      {
      PORTA.4=0x01;
      } 
      
      switch(getchar1())
      {
      case 'A':
        printf("Press A\n\r");
        if(HIGH<900)
        PORTA.4=0x00;
        printf("START Water IN!!\n\r");
        break;
      
      case'B':
        printf("Press B\n\r");
        if(LOW>900)
        {
        PORTB=0x14;   
        
        printf("START Water OUT!!\n\r");
        }
        else
        printf("Little Water\n\r");
        
        break;
        
      case 'C':
        printf("Press C\n\r");
        PORTA.3=0x00;
        delay_ms(500);
        PORTA.3=0x01;                     
        printf("FEED!!\n\r");
        break;
        
      case'D':
        printf("Press D\n\r");
        PORTA.1=0x00;
        printf("LED ON!!\n\r");
        
        break;                                     
        
        
      case 'E':
        printf("Press E\n\r");
        PORTA.1=0x01;
        printf("LED OFF!!\n\r");
        
        break;
      
      case 'F':
        printf("Press E\n\r");
        PORTA.2=0x00;
        printf("HITTER ON !!\n\r");
        
        break;
        
      case 'G':
        printf("Press G\n\r");
        PORTA.2=0x01;
        printf("HITTER OFF!!\n\r");
        break;
      }
      delay_ms(2000);
      }
}