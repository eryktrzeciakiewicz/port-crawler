from multiprocessing.dummy import Pool as ThreadPool
from options import *
from messages import *
import socket
from sys import argv as args


def panic():
    print(USAGE_MSG)
    exit(1)


def initialize():
    def assert_args_length(length):
        if len(args) < length:
            panic()

    def initialize_range():
        assert_args_length(6)
        lower = int(args[4])
        upper = int(args[5])
        if lower > upper:
            lower, upper = upper, lower
        return [port for port in range(lower, upper + 1)]

    def initialize_single():
        assert_args_length(5)
        for port in args[4:]:
            yield int(port)

    def initialize_all():
        return [port for port in range(1, 65535)]

    def initialize_ports():
        assert_args_length(4)
        option = args[3]
        if option == ALL_OPTION:
            return initialize_all()
        elif option == RANGE_OPTION:
            return initialize_range()
        elif option == SINGLE_OPTION:
            return initialize_single()
        else:
            panic()

    ports = initialize_ports()
    server = socket.gethostbyname(args[1])
    num_threads = int(args[2])
    return server, ports, num_threads


def main():
    open_ports = []
    server, ports, num_threads = initialize()
    thread_pool = ThreadPool(num_threads)

    def print_open_ports():
        if len(open_ports) == 0:
            print(NO_OPEN_PORTS_MSG)
            return

        print(OPEN_PORTS_FOUND_MSG)
        print(*open_ports, sep=', ')

    def establish_tcp_connection(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((server, port))
            open_ports.append(port)
        except OSError:
            pass

    def scan_ports():
        thread_pool.map(establish_tcp_connection, ports)

    scan_ports()
    print_open_ports()


if __name__ == "__main__":
    main()
