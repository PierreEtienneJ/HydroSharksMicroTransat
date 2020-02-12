#include "portSerie.h"

PortSerie::PortSerie(int baudrate, std::string port, int nbBits, int partite, char stopBit){

}
PortSerie::~PortSerie(){

}
void PortSerie::open(){
    //if good
    throw this->e_ErrCom_None;
    //else 
    //autre throw 
}
void PortSerie::close(){
    //if good
    throw this->e_ErrCom_None;
    //else 
    //autre throw 
}
void PortSerie::read(Buffer *buffer, unsigned int lenMax){
    //if good
    throw this->e_ErrCom_None;
    //else 
    //autre throw 
}
std::string PortSerie::read(unsigned int lenMax){
    //if good
    throw this->e_ErrCom_None;
    //else 
    //autre throw 
}
void PortSerie::write(std::string msg, int length){
    //if good
    throw this->e_ErrCom_None;
    //else 
    //autre throw 
}