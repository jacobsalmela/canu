# Quickstart Guide

There are several ways to invoke CANU, including:


* `docker run` (or other runtime)


* `docker exec` (or other runtime)


* `canuctl`

For consistency and simplification, the invocations of CANU throughout the documentation will simply be show as

```shell
canu --things
```

even though you may be invoking CANU via a different method.

## Checkout A Fresh System

This procedure requires [`csi`](https://github.com/Cray-HPE/cray-site-init)


1. Make a new directory to save switch IP addresses

```bash
mkdir ips_folder
cd ips_folder
```


2. Parse CSI files and save switch IP addresses

```bash
canu init --sls-file sls_input_file.json --out ips.txt`
```


3. Check network firmware

```bash
canu report network firmware --csm 1.2 --ips-file ips.txt
```


4. Check network cabling

```bash
canu report network cabling --ips-file ips.txt
```


5. Validate BGP status

```bash
canu validate network bgp --ips-file ips.txt --verbose
```


6. Validate cabling

```bash
canu validate network cabling --ips-file ips.txt
```

If you have the system’s **SHCD**, there are even more commands that can be run


1. Validate the SHCD

```bash
canu validate shcd --shcd SHCD.xlsx
```


2. Validate the SHCD against network cabling

```bash
canu validate shcd-cabling --shcd SHCD.xlsx --ips-file ips.txt
```


3. Generate switch config for the network

```bash
canu generate network config --shcd SHCD.xlsx --sls-file sls_input_file.json --folder configs
```


4. Convert the SHCD to CCJ

```bash
canu validate shcd --shcd SHCD.xlsx --json --out paddle.json
```

If you have the system’s **CCJ**

1. Validate the Paddle / CCJ

```bash
canu validate paddle --ccj paddle.json
```


2. Validate the CCJ against network cabling

```bash
canu validate paddle-cabling --ccj paddle.json --ips-file ips.txt
```


3. Generate switch config for the network

```bash
canu generate network config --ccj paddle.json --sls-file sls_input_file.json --folder configs
```