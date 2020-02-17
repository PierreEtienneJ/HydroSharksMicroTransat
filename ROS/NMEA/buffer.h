#ifndef BUFFER_H
#define BUFFER_H
#include <string>
class Buffer{
    private:
        char *buffer;
        int head;
        int queue;
        static int length;

    public:
        Buffer(int length);
        ~Buffer();
        bool addString(char msg); //return si le message a pu s'enregister 
        char popelem();        //rend le first msg 
        int dataSize(); //rend le nb de message enregister dans le buffer
        int remaningSize(); //rend le nb de case restante
        bool dataAvailable();
};

#endif 