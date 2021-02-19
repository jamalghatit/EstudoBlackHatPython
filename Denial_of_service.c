#include <netdb.h>
#include <stdio.h>        // printf(), perror()
#include <sys/types.h>    // AF_INET, SOCK_STREAM
#include <sys/socket.h>   // socket(), connect()
#include <netinet/in.h>   // struct sockaddr_in
#include <arpa/inet.h>    // htons(), inet_addr()

int main(int argc, char *argv[]){
        
        int meusocket;
        int conecta;
        int porta = argv[2];
        char *destino
        destino = argv[1]
        
        struct sockaddr_in alvo;
        
        for(;;){
        meusocket = socket(AF_INET, SOCK_STREAM, 0);
        alvo.sin_family = AF_INET;
        alvo.sin_port = htons(porta);
        alvo.sin_addr.s_addr = inet_addr(destino);
        conecta = connect(meusocket, (struct sockaddr *)&alvo, sizeof alvo);
                if (conecta == 0){
                        printf("Conectou sem erros\n");
                }else{
                        perror("ERRO\n");
                }
        }
}
        
