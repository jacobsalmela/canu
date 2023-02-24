# Install The CANU Container

## Pre-built Image

A pre-built CANU image can be pulled from a container runtime (Docker, Podman, etc.)

```shell
docker pull <registry>/canu:<tag>
```

You may also wish to install the `canuctl` wrapper script to simplify running the container with the correct arguments.  That script is installed with the RPM or is available when building the container image.

## Dockerfile

The container image can be built from the `Dockerfile` in the [canu repo](https://github.com/Cray-HPE/canu/blob/main/Dockerfile.

```shell
git clone https://github.com/Cray-HPE/canu.git
cd canu
make prod
```
