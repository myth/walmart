# -*- coding: utf-8 -*-

import pprint
import queue
import random
import re
import requests
import sys
import threading
import time


# Settings
OFFSET = int(26 * 26)           # Skip 2-letter combos
MAX_ACTIVE_THREADS = 16         # Max simultaniously active requests
REQUEST_DELAY = 0.15            # Interval between each spawned thread

# Define letters, vocals and consonants
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z']
VOCALS = ['a', 'e', 'i', 'o', 'u', 'y']
CONSONANTS = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']

# TLDs of interest
TLDS = ['no']

# API
API = 'https://www.domeneshop.no/check?domainname=%s&checked=1&random=%d'

# Capture
VACANT = queue.Queue()


# ANSI Term colors
class Color(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

COLORS = Color()


class DomainAvailabilityCheck(threading.Thread):
    """
    Perform an API request to domainnameshop on domain availibility
    """

    def __init__(self, thread_id, domain, lock):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        self.name = domain
        self.domain = domain
        self.lock = lock

    def run(self):
        """
        Check domain availability via the API and add domain to VACANT queue if available.
        This thread aquires a lock before starting, and releases upon completion.
        """

        # Acquire resource lock before proceeding
        self.lock.acquire()

        # Make the API request and add a random nonce
        response = requests.get(API % (self.domain, random.randint(10000, 99999)))

        if is_available(response.text):
            price = str(extract_price(response.text))
            sys.stdout.write('%s%s%s%s%s%s\n' % (
                self.domain.ljust(20),
                COLORS.BOLD,
                COLORS.OKGREEN,
                'AVAILABLE'.ljust(20),
                COLORS.ENDC,
                price.ljust(20)
            ))
            sys.stdout.flush()

            # Store available domains for later use
            VACANT.put((self.domain, price))
        else:
            sys.stdout.write('%s%s%s%s%s\n' % (
                self.domain.ljust(20),
                COLORS.BOLD,
                COLORS.FAIL,
                'TAKEN'.ljust(20),
                COLORS.ENDC
            ))
            sys.stdout.flush()

        # Increment available threads on the semaphore
        self.lock.release()


class ExecutorPool(object):
    """
    Thread pool queue that maintains maximum number of active threads.
    """

    def __init__(self):
        self.queue = []
        self.lock = threading.Semaphore(value=MAX_ACTIVE_THREADS)

        # Thread ID
        tid = 0

        # All 2-letter combos
        for a in LETTERS:
            for b in LETTERS:
                for tld in TLDS:
                    self.queue.append(
                        DomainAvailabilityCheck(
                            tid,
                            '%s%s.%s' % (a, b, tld),
                            self.lock
                        )
                    )
                    tid += 1

        # All consonant-vocal-consonant combos
        for a in CONSONANTS:
            for b in VOCALS:
                for c in CONSONANTS:
                    for tld in TLDS:
                        self.queue.append(
                            DomainAvailabilityCheck(
                                tid,
                                '%s%s%s.%s' % (a, b, c, tld),
                                self.lock
                            )
                        )
                        tid += 1

        # All vocal-consonant-vocal combos
        for a in VOCALS:
            for b in CONSONANTS:
                for c in VOCALS:
                    for tld in TLDS:
                        self.queue.append(
                            DomainAvailabilityCheck(
                                tid,
                                '%s%s%s.%s' % (a, b, c, tld),
                                self.lock
                            )
                        )
                        tid += 1

        # All vocal-vocal-consonant combos
        for a in VOCALS:
            for b in VOCALS:
                for c in CONSONANTS:
                    for tld in TLDS:
                        self.queue.append(
                            DomainAvailabilityCheck(
                                tid,
                                '%s%s%s.%s' % (a, b, c, tld),
                                self.lock
                            )
                        )
                        tid += 1

        # All consonant-vocal-vocal combos
        for a in CONSONANTS:
            for b in VOCALS:
                for c in VOCALS:
                    for tld in TLDS:
                        self.queue.append(
                            DomainAvailabilityCheck(
                                tid,
                                '%s%s%s.%s' % (a, b, c, tld),
                                self.lock
                            )
                        )
                        tid += 1

        # All vocal-consonant-consonant combos
        for a in VOCALS:
            for b in CONSONANTS:
                for c in CONSONANTS:
                    for tld in TLDS:
                        self.queue.append(
                            DomainAvailabilityCheck(
                                tid,
                                '%s%s%s.%s' % (a, b, c, tld),
                                self.lock
                            )
                        )
                        tid += 1


    def start(self):
        """
        Starts the process of checking every possible domain name combination
        """

        for t in self.queue[OFFSET:]:
            t.start()
            time.sleep(REQUEST_DELAY)

        for t in self.queue[OFFSET:]:
            t.join()

        print('Done!')
        print_and_save()


def is_available(http_response):
    """
    Checks whether a domain is available or not based on the API response
    """

    if '<tr bgcolor="#B9DBFF">' in http_response:
        return True

    return False


def extract_price(http_response):
    """
    Extracts the price for registration of the domain. Returns None if the domain is only
    available for bidding.
    """

    pattern = re.compile('([0-9]+,\-)')
    m = pattern.search(http_response)
    if m:
        return m.group()
    return None


def print_and_save():
    """
    Prints a formated list of the current state of the VACANT queue of
    available domain names. Also saves the content to disk.
    """

    with open('available_domains.txt', 'w') as f:
        print('Available domains:')
        print('-' * 50)
        while not VACANT.empty():
            domain, price = VACANT.get()
            line = '%s%s' % (domain.ljust(15), price)
            f.write(line + '\n')
            print(line)
        print('-' * 50)


if __name__ == '__main__':
    """
    Perform automated availability checks on auto-generated short domain names.
    """

    welcome_msg = 'Starting short domain name auto checker. '
    welcome_msg += 'This may take a very long time depending on the amount of domains and request delay. '
    welcome_msg += 'Beware of Domeneshop request throttling!\n'
    print(welcome_msg)

    pool = ExecutorPool()
    try:
        pool.start()
    except KeyboardInterrupt:
        print('\nCaught KeyboardInterrupt, exiting...')
        print_and_save()
        exit(0)
