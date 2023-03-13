from argparse import ArgumentParser, FileType

__version__ = '0.0.2'

parser = ArgumentParser(description='This script takes an host address from the resource computernewb.com and checks the action of the keys ctrl+alt+del', epilog='Created with love by Mr. Nom4ik')

parser.add_argument('-c', '--count', type=int, default=-1, help='The number of host addresses to collect, if not specified, will search without stopping')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('--filter', help='Filter string')
parser.add_argument('--output', type=FileType('a', encoding='utf-8'), help='File to safe only host addresses')
parser.add_argument('--timeout_connect', type=int, default=5000, help='Timeout (in milliseconds) of connection to VNC server')
parser.add_argument('--timeout_screen', type=int, default=5, help='Timeout (in seconds) to get a screenshot of the host display')
parser.add_argument('--delay_screen', type=int, default=3, help='Timeout (in seconds) between getting two screenshots for their next review')

args = parser.parse_args()

from typing import Union, Generator
from logging import basicConfig, getLogger, INFO, DEBUG, StreamHandler, Formatter
from requests import get
from vnc_client import SuperClient
from twisted.internet.error import TCPTimedOutError
from vncdotool.api import VNCDoException

basicConfig()
logger = getLogger('vncgrub')
logger.propagate = False
logger.setLevel(INFO)

handler = StreamHandler()
handler.setFormatter(Formatter(fmt='[ %(levelname)s %(asctime)s ] %(message)s'))
logger.addHandler(handler)

cache = {}

if args.debug:
    logger.setLevel(DEBUG)


def print_host(number: int, total: Union[int, str], host: str):
    """
    Informs about the receipt of a new valid host

    :param number: host number
    :param total: total host count
    :param host: host address
    """

    logger.info(f'{host} - {number}/{total} host found')

    if args.output:
        args.output.write(host+'\n')


def get_host_address(filter_: str = None) -> str:
    """
    Get one host address

    :param filter_: filter string
    :return: host string on format f"{ip}:{port}"
    """

    if filter_:
        if not cache.get(filter_):
            result = get(f"https://computernewb.com/vncresolver/api/scans/vnc/search?clientname={filter_}").json()
            cache[filter_] = set(result['result'])

        host_id = cache[filter_].pop()
        host = get(f"https://computernewb.com/vncresolver/api/scans/vnc/id/{host_id}").json()
        return f"{host['ip']}:{host['port']}"
    else:
        host = get("https://computernewb.com/vncresolver/api/scans/vnc/random").json()
        return f"{host['ip']}:{host['port']}"


def check_host(host: str) -> bool:
    client = SuperClient(host, args)
    return client.check()


def get_one_valid_host(filter_: str = None) -> str:
    """
    Get one valid host

    :param filter_: filter string
    :return: host string on format f"{ip}:{port}"
    """

    while True:
        host = get_host_address(filter_=filter_)

        logger.debug(f"{host}: Start check")

        try:
            result = check_host(host)

            if result:
                logger.debug(f"{host}: Check success")
                return host
            logger.debug(f"{host}: Check failed")

        except VNCDoException:
            logger.debug(f"{host}: Failed to connect to server")
        except TCPTimedOutError:
            logger.debug(f"{host}: Timeout error connection to server")
        except TimeoutError:
            logger.debug(f"{host}: Timeout error to get a screenshot of the host display")
        except Exception as exc:
            if logger.level == DEBUG:
                logger.exception(exc)


def get_many_valid_hosts(count: int = -1, filter_: str = None) -> Generator:
    """
    Get many valid hosts

    :param count: count of hosts(-1 = infinity)
    :param filter_: filter string
    :return: generator host string on format f"{ip}:{port}"
    """

    if count == -1:
        while True:
            yield get_one_valid_host(filter_=filter_)
    else:
        for _ in range(count):
            yield get_one_valid_host(filter_=filter_)


if __name__ == '__main__':
    print("The search has begun, press CTRL + C to quit")
    i = 0
    for host in get_many_valid_hosts(args.count, args.filter):
        i += 1
        print_host(i, args.count, host)
