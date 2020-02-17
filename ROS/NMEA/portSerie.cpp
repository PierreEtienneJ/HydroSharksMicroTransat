#include "portSerie.h"
#include <string.h>

//bibliothèque libserial : sudo apt-get install libserial-dev
#include <SerialPort.h>
#include <SerialStream.h>
using namespace LibSerial;

PortSerie::PortSerie(int baudrate, std::string port, int nbBits, int parite, char stopBit){
    this->baudrate=baudrate;
    this->port=port;
    this->nbBits=nbBits;
    this->parite=parite;
    this->stopBit=stopBit;
    this->my_serial_port=new SerialPort(this->port);
}
PortSerie::~PortSerie(){
    this->my_serial_port->Close();
}
void PortSerie::open(){
    try{ //ouverture du port
        this->my_serial_port->Open();
    }
    catch(const std::exception& e){
        throw this->e_ErrCom_Inexistant;
    }
    switch (this->baudrate){ //définition du baudrate
        case 110:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_110);
            break;
        case 300:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_300);
            break;
        case 1200:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_1200);
            break;
        case 2400:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_2400);
            break;
        case 4800:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_4800);
            break;
        case 9600:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_9600);
            break;
        case 19200:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_19200);
            break;
        case 38400:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_38400);
            break;
        case 57600:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_57600);
            break;
        case 115200:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_115200);
            break;
        case 230400:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_230400);
            break;
        case 460800:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_460800);
            break;
        case 921600:
            this->my_serial_port->SetBaudRate(SerialPort::BAUD_921600);
            break;
        default:
            throw this->e_ErrCom_Baudrate;
            break;
    }
    switch (this->nbBits){ //taille caractère
        case 5:
            this->my_serial_port->SetCharSize(SerialPort::CHAR_SIZE_5);
            break;
        case 6:
            this->my_serial_port->SetCharSize(SerialPort::CHAR_SIZE_6);
            break;
        case 7:
            this->my_serial_port->SetCharSize(SerialPort::CHAR_SIZE_7);
            break;
        case 8:
            this->my_serial_port->SetCharSize(SerialPort::CHAR_SIZE_8);
            break;
        default:
            this->my_serial_port->SetCharSize(SerialPort::CHAR_SIZE_DEFAULT);
            break;
    }
    switch (this->stopBit){
        case 1:
            this->my_serial_port->SetNumOfStopBits(SerialPort::STOP_BITS_1);
            break;
        case 2:
            this->my_serial_port->SetNumOfStopBits(SerialPort::STOP_BITS_2);
            break;
        default:
            this->my_serial_port->SetNumOfStopBits(SerialPort::STOP_BITS_DEFAULT);
            break;
    }
}
    //if good
    //throw this->e_ErrCom_None;
    //else
    //autre throw

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