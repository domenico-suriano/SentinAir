#define N_CH0 2
#define N_CH1 50
#define N_CH2 50
#define N_S5 80
#define N_S6 80
#define N_S7 80
#define N_S8 80
#define N_S1 80
#define N_S3 80
#define N_S4 80
#define N_S2 80

//filtro1
static unsigned int32 preCH0[N_CH0];
static unsigned int32 preCH1[N_CH1];
static unsigned int32 preCH2[N_CH2];
static unsigned int32 preS5[N_S5];
static unsigned int32 preS6[N_S6];
static unsigned int32 preS7[N_S7];
static unsigned int32 preS8[N_S8];
static unsigned int32 preS1[N_S1];
static unsigned int32 preS3[N_S3];
static unsigned int32 preS4[N_S4];
static unsigned int32 preS2[N_S2];

void campionaCH0(unsigned int32 * vett,byte * numcamp)//A0
{
	set_adc_channel(0);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_CH0-1)) {(*(numcamp)) = 0;}
}


void campionaCH1(unsigned int32 * vett,byte * numcamp)//A1
{
	set_adc_channel(1);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_CH1-1)) {(*(numcamp)) = 0;}
}


void campionaCH2(unsigned int32 * vett,byte * numcamp)//A2
{
	set_adc_channel(2);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_CH2-1)) {(*(numcamp)) = 0;}
}


void campionaS5(unsigned int32 * vett,byte * numcamp)//A3-an3-ch1-s5-O3B4W
{
	set_adc_channel(3);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_S5-1)) {(*(numcamp)) = 0;}
}



void campionaS6(unsigned int32 * vett,byte * numcamp)//A5-an4-ch2-s6-O3B4A
{
	set_adc_channel(4);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
    if((*(numcamp))>(N_S6-1)) {(*(numcamp)) = 0;}
}

void campionaS7(unsigned int32 * vett,byte * numcamp)//E0-an5-ch3-s7-SO2B4A
{
	set_adc_channel(5);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_S7-1)) {(*(numcamp)) = 0;}
}

void campionaS8(unsigned int32 * vett,byte * numcamp)//E1-an6-ch4-s8-SO2B4W
{
	set_adc_channel(6);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_S8-1)) {(*(numcamp)) = 0;}
}

void campionaS1(unsigned int32 * vett,byte * numcamp)//E2-an7-ch5-s1-NO2B4A
{
	set_adc_channel(7);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_S1-1)) {(*(numcamp)) = 0;}
}

void campionaS3(unsigned int32 * vett,byte * numcamp)//B1-S3-CH7-an8-COB4A
{
	set_adc_channel(8);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_S3-1)) {(*(numcamp)) = 0;}
}

void campionaS4(unsigned int32 * vett,byte * numcamp)//B4-an9-ch8-s4-COB4W
{
	set_adc_channel(9);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_S4-1)) {(*(numcamp)) = 0;}
}

void campionaS2(unsigned int32 * vett,byte * numcamp)//B0-an10-ch6-s2-NO2B4W
{
	set_adc_channel(10);
	delay_ms(1);
	vett[*(numcamp)] = (int32)read_adc();
	(*(numcamp))++;
	if((*(numcamp))>(N_S2-1)) {(*(numcamp)) = 0;}
}

unsigned long filtro(unsigned int32 * vett, byte dim)
{
byte count;
unsigned int32 meas;
meas = 0;
for(count=0;count<dim;count++) meas = meas + vett[count];
meas = meas/(int32)dim;
return (unsigned long)meas;
}
