#ifndef NMEA_H
#define NMEA_H 
#include <string>
#include "portSerie.h"
class NMEA : public PortSerie{
    private:
        

    public:
        NMEA(int baudrate, std::string port, int nbBits, int partite, char stopBit);
};
#endif