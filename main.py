from threading import Thread
import logging
import socket
from node import nodes

format = "%(asctime)s: %(message)s"
port = 5000
host = socket.gethostname()


def main():
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    n_qtd = int(input('Número de processos (2 <= n <= 10): '))
    n_iter = int(input('Número máximo de acessos a RC (i > 1): '))
    print('\n\n')

    count = 0
    while (count < n_qtd):
        node = Thread(target=nodes, args=[count, n_qtd, port+count, host, n_iter])
        node.deamon = True
        node.start()
        count += 1


if __name__ == '__main__':
    main()