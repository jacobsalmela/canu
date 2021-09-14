# Generate Network Config

CANU can generate switch config for all the switches on a network.

To see all the lags that are generated, see [lags](docs/lags.md)

In order to generate switch config, a valid SHCD must be passed in and system variables must be read in from either CSI output or the SLS API.

#### CSI Input

- In order to parse CSI output, use the `--csi-folder FOLDER` flag to pass in the folder where the _sls_input_file.json_ file is located.

The sls_input_file.json file is generally stored in one of two places depending on how far the system is in the install process.

- Early in the install process, when running off of the LiveCD the sls_input_file.json file is normally found in the the directory `/var/www/ephemeral/prep/SYSTEMNAME/`

- Later in the install process, the sls_input_file.json file is generally in `/mnt/pitdata/prep/SYSTEMNAME/`

#### SLS API Input

- To parse the Shasta SLS API for IP addresses, ensure that you have a valid token. The token file can either be passed in with the `--auth-token TOKEN_FILE` flag, or it can be automatically read if the environmental variable **SLS_TOKEN** is set. The SLS address is default set to _api-gw-service-nmn.local_, if you are operating on a system with a different address, you can set it with the `--sls-address SLS_ADDRESS` flag.

#### SHCD Input

- The `--shasta / -s` flag is used to set the Shasta version of the system.
- The `--architecture / -a` flag is used to set the architecture of the system, either **TDS**, or **Full**.
- Use the `--tabs` flag to select which tabs on the spreadsheet will be included.
- The `--corners` flag is used to input the upper left and lower right corners of the table on each tab of the worksheet. The table should contain the 11 headers: **Source, Rack, Location, Slot, (Blank), Port, Destination, Rack, Location, (Blank), Port**. If the corners are not specified, you will be prompted to enter them for each tab.

To generate network config, a folder must also be passed in using the `--folder FOLDERNAME` flag.

## Examples

### 1. Generate network config from SLS API

To generate network config run: `canu generate network config -s 1.5 -a full --shcd FILENAME.xlsx --tabs 'INTER_SWITCH_LINKS,NON_COMPUTE_NODES,HARDWARE_MANAGEMENT,COMPUTE_NODES' --corners 'J14,T44,J14,T48,J14,T24,J14,T23' --auth_token TOKEN_FILE --folder SWITCH_CONFIG`

```bash
$ canu generate network config -s 1.5 -a full --shcd FILENAME.xlsx --tabs INTER_SWITCH_LINKS,NON_COMPUTE_NODES,HARDWARE_MANAGEMENT,COMPUTE_NODES --corners J14,T44,J14,T48,J14,T24,J14,T23 --auth_token TOKEN_FILE --folder SWITCH_CONFIG

sw-spine-001 Config Generated
sw-spine-002 Config Generated
sw-leaf-001 Config Generated
sw-leaf-002 Config Generated
sw-leaf-003 Config Generated
sw-leaf-004 Config Generated
sw-cdu-001 Config Generated
sw-cdu-002 Config Generated
sw-leaf-bmc-001 Config Generated

```

### 2. Generate network config from CSI

To generate network config run: `canu generate network config -s 1.5 -a full --shcd FILENAME.xlsx --tabs 'INTER_SWITCH_LINKS,NON_COMPUTE_NODES,HARDWARE_MANAGEMENT,COMPUTE_NODES' --corners 'J14,T44,J14,T48,J14,T24,J14,T23' --csi-folder /CSI/OUTPUT/FOLDER/ADDRESS --folder SWITCH_CONFIG`

```bash
$ canu generate network config -s 1.5 -a full --shcd FILENAME.xlsx --tabs INTER_SWITCH_LINKS,NON_COMPUTE_NODES,HARDWARE_MANAGEMENT,COMPUTE_NODES --corners J14,T44,J14,T48,J14,T24,J14,T23 --csi-folder /CSI/OUTPUT/FOLDER/ADDRESS --folder SWITCH_CONFIG

sw-spine-001 Config Generated
sw-spine-002 Config Generated
sw-leaf-001 Config Generated
sw-leaf-002 Config Generated
sw-leaf-003 Config Generated
sw-leaf-004 Config Generated
sw-cdu-001 Config Generated
sw-cdu-002 Config Generated
sw-leaf-bmc-001 Config Generated

```

## Flags

| Option                | Description                                                                |
| --------------------- | -------------------------------------------------------------------------- |
| `-s / --shasta`       | Shasta version                                                             |
| `-a / --architecture` | Shasta architecture ("Full", or "TDS")                                     |
| `--shcd`              | SHCD File                                                                  |
| `--tabs`              | The tabs on the SHCD file to check, e.g. 10G_25G_40G_100G,NMN,HMN.         |
| `--corners`           | The corners on each tab, comma separated e.g. 'J37,U227,J15,T47,J20,U167'. |
| `--csi_folder`        | Directory containing the CSI json file                                     |
| `--auth_token`        | Token for SLS authentication                                               |
| `--sls_address`       | The address of SLS                                                         |
| `--folder`            | Folder to store config files                                               |

---

**[Back To Readme](/readme.md)**<br>