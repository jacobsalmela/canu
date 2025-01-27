# MIT License
#
# (C) Copyright 2022-2023 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# STAGE 1 - install build dependencies and activate virtualenv
ARG         ALPINE_IMAGE=artifactory.algol60.net/docker.io/library/alpine:3.17
FROM        ${ALPINE_IMAGE} AS deps
USER        root
WORKDIR     /root
VOLUME      [ "/root/mounted" ]
RUN         apk add --no-cache \
              cmake=3.24.3-r0 \
              g++=12.2.1_git20220924-r4 \
              gcc=12.2.1_git20220924-r4 \
              git=2.38.4-r0 \
              libffi-dev=3.4.4-r0 \
              make=4.3-r1 \
              musl-dev=1.2.3-r4 \
              openssl=3.0.8-r0 \
              py3-pip=22.3.1-r1 \
              py3-virtualenv=20.16.7-r0 \
              python3=3.10.10-r0 \
              python3-dev=3.10.10-r0
ENV         VIRTUAL_ENV=/opt/venv
RUN         python -m venv $VIRTUAL_ENV
ENV         PATH="$VIRTUAL_ENV/bin:$PATH"

# STAGE 2 - install canu in editable mode
FROM        deps AS dev
USER        root
WORKDIR     /root
VOLUME      [ "/root/mounted", "/ssh-agent" ]
ENV         VIRTUAL_ENV=/opt/venv \
            SSH_AUTH_SOCK=/ssh-agent
RUN         apk --update add \
              openssh-client=9.1_p1-r2
RUN         source $VIRTUAL_ENV/bin/activate
COPY        .flake8 ./.flake8
COPY        .git/ ./.git
COPY        .darglint ./.darglint
COPY        canu/ ./canu
COPY        docs/ ./docs
COPY        network_modeling/ ./network_modeling
COPY        pyinstaller_hooks/ ./pyinstaller_hooks
COPY        tests/ ./tests
COPY        canu.spec ./canu.spec
COPY        canuctl ./canuctl
COPY        Dockerfile ./Dockerfile
COPY        entry_points.ini ./entry_points.ini
COPY        LICENSE ./LICENSE
COPY        Makefile ./Makefile
COPY        MANIFEST.in ./MANIFEST.in
COPY        noxfile.py ./noxfile.py
COPY        pyinstaller.py ./pyinstaller.py
COPY        pyproject.toml ./pyproject.toml
RUN         python -m pip install --editable .

# STAGE 3 - build the binaries with pyinstaller
FROM        dev AS build
USER        root
WORKDIR     /root
# must mount ${SSH_AUTH_SOCK} to /ssh-agent to use host ssh
VOLUME      [ "/root/mounted"]
RUN         source $VIRTUAL_ENV/bin/activate
RUN         python -m pip install . pyinstaller
RUN         cp -pv pyinstaller.py pyinstaller.spec
RUN         pyinstaller --clean -y --dist ./dist/linux --workpath /tmp pyinstaller.spec

# STAGE 4 - final production image
FROM        ${ALPINE_IMAGE} AS prod
USER        root
# ssh is needed for 'canu test' command
RUN         apk --update add \
              openssh-client=9.1_p1-r2
# must mount ${SSH_AUTH_SOCK} to /ssh-agent to use host ssh
VOLUME      [ "/home/canu/mounted", "/ssh-agent" ]
ENV         VIRTUAL_ENV=/opt/venv \
            SSH_AUTH_SOCK=/ssh-agent
# copy the binaries.  The final image has the base image, ssh, and these binaries only
COPY        --from=build /root/dist/linux/canu /usr/local/bin/canu
COPY        --from=build /root/dist/linux/canu-inventory /usr/local/bin/canu-inventory
RUN         addgroup -S canu && \
              adduser \
              -S canu \
              -G canu \
              -h /home/canu \
              -s /bin/bash \
              -D
USER        canu
WORKDIR     /home/canu
RUN         mkdir -p /home/canu/mounted
ENV         CANU_NET="HMN" \
            PS1="canu \w$ " \
            REQUESTS_CA_BUNDLE="" \
            SLS_API_GW="api-gw-service.local" \
            SLS_FILE="" \
            SLS_TOKEN="" \
            SSH_AUTH_SOCK=/ssh-agent \
            SWITCH_USERNAME="admin" \
            SWITCH_PASSWORD=""
CMD         [ "sh" ]
