/**
  * This program calculate apparent temperature based on 
  * Robert G.Steadman's apparent temperature formula.
  * 
  * 
  * 2019/3/8
  * Version1
  * 
  * Some Thought:
  * 1. Sensor to get precise data
  * 2. Find the relationship between cloth type, warmth index and Apparent temperature.
  * 3. Based on 2. give suggestions on cloth wearing.
  *
  * #TODO:
  * 1. USE crawler to get real-time data.
  * 2. Give suggestions on cloth wearing based on apparent temperature.
  */

#include <stdio.h>
#include <math.h>

void calculate_at(float, float, float);

int main(void) {
    float temperature; /* Unit: centigrade */
    float rh; /* relative humidity, domain interval : [0,1] */
    float V_wind; /* speed of wind, unit: m/s */

    printf("Input temperature(in centigrade):\n");
    scanf("%f", &temperature);
    
    printf("Input relative humidity(0.00,1.00) <e.g. 0.90>:\n");
    scanf("%f", &rh);

    printf("Input wind speed(m/s):\n");
    scanf("%f", &V_wind);

    calculate_at(temperature, rh, V_wind);

    return 0;
}

void calculate_at(float temperature, float rh, float V_wind) {
    float at =  1.07 * temperature + 
          0.2 * ( (rh / 100) * 6.105 * exp( (17.27 * temperature) / (237.7 + temperature))) - 
          0.65 * V_wind - 
          2.7;

    printf("Apparent temperature: %.3f\n", at);
}
