#include "NMEA.h"

NMEA::NMEA(int baudrate, std::string port, int nbBits, int partite, char stopBit, Buffer *buffer):PortSerie(baudrate, port, nbBits, partite, stopBit,buffer){
    this->dState=this->decodeState::Waiting;
}

TrameNMEA NMEA::getMessage(void){
    TrameNMEA trame();
    std::string *msg;
    char *idR=new char[2];
    char *idT=new char[3];
    while(this->buffer->dataAvailable()){
        char c=buffer->popelem();
        switch(this->dState){
            case this->decodeState::Waiting:
                if(c=='$') //premier element d'une TrameNMEA
                    this->dState=this->decodeState::iDr_1;
                break;
            case this->decodeState::iDr_1:
                idR[0]=c;
                this->dState=this->decodeState::iDr_2;
                break;
            case this->decodeState::iDr_2:
                idR[1]=c;
                this->dState=this->decodeState::iDt_1;
                break;
            case this->decodeState::iDt_1:
                idT[0]=c;
                this->dState=this->decodeState::iDt_2;
                break;
            case this->decodeState::iDt_2:
                idT[1]=c;
                this->dState=this->decodeState::iDt_3;
                break;
            case this->decodeState::iDt_3:
                idT[2]=c;
                this->dState=this->decodeState::payload;
                break;
            default:
                break;
        }
    }
}