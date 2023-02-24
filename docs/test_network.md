# canu test

Run tests against the network.

Args:

    ctx: CANU context settings
    username: Switch username
    csm: CSM version
    password: Switch password
    sls_file: JSON file containing SLS data
    sls_address: The address of SLS
    network: The network that is used to connect to the switches.


    ```
    log_
    ```

    : enable logging


    ```
    json_
    ```

    : output test results in JSON format
    ping: run the ping test suite

```shell
canu test [OPTIONS]
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


### --json()
JSON output.


### --ping()
Ping test from all mgmt switches to all NCNs.


### --sls-address( <sls_address>)

* **Default**

    `api-gw-service-nmn.local`



### --password( <password>)
Switch password


### --csm( <csm>)
**Required** CSM version


* **Options**

    1.0 | 1.2 | 1.3



### --username( <username>)
Switch username


* **Default**

    `admin`
