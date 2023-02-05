# VNCAutoGrubber
A script that takes ip addresses from computernewb.com and checks them for vulnerabilities by rebooting the machine via ctrl+alt+del, which further facilitates obtaining root access through the operating system bootloader

```
$ python main.py --help
usage: main.py [-h] [-c COUNT] [-d] [-v] [--filter FILTER] [--output OUTPUT] [--timeout_connect TIMEOUT_CONNECT] [--timeout_screen TIMEOUT_SCREEN]
               [--delay_screen DELAY_SCREEN]

This script takes an host address from the resource computernewb.com and checks the action of the keys ctrl+alt+del

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        The number of host addresses to collect, if not specified, will search without stopping
  -d, --debug           Enable debug mode
  -v, --version         show program's version number and exit
  --filter FILTER       Filter string
  --output OUTPUT       File to safe only host addresses
  --timeout_connect TIMEOUT_CONNECT
                        Timeout (in milliseconds) of connection to VNC server
  --timeout_screen TIMEOUT_SCREEN
                        Timeout (in seconds) to get a screenshot of the host display
  --delay_screen DELAY_SCREEN
                        Timeout (in seconds) between getting two screenshots for their next review

Created with love by Mr. Nom4ik
```

```
$ python main.py --count 3 --filter ubuntu --output ubuntu_hosts.txt
The search has begun, press CTRL + C to quit
[ INFO 2023-02-05 15:50:01,170 ] 42.51.28.181:5900 - 1/3 host found
[ INFO 2023-02-05 15:50:29,684 ] 24.141.38.33:5900 - 2/3 host found
[ INFO 2023-02-05 15:50:41,968 ] 213.32.89.18:5900 - 3/3 host found
$ cat ubuntu_hosts.txt
42.51.28.181:5900
24.141.38.33:5900
213.32.89.18:5900
```
