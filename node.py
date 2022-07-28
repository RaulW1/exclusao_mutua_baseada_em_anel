import socket
import time
import random
import logging
from datetime import datetime

# ----- ROTINA PARA CONSUMIR O RECURSO -----
def use_rc(pid, token):
    try:
        rc = open('regiao_critica.txt', 'a')
        logging.info(f'Processo {pid}: Acessando região crítica com o token: {token}')
        rc.write(f'Processo {pid} esteve aqui em {datetime.now().strftime("%H:%M:%S")} com o token: {str(token)}\n')
        time.sleep(1)
        rc.close()
    except Exception as e:
        print(e)

# ----- NODES -----
def nodes(pid, p_qtd, port, host, n_iter):
    if pid == p_qtd-1:
        next_port = port-pid # aponta para o inicio do anel
    else:
        next_port = port + 1 # aponta para o proximo node no anel

    # cria socket UDP para comunicação entre os nodos
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    has_token = False
    token = 1

    # se o node for o primeiro, recebe o privilégio e cria o token
    if pid == 0:
            has_token = True
            time.sleep(5)

    s.bind((host, port)) # faz o bind entre host e porta para o nodo

    logging.info(f'Processo {pid}: pronto')

    while token <= n_iter:
        time.sleep(1)
        # ----- NÂO POSSUI TOKEN -----
        while not has_token:  # aguarda recebimento do token
            data_token, addr = s.recvfrom(1024)
            if data_token.decode():  # se recebe o token, altera o atributo hasToken p\ True
                    has_token = True
                    logging.info(f'Processo {pid}: tem o token')
                    token = int(data_token)
        # ----- POSSUI TOKEN -----
        # 'coin flip' para determinar se tem um requisição
        if random.randint(0, 10) == pid:  # se sim, entra na região critica, consome o token e o incrementa
            use_rc(pid, token)  # usufrui do privilégio
            logging.info(f'Processo {pid}: consumiu o token')
            token += 1
            s.sendto(str(token).encode(),(host,next_port))
            logging.info(f'Processo {pid}: enviou o token para {next_port-5000}')
            has_token = False
        else:  # se não, passa o token adiante para o próximo node do anel
            logging.info(f'Processo {pid}: não precisa do token')
            s.sendto(str(token).encode(),(host,next_port))
            logging.info(f'Processo {pid}: enviou o token para {next_port - 5000}')
            has_token = False
