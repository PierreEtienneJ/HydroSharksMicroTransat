It's all of algorithm to predict speed, solar panel's production..

With all data produced by the boat, this algorithm give speed predictions, production predictions, drift predictions and consumption prediction. 

For that we need :
- Wind : speed, direction 
- Swell : frequency, amplitude, direction
- Stream : speed, direction
- air : Temperature, Pressure, Humidity
- water : Temperature, Salinity
- Sun : UV, Lux and numb octa
- time : UTC

Consumption depends on the enslavement's coefficient which itself depends on the battery charge. 
Production depends on the height of the sun in the sky (depends on time), clouds and roll (depends on wind and Swell). 
Speed also depends on  the enslavement's coefficient. 

This code is used to feed the routing algorithm. 

These two algorythms, are optimized for calculations on GPU. 


In order to test prediction's algorythm, we create an algorythm to generate some datas. 



