#include "trameNMEA.h"

TrameNMEA::TrameNMEA(TrameNMEA::iDrecepteur idrecepteur, TrameNMEA::iDtrame idtrame, std::string *message){
    this->recepteur=idrecepteur;
    this->trame=idtrame;
    this->message=message;
}


TrameNMEA::iDtrame TrameNMEA::convertStr2IdTrame(std::string idT){
    int i=0;
    while(i<86 && idT !=this->strIdTrame[i])
        i++;
    if(i==86 && idT !=this->strIdTrame[86])
        return TrameNMEA::iDtrame(i);
    else if (i<86)
        return TrameNMEA::iDtrame(i);
    else
        return TrameNMEA::iDtrame(-1);
}