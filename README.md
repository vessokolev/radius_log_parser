# parser.py - lightweight parser for locating entries in the FreeRADIUS log files by MAC address

## General information

The goal of developing and supporting this parser script, is to help analyzing the log files mainainned by the [FreeRADIUS](https://freeradius.org/) daemon `radiusd` (the content of those files is in plain text). When analyzing those files, the script is parsing their content line by line, and conditionally performing an additional check, if the line content has pattern mathching the one typical for the WiFi clients' autnetnication requests. That additional check has a goal to check if the MAC address of the client's WiFi adaper matches the one passed to the script as an invoking parameter. If match is found, the script prints the line to the standard output. 

The script might be of help to the administrators of the FreeRADIUS servers that are part of the [Eduroam](https://www.eduroam.org) infrastructure. Its code could be modified to support specific tasks like grouping the entries in the log files or providing front end to Zabbix agents.

## Information regarding the format of MAC addresses reported to the log files

The MAC address of the client's WiFi adapter, along with some information regarding the process of authentication, is reported to `/var/log/radius/radius.log`. There, the string representing the MAC address number, can match one of the following formats:
```
0123456789ab
01:23:45:67:89:ab
01-23-45-67-89-ab
0123-4567-89ab
0123.4567.89ab
```
Those formats are imposed by the type of the reporting access point device. Different WiFi access point devices vendors adopts differen format for reporting the MAC address of the client to the RADIUS server.

The script code has the ability to parse the log files line by line, to recognize there the sought MAC address, regardless its string format, and print that line out to the standard output.

## Pre-requsites

To execute the script one needs to have installed the recent [Python](http://python.org) 3.x.

## Download the code

$ git clone https://github.com/vessokolev/radius_log_parser.git

## License

See the file LICENSE.

## Author

See the file AUTHORS.

## Examples:

Search for any entries, related to the authentication of a client with MAC address `0123456789ab` and reported to `/var/log/radius/radius.log` (the default `radiusd` log file):

```
# parser.py 0123456789ab
```

Search for any entries, related to the authentication of a client with MAC address `0123456789ab` and reported to `/var/log/radius/radius.log-20180901.gz`:

```
# parser.py 0123456789ab /var/log/radius.log-20180901.gz
```

Search for any entries, related to the authentication of a client with MAC address `0123456789ab` and reported to any of the `radiusd` log files stored in `/var/log/radius/`:

```
# FILES=`ls /var/log/radius/radius.log*` && for i in $FILES ; do parser.py 0123456789ab $i ; done
```
