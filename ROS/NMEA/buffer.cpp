#include "buffer.h"
Buffer::Buffer(int length){
    this->length=length;
    this->buffer=new std::string[length];
    this->head=0;
    this->queue=0;
}
Buffer::~Buffer(){
    delete buffer;
}

bool Buffer::addString(std::string msg){
    if(this->remaningSize>0){
        this->buffer[this->head++]=msg;
        if(this->head >= this->length)
            this->head=0;
        return true;
    }
    return false;
}
std::string Buffer::popString(){
    std::string msg=this->buffer[this->queue++];
    if(this->queue>=this->length)
        this->queue=0;
    return msg;
}

int Buffer::remaningSize(){
    return this->length-this->dataSize();
}
int Buffer::dataSize(){
    if(this->head-this->queue<0)
        return this->head-this->queue+this->length;
    return this->head-this->queue;
}
bool Buffer::dataAvailable(){
    if(this->queue==this->head)
        return false;
    return true;
}