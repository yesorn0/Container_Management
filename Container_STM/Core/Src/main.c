/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * Copyright (c) 2025 STMicroelectronics.
 * All rights reserved.
 *
 * This software is licensed under terms that can be found in the LICENSE file
 * in the root directory of this software component.
 * If no LICENSE file comes with this software, it is provided AS-IS.
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "dma.h"
#include "i2c.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "led.h"
#include "sensor.h"
#include "dht11.h"
#include <string.h>

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

// 온도 경계값 (20 ~ 25도), 습도 경계값 (35 ~ 45%)
#define TEMP_MAX 27
#define TEMP_MIN 25

#define HUMI_MAX 30
#define HUMI_MIN




#ifdef __GNUC__
/* With GCC small printf (option LD Linker->Libraries->Small printf
 * set to 'Yes') calls __io_putchar() */
#define PUTCHAR_PROTOTYPE int  __io_putchar(int ch)
#else
#define PUTCHAR_PROTOTYPE int  fputc(int ch, FILE *f)
#endif /* __GNUC__*/

/** @brief Retargets the C library printf function to the USART.
 *  @param None
 *  @retval None
 */
PUTCHAR_PROTOTYPE
{
	/* Place your implementation of fputc here */
	/* e.g. write a character to the USART2 and Loop
     until the end of transmission */
	if(ch == '\n')
		HAL_UART_Transmit(&huart2, (uint8_t*) "\r", 1, 0xFFFF);
	HAL_UART_Transmit(&huart2, (uint8_t*) &ch, 1, 0xFFFF);
}

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
DHT11 dht1;
DHT11 dht2;
DHT_THRES dht_thr;
volatile uint8_t dht_readFLAG = 0;
volatile uint8_t adc_readFLAG = 0;
volatile uint8_t trans_FLAG = 0;
volatile uint8_t cnt = 0;

volatile uint8_t second_FLAG = 0; // 1초마다 1씩 증가되는 시스템 1초

volatile uint8_t fire_timer_running = 0; // 불꽃감지되면 1이 되어서 3초 셀수있게하는 flag
volatile uint8_t fire_timer_count = 0; // 3초를 카운트하는 변수


uint8_t led_update_time = 0;
uint8_t led_step = 0; // 1초마다 led 단계 증가할 수 있게

char recv_data[6] = "-----";   // 수신 받은 데이터

volatile uint16_t adcValue[3]; // adc값 저장 배열

uint8_t FIRE_flag = 0;
uint16_t FIRE_value = 0;
uint16_t WATER_Leftvalue = 0;
uint16_t WATER_Rightvalue = 0;



/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

// (온습도-500ms), (수위, 불꽃-100ms), (전송-500ms)
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
	if(htim->Instance == TIM9) // 100ms마다 타이머 인터럽트 발생
	{
		adc_readFLAG = 1;
		dht_readFLAG = (cnt % 5 == 0) ? 1 : 0;
		trans_FLAG = (cnt % 5 == 0) ? 1 : 0;

		cnt++;
	}

	// 시스템 전체의 s를 세고있음
	else if(htim->Instance == TIM4) // 1s마다 타이머 인터럽트 발생
	{
		second_FLAG = (second_FLAG + 1) % 256;

		if(fire_timer_running)
		{
			fire_timer_count++;

			if(fire_timer_count >= 3)
			{
				HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, RESET); // 3초 후 가습기 OFF
				fire_timer_running = 0;
				fire_timer_count = 0;
			}
		}
	}
}


/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_TIM11_Init();
  MX_USART2_UART_Init();
  MX_I2C1_Init();
  MX_ADC1_Init();
  MX_USART1_UART_Init();
  MX_TIM3_Init();
  MX_TIM9_Init();
  MX_TIM4_Init();
  /* USER CODE BEGIN 2 */

    // 사용센서 : 블루투스, 온습도 2개, 선풍기, FAN, 수위센서, 불꽃감지센서, 바 LED

    char trans_msg[55];

    printf("STM32 start\n");

    HAL_UART_Receive_DMA(&huart1, recv_data, 6);

    DHT_thres_init(&dht_thr); // 온습도 경계값 초기화
	dht11Init(&dht1, GPIOB, GPIO_PIN_4, &htim11); // 온습도 초기화
	dht11Init(&dht2, GPIOB, GPIO_PIN_5, &htim11);

	HAL_ADC_Start_DMA(&hadc1, adcValue, 3); // 수위센서, 불꽃감지센서 초기화

	HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1); // 선풍기 초기화

	HAL_TIM_Base_Start_IT(&htim4);	// 1s 주기로 타이머 인터럽트 발생
	HAL_TIM_Base_Start_IT(&htim9);  // 100ms 주기로 타이머 인터럽트 발생

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	while (1)
	{
		// 수신
		printf("recv : %s\n", recv_data);
		DHT_parse(&dht_thr, recv_data);

		// 온습도 경계값 출력
		printf("[thres] T1:%d, H1:%d, T2:%d, H2:%d\n", dht_thr.T1, dht_thr.H1, dht_thr.T2, dht_thr.H2);


		if(adc_readFLAG)
		{
			// 불꽃감지(ADC4), 수위센서(ADC5, ADC6)
			FIRE_value = FIRE_check();
			if(FIRE_value >= 500) // 불꽃 감지 됨
				FIRE_flag = 1;
			else
				FIRE_flag = 0;



			printf("fire : %4d, flag : %d\r\n", FIRE_value, FIRE_flag);


			WATER_Leftvalue = WATER_Leftcheck();
			printf("water_Left : %4d\r\n", WATER_Leftvalue);

			WATER_Rightvalue = WATER_Rightcheck();
			printf("water_right : %4d\r\n", WATER_Rightvalue);

			adc_readFLAG = 0;
		}


		if(FIRE_flag == 1)
		{
		    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, SET); // 가습기 on
		    fire_timer_running = 1;                    // 타이머 활성화
		    fire_timer_count = 0;                      // 타이머 초기화 (다시 3초 측정)
		}


		if(dht_readFLAG)
		{
			// 측정
			// 온습도 1 (해당 온습도로 선풍기, FAN 동작하도록)
			if(dht11Read(&dht1))
			{
				printf("dht1 => Temp : %d C, Hum : %d %%\r\n", dht1.temperature, dht1.humidity);
			}
			// 온습도 2 (여기는 그냥 온습도 출력만)
			if(dht11Read(&dht2))
			{
				printf("dht2 => Temp : %d C, Hum : %d %%\r\n", dht2.temperature, dht2.humidity);
			}


			// 온도 경계값 (20 ~ 25도), 습도 경계값 (35 ~ 45%)


			// 온도
			if(dht1.temperature > dht_thr.T1 + 2) // 온도가 경계값보다 큰가?
			{
				PINWHEEL_on(); // 선풍기 ON
				LED1_off();
			}
			else if(dht1.temperature < dht_thr.T1 - 2) // 온도가 경계값보다 낮은가?
			{
				PINWHEEL_off(); // 선풍기 off
//				static uint8_t cnt = 0;
//				cnt++;
//				if(cnt == 2)
//				{
//					cnt = 0;
//					led_step = (led_step % 4) + 1;  // 1단 ~ 4단
//
//					LED1_on(led_step); // LED ON (히터)
//				}
				if(second_FLAG != led_update_time)
				{
					led_update_time = second_FLAG; // 현재의 초로 초기화
					led_step = (led_step % 4) + 1;  // 1단 ~ 4단

					LED1_on(led_step); // LED ON (히터)
				}
			}
			else
			{
				LED1_off(); // LED OFF (히터)
				PINWHEEL_off(); // 선풍기 off
				led_step = 0;
			}



			// 습도
			if(dht1.humidity > dht_thr.H1 + 10)
			{
				FAN_on(); // FAN ON
				HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, RESET); // 가습기 OFF
			}
			else if(dht1.humidity < dht_thr.H1 - 5)
			{
				HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, SET); // 가습기 ON
				FAN_off(); // FAN OFF
			}
			else
			{
				FAN_off(); // FAN OFF
				HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, RESET); // 가습기 OFF
			}


			LED2_off();
			dht_readFLAG = 0; // 새로운 온습도 값을 받아올 수 있게
		}



		// 가습기 센서
//		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, SET);
//		HAL_Delay(1000);
//		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, RESET);
//		HAL_Delay(1000);


		// bar LED (원하는 단수 입력{1단, 2단, 3단, 4단}) - 0단은 off
//		for(uint8_t i=1; i<=4; i++)
//		{
//			LED1_on(i);
//			HAL_Delay(500);
//			LED2_on(i);
//			HAL_Delay(500);
//		}
		//LED1_off();
		//HAL_Delay(500);
		//LED2_off();
		//HAL_Delay(500);



		// 선풍기
//		PINWHEEL_on();
//		HAL_Delay(2000);
//		PINWHEEL_off();
//		HAL_Delay(2000);


		// FAN
//		FAN_on();
//		HAL_Delay(2000);
//		FAN_off();
//		HAL_Delay(2000);




		if(trans_FLAG)
		{
			// 블루투스 송신 : stm -> 라즈베리파이
			sprintf(trans_msg, "T1:%2d, H1:%2d, T2:%2d, H2:%2d, F:%d, LW:%4d, RW:%4d\n",
					dht1.temperature, dht1.humidity, dht2.temperature, dht2.humidity, FIRE_flag, WATER_Leftvalue, WATER_Rightvalue);
			HAL_UART_Transmit(&huart1, (uint8_t *)trans_msg, strlen(trans_msg), 100);

			trans_FLAG = 0;
		}

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	}
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 100;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_3) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
	/* User can add his own implementation to report the HAL error return state */
	__disable_irq();
	while (1)
	{
	}
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
	/* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
