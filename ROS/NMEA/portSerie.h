#ifndef PORTSERIE_H
#define PORTSERIE_H
#include <string>
#include "buffer.h"

class PortSerie{
    private:
        typedef enum{
                e_ErrCom_None,		// Pas d'erreur
                e_ErrCom_Creation,	// Erreur lors de la création du flux
                e_ErrCom_Utilise,		// Le port com est déjà utilisé
                e_ErrCom_Inexistant,	// Le port com n'existe pas
                e_ErrCom_Timeout,	// Timeout lors d'une émission-réception
                e_ErrCom_Emission,		// Erreur lors de l'émission
                e_ErrCom_Reception,		// Erreur lors de la réception
                e_ErrCom_Definition_Trame,	// Erreur de définition de la trame
                e_ErrCom_Nack,	// Demande non prise en coompte
                e_ErrCom_Checksum		// Erreur de checksum
            } e_ErrCom;
    protected:
        int baudrate;
        std::string port;
        
    public:
        PortSerie(int baudrate, std::string port, int nbBits, int parite, char stopBit);
        ~PortSerie();

        void open();
        void close();
        void read(Buffer *buffer, unsigned int lenMax);
        std::string read(unsigned int lenMax); // ?
        void write(std::string msg, int length);
};

#endif