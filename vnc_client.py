from typing import Dict
from time import sleep
from PIL.Image import Image
from vncdotool.api import connect
from vncdotool.client import VNCDoToolClient


class Options:
    """
    Class with options (useless class)
    """

    __slots__ = 'timeout_connect', 'timeout_screen', 'delay_screen'

    timeout_connect: int
    timeout_screen: int
    delay_screen: int

    """
    :param timeout_connect: Timeout (in milliseconds) of connection to VNC server
    :param timeout_screen: Timeout (in seconds) to get a screenshot of the host display
    :param delay_screen: Timeout (in seconds) between getting two screenshots for their next review
    """


class SuperClient:
    """
    Helper class
    """

    __slots__ = ('host', 'options', 'client')

    client: VNCDoToolClient
    host: str
    extra: Dict[str, str]

    def __init__(self, host: str, options: Options):
        """
        :param host: host address
        :param options: options class
        """

        self.host = host
        self.options = options
        self.client = connect(host.split(':')[0] if host.split(':')[1] == '5900' else host, timeout=self.options.timeout_connect)

    def reboot(self):
        """
        Sends the ctrl+alt+del key combination to reboot the host
        """

        self.client.keyDown('ctrl')
        self.client.keyDown('alt')
        self.client.keyDown('del')

        self.client.keyUp('ctrl')
        self.client.keyUp('alt')
        self.client.keyUp('del')

    def get_screen(self) -> Image:
        """
        Get a screenshot of the host display
        """

        return self.client.refreshScreen().screen.copy()

    def check(self) -> bool:
        """
        Check if ctrl+alt+del key combination works on host
        """

        screen_1 = self.get_screen()
        self.reboot()
        sleep(self.options.delay_screen)
        screen_2 = self.get_screen()
        return not screen_1 == screen_2
