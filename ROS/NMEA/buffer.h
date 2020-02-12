#ifndef BUFFER_H
#define BUFFER_H
#include <string>
class Buffer{
    private:
        std::string *buffer;
        int head;
        int queue;
        static int length;

    public:
        Buffer(int length);
        ~Buffer();
        bool addString(std::string msg); //return si le message a pu s'enregister 
        std::string popString();        //rend le first msg 
        int dataSize(); //rend le nb de message enregister dans le buffer
        int remaningSize(); //rend le nb de case restante
        bool dataAvailable();
};

#endif 