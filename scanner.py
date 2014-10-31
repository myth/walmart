import socket
import threading
from Queue import Queue

"""
Scan hosts multithreaded
"""

ADDR_START = '81.166.52.2'
ADDR_STOP = '81.166.53.255'
MAX_THREADS = 100

def get_next_addr(addr):
    if addr == ADDR_STOP:
        return None

    skeet = addr.split('.')
    skeet = map(int, skeet)

    if skeet[3] < 256:
        skeet[3] += 1
    else:
        if skeet[3] == 256:
            skeet[3] = 2
            if skeet[2] < 256:
                skeet[2] += 1
            else:
                if skeet[2] == 256:
                    skeet[2] = 1
                if skeet[1] < 256:
                    skeet[1] += 1

    return '.'.join(map(str, skeet))

fail = Queue()
success = Queue()

def scan(addr):
    """
    Worker
    """

    s = socket.socket()
    s.settimeout(1)

    try:
        s.connect((addr, 80))
        success.put(addr, True, 2)
        s.shutdown(1)
        s.close()
        return addr
    except socket.error:
        fail.put(addr, True, 2)
        return None

if __name__ == '__main__':
    """
    Main control flow
    """

    tc = 0
    threads = []
    addr = get_next_addr(ADDR_START)
    
    try:
        while addr:
            print 'Scanning %s' % addr
            if tc > MAX_THREADS:
                for thread in threads:
                    thread.join()
                tc = 0

            t = threading.Thread(target=scan, args=(addr,))
            t.start()
            tc += 1
            threads.append(t)

            addr = get_next_addr(addr)

    except KeyboardInterrupt:
        pass
    finally:
        for thread in threads:
            thread.join()
            tc = 0

    print 'Completed. Found %d servers live' % success.qsize()

    with open('scan_dump.txt', 'w') as dump:
        while not success.empty():
            dump.write(success.get() + '\n')
