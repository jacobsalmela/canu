# canu report

Canu report commands.

```shell
canu report [OPTIONS] COMMAND [ARGS]...
```

## network

Commands that report on the entire network.

```shell
canu report network [OPTIONS] COMMAND [ARGS]...
```

### cabling

Report the cabling of all switches (Aruba, Dell, or Mellanox) on the network by using LLDP.

Pass in either a comma separated list of IP addresses using the –ips option

OR

Pass in a file of IP addresses with one address per line.

There are three different connection types that will be shown in the results.


1. ‘===>’ Outbound connections


2. ‘<===’ Inbound connections


3. ‘<==>’ Bi-directional connections

There are two different ‘–view’ options, ‘switch’ and ‘equipment’.


1. The ‘–view switch’ option displays a table for every switch IP address passed in showing connections.

2. The ‘–view equipment’ option displays a table for each mac address connection. This means that servers
and switches will both display incoming and outgoing connections.

If the neighbor name is not in LLDP, the IP and vlan information are displayed
by looking up the MAC address in the ARP table and mac address table.

If there is a duplicate port, the duplicates will be highlighted in ‘bright white’.

Ports highlighted in ‘blue’ contain the string “ncn” in the hostname.

Ports are highlighted in ‘green’ when the port name is set with the interface name.

```shell
canu report network cabling [OPTIONS]
```

### Options


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


### --out( <out>)
Output results to a file


### --view( <view>)
View of the cabling results.


* **Default**

    `switch`



* **Options**

    switch | equipment



### --log( <log_>)
Level of logging.


* **Options**

    DEBUG | INFO | WARNING | ERROR


### firmware

Report the firmware versions of all switches (Aruba, Dell, or Mellanox) on the network.

Pass in either a comma separated list of IP addresses using the ‘–ips’ option

OR

Pass in a file of IP addresses with one address per line using the ‘–ips-file’ option

There are three different statuses found in the report.


* 🛶 Pass: Indicates that the switch passed the firmware verification.


* ❌ Fail: Indicates that the switch failed the firmware verification, in the generated table, a list of expected firmware versions for that switch is displayed.


* 🔺 Error: Indicates that there was an error connecting to the switch, check the Errors table for the specific error.


---

```shell
canu report network firmware [OPTIONS]
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


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --json()
Output JSON


### --out( <out>)
Output results to a file

### version

Report Switch Version.

Args:

    ctx: CANU context settings
    username: Switch username
    password: Switch password
    sls_file: JSON file containing SLS data
    sls_address: The address of SLS
    network: The network that is used to connect to the switches.


    ```
    log_
    ```

    : enable logging

```shell
canu report network version [OPTIONS]
```

### Options


### --sls-file( <sls_file>)
File containing system SLS JSON data.


### --network( <network>)
The network that is used to connect to the switches.


* **Default**

    `HMN`



* **Options**

    HMN | CMN



### --log()
enable logging.


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --sls-address( <sls_address>)

* **Default**

    `api-gw-service-nmn.local`


## switch

Report switch commands.

```shell
canu report switch [OPTIONS] COMMAND [ARGS]...
```

### cabling

Report the cabling of a switch (Aruba, Dell, or Mellanox) on the network by using LLDP.

If the neighbor name is not in LLDP, the IP and vlan information are displayed
by looking up the MAC address in the ARP table or the mac address table.

If there is a duplicate port, the duplicates will be highlighted in ‘bright white’.

Ports highlighted in ‘blue’ contain the string “ncn” in the hostname.

Ports are highlighted in ‘green’ when the port name is set with the interface name.


---

```shell
canu report switch cabling [OPTIONS]
```

### Options


### --ip( <ip>)
**Required** The IP address of the switch


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --out( <out>)
Output results to a file

### firmware

Report the firmware of a switch (Aruba, Dell, or Mellanox) on the network.

There are two different statuses that might be indicated.


* 🛶 - Pass: Indicates that the switch passed the firmware verification.


* ❌ - Fail: Indicates that the switch failed the firmware verification. A list of expected firmware versions will be displayed.


---

```shell
canu report switch firmware [OPTIONS]
```

### Options


### --csm( <csm>)
**Required** CSM network version


* **Options**

    1.0 | 1.2 | 1.3



### --ip( <ip>)
**Required** The IP address of the switch


### --username( <username>)
Switch username


* **Default**

    `admin`



### --password( <password>)
Switch password


### --json()
Output JSON


### --verbose()
Verbose mode


### --out( <out>)
Output results to a file
