/*
===============================================================================
 Name        : app.c
 Author      : Ing. Juan Manuel Cruz, Ing. Cesar Fuoco, Ing. Israel Pavelek
 Version     : 2.0
 Modified    : 9/29/2025
 Copyright   : $(copyright)
 Description : application definition
===============================================================================
*/
#include "main.h"
#include "filter.h"

/* Variables  ------------------------------------------------------------------*/
//Función que ejecuta > TALKTHROUGH / FIR / IIR
filter_type_t filter = IIR;

estado_t estado=NO_PROCESAR;
extern ADC_HandleTypeDef hadc1;
extern DAC_HandleTypeDef hdac;

//Filter Struct
arm_fir_instance_f32 SFIR;
arm_biquad_casd_df1_inst_f32 SIIR;

//Variables de estado
float32_t fir_state[FIR_TAP_NUM+SAMPLES_PER_BLOCK-1];
float32_t iir_state[IIR_TAP_NUM+SAMPLES_PER_BLOCK-1];

//Ping Pong Buffers
float32_t InputA[SAMPLES_PER_BLOCK]={0};
float32_t InputB[SAMPLES_PER_BLOCK]={0};
float32_t OutputA[SAMPLES_PER_BLOCK]={0};
float32_t OutputB[SAMPLES_PER_BLOCK]={0};

/* Filter Taps  ------------------------------------------------------------------*/
float32_t float_fir_taps[FIR_TAP_NUM] =
{
    1.0437117339e-03f,
    1.0764469034e-03f,
    1.1349955169e-03f,
    1.2205732866e-03f,
    1.3342425536e-03f,
    1.4769019274e-03f,
    1.6492769397e-03f,
    1.8519117922e-03f,
    2.0851622683e-03f,
    2.3491898728e-03f,
    2.6439572535e-03f,
    2.9692249507e-03f,
    3.3245495106e-03f,
    3.7092829884e-03f,
    4.1225738595e-03f,
    4.5633693426e-03f,
    5.0304191328e-03f,
    5.5222805297e-03f,
    6.0373249359e-03f,
    6.5737456916e-03f,
    7.1295672007e-03f,
    7.7026552941e-03f,
    8.2907287672e-03f,
    8.8913720187e-03f,
    9.5020487104e-03f,
    1.0120116360e-02f,
    1.0742841769e-02f,
    1.1367417188e-02f,
    1.1990977106e-02f,
    1.2610615554e-02f,
    1.3223403803e-02f,
    1.3826408345e-02f,
    1.4416709016e-02f,
    1.4991417157e-02f,
    1.5547693667e-02f,
    1.6082766845e-02f,
    1.6593949879e-02f,
    1.7078657866e-02f,
    1.7534424248e-02f,
    1.7958916542e-02f,
    1.8349951265e-02f,
    1.8705507932e-02f,
    1.9023742040e-02f,
    1.9302996955e-02f,
    1.9541814591e-02f,
    1.9738944833e-02f,
    1.9893353628e-02f,
    2.0004229672e-02f,
    2.0070989679e-02f,
    2.0093282154e-02f,
    2.0070989679e-02f,
    2.0004229672e-02f,
    1.9893353628e-02f,
    1.9738944833e-02f,
    1.9541814591e-02f,
    1.9302996955e-02f,
    1.9023742040e-02f,
    1.8705507932e-02f,
    1.8349951265e-02f,
    1.7958916542e-02f,
    1.7534424248e-02f,
    1.7078657866e-02f,
    1.6593949879e-02f,
    1.6082766845e-02f,
    1.5547693667e-02f,
    1.4991417157e-02f,
    1.4416709016e-02f,
    1.3826408345e-02f,
    1.3223403803e-02f,
    1.2610615554e-02f,
    1.1990977106e-02f,
    1.1367417188e-02f,
    1.0742841769e-02f,
    1.0120116360e-02f,
    9.5020487104e-03f,
    8.8913720187e-03f,
    8.2907287672e-03f,
    7.7026552941e-03f,
    7.1295672007e-03f,
    6.5737456916e-03f,
    6.0373249359e-03f,
    5.5222805297e-03f,
    5.0304191328e-03f,
    4.5633693426e-03f,
    4.1225738595e-03f,
    3.7092829884e-03f,
    3.3245495106e-03f,
    2.9692249507e-03f,
    2.6439572535e-03f,
    2.3491898728e-03f,
    2.0851622683e-03f,
    1.8519117922e-03f,
    1.6492769397e-03f,
    1.4769019274e-03f,
    1.3342425536e-03f,
    1.2205732866e-03f,
    1.1349955169e-03f,
    1.0764469034e-03f,
    1.0437117339e-03f
};

/*
float32_t float_iir_taps[IIR_TAP_NUM] =
{
    // SOS 1
    3.64382755e-12f,
    7.28765510e-12f,
    3.64382755e-12f,
    0.995462872f,
    0.0f,

    // SOS 2
    1.0f,
    2.0f,
    1.0f,
    1.99256371f,
   -0.992669244f,

    // SOS 3
    1.0f,
    1.0f,
    0.0f,
    1.99695013f,
   -0.997193640f
};
*/
float32_t float_iir_taps[IIR_TAP_NUM] =
{
     0.99992147f,    // b0
    -1.99978125f,    // b1
     0.99992147f,    // b2
     1.99978125f,    // -a1
    -0.99984293f     // -a2
};

/* main loop ------------------------------------------------------------------*/

void app_init(void){
	/* Start adc & timer */
	HAL_ADC_Start_IT(&hadc1);
	HAL_TIM_Base_Start_IT(&htim2);
	HAL_DAC_Start(&hdac,DAC_CHANNEL_1);

  // Inicializa los filtros
	arm_fir_init_f32(&SFIR,FIR_TAP_NUM,float_fir_taps,fir_state,SAMPLES_PER_BLOCK);
	arm_biquad_cascade_df1_init_f32(&SIIR,IIR_SOS_NUM,float_iir_taps,iir_state);
}

void app_update(void){
	if(estado!=NO_PROCESAR){
		switch (filter){

			case TALKTHROUGH:
					for(uint16_t i=0;i<SAMPLES_PER_BLOCK;i++){
						if(estado==PROCESAR_A)OutputA[i]=InputA[i];
						else OutputB[i]=InputB[i];
					}
					break;

			case FIR:
					if(estado==PROCESAR_A){
						arm_fir_f32(&SFIR,InputA, OutputA, SAMPLES_PER_BLOCK);
					}else {
						arm_fir_f32(&SFIR,InputB, OutputB , SAMPLES_PER_BLOCK);
					}
					break;

			case IIR:
					if(estado==PROCESAR_A){
						arm_biquad_cascade_df1_f32(&SIIR, InputA, OutputA, SAMPLES_PER_BLOCK);
					}else {
						arm_biquad_cascade_df1_f32(&SIIR, InputB, OutputB, SAMPLES_PER_BLOCK);
						}
					break;

			default:break;

		}
		estado=NO_PROCESAR;
	}
}

//ADC Callback
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc){
	static bool estadoADC = CARGANDO_A;
	static uint16_t index = 0;
	uint32_t val=HAL_ADC_GetValue(&hadc1);

	if (estadoADC==CARGANDO_A){
		InputA[index] =(float32_t)val;
		InputA[index] = InputA[index] - 2048;
		HAL_DAC_SetValue(&hdac,DAC_CHANNEL_1,DAC_ALIGN_12B_R,OutputA[index]+2048);

	}
	else {
		InputB[index] =(float32_t) val ;
		InputB[index] = InputB[index] - 2048;
		HAL_DAC_SetValue(&hdac,DAC_CHANNEL_1,DAC_ALIGN_12B_R,OutputB[index]+2048);
	}
	index++;
	if (index == SAMPLES_PER_BLOCK) {
		index = 0;
		if(estadoADC==CARGANDO_A)
			estado=PROCESAR_A;
		else
			estado=PROCESAR_B;
		estadoADC ^= 1;
	}
    //HAL_GPIO_TogglePin(Test_GPIO_Port, Test_Pin);
}




