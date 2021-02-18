//creato il 14/3/2018
#include <18F4685.h>
#device ADC=16 //RISOLUZIONE ADC
#fuses HS,NOWDT,NOPROTECT,NOLVP,BROWNOUT
#use delay(clock=10M)
#use rs232(baud=115200, xmit=PIN_C6, rcv=PIN_C7, timeout = 1500, errors, stream=usb)

#include "C:\progetti\firmware-multisensori\sensori.h"

#define IDENTITY "LCSS\r\n"
#define BUFFER_LENGHT 10

static byte buffer_index;
static byte buffer_counter;
static byte usb_buffer_pointer;
static BYTE usb_rx_buf[BUFFER_LENGHT];

static float misure[11];

////////////////////////////////////////////////////////////////////////////
////// FORMATO PACCHETTI IN USCITA /////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

void invia_misure_ASCII_usb(float * mis)
{
fprintf(usb,"%4.4f;%4.4f;%4.4f;%4.4f;%4.4f;%4.4f;%4.4f;%4.4f;%3.1f;%3.1f;%2.3f\r\n",
	mis[1],mis[2],mis[3],mis[4],mis[5],mis[6],mis[7],mis[8],mis[9],mis[10],mis[0]);
}


void invia_HEADER_USB()
{
disable_INTERRUPTS(INT_RDA);
fprintf(usb,"s1[v];s2[v];s3[v];s4[v];s5[v];s6[v];s7[v];s8[v];t[c];rh[%%];pwr[v]\r\n");
enable_INTERRUPTS(INT_RDA);
}

////////////////////////////////////////////////////////////////////////////
//////GESTIONE COMUNICAZIONI CON CPU////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
#int_rda
void rb0_isr()
{
disable_INTERRUPTS(INT_RDA);
usb_rx_buf[buffer_index]=fgetc(usb);
buffer_index++;
if(buffer_index==BUFFER_LENGHT) buffer_index = 0;
enable_INTERRUPTS(INT_RDA);
}


////////////////////////////////////////////////////////////////////////////
///////////////////////////MAIN///////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
void main()
{
byte stepS5;
byte stepS6;
byte stepS7;
byte stepS8;
byte stepS1;
byte stepS3;
byte stepS4;
byte stepS2;
byte stepT;
byte stepRH;
byte stepPWR;
unsigned long sensCH0;
unsigned long sensCH1;
unsigned long sensCH2;
unsigned long sensS5;
unsigned long sensS6;
unsigned long sensS7;
unsigned long sensS8;
unsigned long sensS1;
unsigned long sensS3;
unsigned long sensS4;
unsigned long sensS2;
float tempBias;
float tempSens;
float RHBias;
float RHsens;
float V33;
float pwr33V;
port_b_pullups(true);
enable_INTERRUPTS(INT_RDA);
enable_interrupts(GLOBAL);

init:
buffer_index = 0;
buffer_counter = 0;
setup_adc_ports(ALL_ANALOG);
setup_adc(ADC_CLOCK_INTERNAL);

stepS5 = 0;
stepS6 = 0;
stepS7 = 0;
stepS8 = 0;
stepS1 = 0;
stepS3 = 0;
stepS4 = 0;
stepS2 = 0;
stepT = 0;
stepRH = 0;
stepPWR = 0;

tempBias=0.5;
tempSens=100;
RHBias=0.1515;
RHsens=157.23270440251572327044025157233;


ciclo:
if(buffer_index!=buffer_counter)
{
	if(buffer_index==0){usb_buffer_pointer = BUFFER_LENGHT-1;}
	else{usb_buffer_pointer = buffer_index-1;}
	switch ( usb_rx_buf[usb_buffer_pointer] ) {
	case 'i':
		disable_INTERRUPTS(INT_RDA);
		fprintf(usb,IDENTITY);
		enable_INTERRUPTS(INT_RDA);
		break;
	case 'h':
		disable_INTERRUPTS(INT_RDA);
		invia_HEADER_USB();
		enable_INTERRUPTS(INT_RDA);
		break;
	case 'g':
		disable_INTERRUPTS(INT_RDA);
		invia_misure_ASCII_usb(misure);
		enable_INTERRUPTS(INT_RDA);
		break;
	}
	buffer_counter = buffer_index;
}

campionaCH0(preCH0,&stepPWR);
campionaCH1(preCH1,&stepT);
campionaCH2(preCH2,&stepRH);
campionaS5(preS5,&stepS5);
campionaS6(preS6,&stepS6);
campionaS7(preS7,&stepS7);
campionaS8(preS8,&stepS8);
campionaS1(preS1,&stepS1);
campionaS3(preS3,&stepS3);
campionaS4(preS4,&stepS4);
campionaS2(preS2,&stepS2);

sensCH0 = filtro(preCH0,N_CH0);
sensCH1 = filtro(preCH1,N_CH1);
sensCH2 = filtro(preCH2,N_CH2);
sensS5 = filtro(preS5,N_S5);
sensS6 = filtro(preS6,N_S6);
sensS7 = filtro(preS7,N_S7);
sensS8 = filtro(preS8,N_S8);
sensS1 = filtro(preS1,N_S1);
sensS3 = filtro(preS3,N_S3);
sensS4 = filtro(preS4,N_S4);
sensS2 = filtro(preS2,N_S2);


//3.47/2^16=0.000055694580078125
//3.26/2^16=0.00004974365234375
//3.3/2^16=0.00005035400390625
//3.28/2^16=0.000050048828125
//3.27/2^16=0.000049896240234375
V33 = 0.000049896240234375;
pwr33V = 3.27;
misure[0]=(float)sensCH0*V33*1.9864011656143759106362311801846; //0,000052490234375 //0.0000531005859375
misure[9]=(((float)sensCH1*V33)-tempBias)*tempSens;//0.5;100
misure[10]= ((((float)sensCH2 *V33)/pwr33V)-RHBias)*RHsens;//0.1515;1/0.00636=157.23270440251572327044025157233
misure[5]=(float)sensS5*V33;
misure[6]=(float)sensS6*V33;
misure[7]=(float)sensS7*V33;
misure[8]=(float)sensS8*V33;
misure[1]=(float)sensS1*V33;
misure[3]=(float)sensS3*V33;
misure[4]=(float)sensS4*V33;
misure[2]=(float)sensS2*V33;

goto ciclo;
}
