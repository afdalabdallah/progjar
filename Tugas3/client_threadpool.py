import sys
import socket
import logging
import concurrent.futures
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
        logging.warning("closing\n")
        global max_thread
        max_thread = max(max_thread,threading.active_count())
        sock.close()
    return

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        count = 0
        request = set()
        start = time.time()
        while time.time() - start < 60:
            request.add(executor.submit(kirim_data))
            
            complete_req = {req for req in request if req.done()}
            request -= complete_req
            
            count += len(complete_req)
                
        for r in request:
            r.result()
        
        f = open('hasil-threadpool.txt', 'w')
        f.write(f"Maximum threadpool acquired: {count}")
        f.close
        
        logging.warning(f"Threadpool Max Active: {count}")
    executor.shutdown(wait=True)