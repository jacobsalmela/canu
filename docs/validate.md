# canu validate

CANU validate commands.

```shell
canu validate [OPTIONS] COMMAND [ARGS]...
```

## network

Commands that validate the network.

```shell
canu validate network [OPTIONS] COMMAND [ARGS]...
```

### bgp

Validate BGP neighbors.

This command will check the BGP neighbors for the switch IP addresses entered. All of the neighbors of a switch
must be ‘Established’, or the verification will fail.

If a switch that is not a spine switch is tested, it will show in the results table as ‘SKIP’.


* Enter a comma separated list of IP addresses with the ‘—ips’ flag.


* Or read the IP addresses from a file, one IP address per line, using ‘–ips-file FILENAME’ flag.

If you want to see the individual status of all the neighbors of a switch, use the ‘–verbose’ flag.


---

```shell
canu validate network bgp [OPTIONS]
```

### Options


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --network( <network>)
The network that BGP neighbors are checked.


* **Default**

    `ALL`



* **Options**

    ALL | NMN | CMN



### --verbose()
Verbose mode

### cabling

Validate network cabling.

CANU can be used to validate that network cabling passes basic validation checks.

This command will use LLDP to determine if the network is properly connected architecturally.

The validation will ensure that spine switches, leaf switches, edge switches, and nodes all are connected properly.


---

```shell
canu validate network cabling [OPTIONS]
```

### Options


### -a(, --architecture( <architecture>)
**Required** CSM architecture


* **Options**

    Full | TDS | v1



### --ips( <ips>)
Comma separated list of IPv4 addresses of switches


### --ips-file( <ips_file>)
File with one IPv4 address per line


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --log( <log_>)
Level of logging.


* **Options**

    DEBUG | INFO | WARNING | ERROR



### --out( <out>)
Output results to a file

### config

Validate network config.

For each switch, this command will compare the current running switch config with a generated switch config.

## Running Config
There are three options for passing in the running config:


* A comma separated list of ips using ‘–ips 192.168.1.1,192.168.1.’


* A file of ip addresses, one per line using the flag ‘–ips-file ips.txt’


* A directory containing the running configuration ‘–running RUNNING/CONFIG/DIRECTORY’

## Generated Config
A directory of generated config files will also need to be passed in using ‘–generated GENERATED/CONFIG/DIRECTORY’.

There will be a summary table for each switch highlighting the most important differences between the running switch config and the generated config files.


---

```shell
canu validate network config [OPTIONS]
```

### Options


### --csm( <csm>)
**Required** CSM network version


* **Options**

    1.0 | 1.2 | 1.3



### --ips( <ips>)
Comma separated list of IPv4 addresses of switches


### --ips-file( <ips_file>)
File with one IPv4 address per line


### --running( <running>)
Folder containing running config files


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --generated( <generated_folder>)
**Required** Config file folder


### --json()
Output JSON


### --out( <out>)
Output results to a file

## paddle

Validate a CCJ file.

Pass in a CCJ file to validate that it works architecturally. The validation will ensure that spine switches,
leaf switches, edge switches, and nodes all are connected properly.

```shell
canu validate paddle [OPTIONS]
```

### Options


### --ccj( <ccj>)
CCJ (CSM Cabling JSON) File containing system topology.


### --out( <out>)
Output results to a file


### --log( <log_>)
Level of logging.


* **Options**

    DEBUG | INFO | WARNING | ERROR


## paddle-cabling

Validate a CCJ file against the current network cabling.

Pass in a CCJ file to validate that it works architecturally.

This command will also use LLDP to determine the neighbors of the IP addresses passed in to validate that the network
is properly connected architecturally.

The validation will ensure that spine switches, leaf switches,
edge switches, and nodes all are connected properly.

```shell
canu validate paddle-cabling [OPTIONS]
```

### Options


### --csm( <csm>)
**Required** CSM network version


* **Options**

    1.0 | 1.2 | 1.3



### --ccj( <ccj>)
**Required** CCJ (CSM Cabling JSON) File containing system topology.


### --ips( <ips>)
Comma separated list of IPv4 addresses of switches


### --ips-file( <ips_file>)
File with one IPv4 address per line


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --log( <log_>)
Level of logging.


* **Options**

    DEBUG | INFO | WARNING | ERROR



### --out( <out>)
Output results to a file

## shcd

Validate a SHCD file.

CANU can be used to validate that an SHCD (SHasta Cabling Diagram) passes basic validation checks.


* Use the ‘–tabs’ flag to select which tabs on the spreadsheet will be included.


* The ‘–corners’ flag is used to input the upper left and lower right corners of the table on each tab of the worksheet. If the corners are not specified, you will be prompted to enter them for each tab.


* The table should contain the 11 headers: Source, Rack, Location, Slot, (Blank), Port, Destination, Rack, Location, (Blank), Port.


---

```shell
canu validate shcd [OPTIONS]
```

### Options


### -a(, --architecture( <architecture>)
**Required** CSM architecture


* **Options**

    Full | TDS | V1



### --shcd( <shcd>)
**Required** SHCD file


### --tabs( <tabs>)
The tabs on the SHCD file to check, e.g. 10G_25G_40G_100G,NMN,HMN.


### --corners( <corners>)
The corners on each tab, comma separated e.g. ‘J37,U227,J15,T47,J20,U167’.


### --out( <out>)
Output results to a file


### --json()
Output JSON model to a file


### --log( <log_>)
Level of logging.


* **Options**

    DEBUG | INFO | WARNING | ERROR


## shcd-cabling

Validate a SHCD file against the current network cabling.

Pass in a SHCD file and a list of IP address to compair the connections.

The output of the validate shcd-cabling command will show a port by port comparison between the devices found in the SHCD and devices found on the network.
If there is a difference in what is found connected to a devices port in SHCD and Cabling, the line will be highlighted in ‘red’.


---

```shell
canu validate shcd-cabling [OPTIONS]
```

### Options


### --csm( <csm>)
**Required** CSM network version


* **Options**

    1.0 | 1.2 | 1.3



### -a(, --architecture( <architecture>)
**Required** CSM architecture


* **Options**

    Full | TDS | V1



### --shcd( <shcd>)
**Required** SHCD file


### --tabs( <tabs>)
The tabs on the SHCD file to check, e.g. 10G_25G_40G_100G,NMN,HMN.


### --corners( <corners>)
The corners on each tab, comma separated e.g. ‘J37,U227,J15,T47,J20,U167’.


### --ips( <ips>)
Comma separated list of IPv4 addresses of switches


### --ips-file( <ips_file>)
File with one IPv4 address per line


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --log( <log_>)
Level of logging.


* **Options**

    DEBUG | INFO | WARNING | ERROR



### --out( <out>)
Output results to a file


### --macs()
Print NCN MAC addresses

## switch

Commands that validate a switch.

```shell
canu validate switch [OPTIONS] COMMAND [ARGS]...
```

### config

Validate switch config.

After config has been generated, CANU can validate the generated config against running switch config. The running config can be from either an IP address, or a config file.


* To get running config from an IP address, use the flags ‘–ip 192.168.1.1 –username USERNAME –password PASSWORD’.


* To get running config from a file, use the flag ‘–running RUNNING_CONFIG.cfg’ instead.

After running the ‘validate switch config’ command, you will be shown a line by line comparison of the currently running switch config against the config file that was passed in. You will also be given a list of remediation commands that can be typed into the switch to get the running config to match the config file. There will be a summary table at the end highlighting the most important differences between the configs.


* Lines that are red and start with a ‘-’ are in the running config, but not in the config file


* Lines that are green and start with a ‘+’ are not in the running config, but are in the config file


* Lines that are blue and start with a ‘?’ are attempting to point out specific line differences


---

```shell
canu validate switch config [OPTIONS]
```

### Options


### --ip( <ip>)
The IP address of the switch with running config


### --running( <running>)
The running switch config file


### --vendor( <vendor>)
The vendor is needed if passing in the running config from a file


* **Options**

    Aruba | Dell | Mellanox



### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --generated( <generated_config>)
Generated config file


### --out( <out>)
Output results to a file


### --remediation()
Outputs commands to get from the running-config to generated config
