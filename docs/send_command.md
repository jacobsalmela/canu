# canu send command

Canu send command.

```shell
canu send command [OPTIONS]
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


### --command( <command>)
**Required** command to send to the switches e.g. show version


### --name( <name>)
The name of the switch to run the command on, the default for this is all switches e.g. sw-leaf-bmc-001


### --sls-address( <sls_address>)

* **Default**

    `api-gw-service-nmn.local`



### --password( <password>)
Switch password


### --username( <username>)
Switch username


* **Default**

    `admin`
