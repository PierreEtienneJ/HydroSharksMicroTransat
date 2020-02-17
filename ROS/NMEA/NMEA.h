#ifndef NMEA_H
#define NMEA_H 
#include <string>
#include "portSerie.h"
#include "trameNMEA.h"

class NMEA : public PortSerie{
    private:
        typedef enum{Waiting, iDr_1,iDr_2, iDt_1, iDt_2, iDt_3, payload, checksum} decodeState;
        NMEA::decodeState dState;
    public:
        NMEA(int baudrate, std::string port, int nbBits, int partite, char stopBit, Buffer *buffer);
        TrameNMEA getMessage(void);
};
#endif