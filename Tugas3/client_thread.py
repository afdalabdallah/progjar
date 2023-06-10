import sys
import socket
import logging
import time
import threading

max_thread = 0
def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('172.18.0.2', 44000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] sending {message}")
        sock.sendall(message.encode('utf-8'))
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(1024).decode('utf-8')
            amount_received += len(data)
            logging.warning(f"[DITERIMA DARI SERVER] {data}")
    finally:
        logging.warning("closing")
        global max_thread
        max_thread = max(max_thread,threading.active_count())
        sock.close()
    return


if __name__=='__main__':
    count = 0
    start = time.time()
    while time.time() - start < 60:
        t = threading.Thread(target=kirim_data)
        t.start()
        t.join()
        count += 1
        
    f = open('hasil-thread.txt', 'w')
    f.write(f"Maximum threads acquired: {count}")
    f.close
    
    logging.warning(f"Thread Max Active: {count}")