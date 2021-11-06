import socket
import logging
import pickle

import server


def test_server():
    logger = logging.getLogger('client')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server localhost 9999')
    s.connect(('localhost', 9999))
    s.send(pickle.dumps(60, -1))
    logger.debug(f'recieved {pickle.loads(s.recv(1024))}')
    s.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server.main()
    test_server()
