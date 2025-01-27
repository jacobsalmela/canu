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
"""Test CANU validate network config commands."""
from os import mkdir, urandom
from unittest.mock import patch

from click import testing
from netmiko import NetmikoAuthenticationException, NetmikoTimeoutException

from canu.cli import cli
from .test_validate_switch_config import switch_config


username = "admin"
password = "admin"
ips = "192.168.1.1"
credentials = {"username": username, "password": password}
cache_minutes = 0
running_config_file = "running_switch.cfg"
csm = "1.0"
runner = testing.CliRunner()


@patch("canu.validate.switch.config.config.switch_vendor")
@patch("canu.validate.switch.config.config.netmiko_command")
def test_validate_network_config(netmiko_command, switch_vendor):
    """Test that the `canu validate network config` command runs."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        switch_vendor.return_value = "aruba"
        netmiko_command.return_value = "sw-spine-001"
        netmiko_command.return_value = switch_config
        mkdir("generated")
        with open("generated/sw-spine-001.cfg", "w") as f:
            f.writelines(switch_config_edit)

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "validate",
                "network",
                "config",
                "--ips",
                ips,
                "--username",
                username,
                "--password",
                password,
                "--generated",
                "generated/",
                "--csm",
                csm,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Switch: sw-spine-001 (192.168.1.1)\n"
            + "Differences\n"
            + "-------------------------------------------------------------------------\n"
            + "In Generated Not In Running (+)     |  In Running Not In Generated (-)   \n"
            + "-------------------------------------------------------------------------\n"
            + "Total Additions:                 1  |  Total Deletions:                 1\n"
            + "                                    |  Script:                          1\n"
            + "Router:                          1  |                                    \n"
        ) in str(result.output)


def test_validate_network_config_running_file():
    """Test that the `canu validate network config` command runs."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        mkdir("running")
        mkdir("generated")
        with open("running/running_switch.cfg", "w") as f:
            f.writelines(switch_config)
        with open("generated/sw-spine-001.cfg", "w") as f:
            f.writelines(switch_config_edit)

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "validate",
                "network",
                "config",
                "--running",
                "running/",
                "--generated",
                "generated/",
                "--csm",
                csm,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Switch: sw-spine-001\n"
            + "Differences\n"
            + "-------------------------------------------------------------------------\n"
            + "In Generated Not In Running (+)     |  In Running Not In Generated (-)   \n"
            + "-------------------------------------------------------------------------\n"
            + "Total Additions:                 1  |  Total Deletions:                 1\n"
            + "                                    |  Script:                          1\n"
            + "Router:                          1  |                                    \n"
        ) in str(result.output)


@patch("canu.validate.switch.config.config.switch_vendor")
@patch("canu.validate.switch.config.config.netmiko_command")
def test_validate_network_config_file(netmiko_command, switch_vendor):
    """Test that the `canu validate network config` command runs from a file."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        switch_vendor.return_value = "aruba"
        netmiko_command.return_value = "sw-spine-001"
        netmiko_command.return_value = switch_config
        mkdir("generated")
        with open("test.txt", "w") as f:
            f.write("192.168.1.1")

        with open("generated/sw-spine-001.cfg", "w") as f:
            f.writelines(switch_config_edit)

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "validate",
                "network",
                "config",
                "--ips-file",
                "test.txt",
                "--username",
                username,
                "--password",
                password,
                "--generated",
                "generated/",
                "--csm",
                csm,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Switch: sw-spine-001 (192.168.1.1)\n"
            + "Differences\n"
            + "-------------------------------------------------------------------------\n"
            + "In Generated Not In Running (+)     |  In Running Not In Generated (-)   \n"
            + "-------------------------------------------------------------------------\n"
            + "Total Additions:                 1  |  Total Deletions:                 1\n"
            + "                                    |  Script:                          1\n"
            + "Router:                          1  |                                    \n"
        ) in str(result.output)


@patch("canu.validate.switch.config.config.switch_vendor")
@patch("canu.validate.switch.config.config.netmiko_command")
def test_validate_network_config_password_prompt(netmiko_command, switch_vendor):
    """Test that the `canu validate network config` command runs and prompts for password."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        switch_vendor.return_value = "aruba"
        netmiko_command.return_value = "sw-spine-001"
        netmiko_command.return_value = switch_config
        mkdir("generated")
        with open("generated/sw-spine-001.cfg", "w") as f:
            f.writelines(switch_config_edit)

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "validate",
                "network",
                "config",
                "--ips",
                ips,
                "--username",
                username,
                "--generated",
                "generated/",
                "--csm",
                csm,
            ],
            input=password,
        )
        assert result.exit_code == 0
        assert (
            "Switch: sw-spine-001 (192.168.1.1)\n"
            + "Differences\n"
            + "-------------------------------------------------------------------------\n"
            + "In Generated Not In Running (+)     |  In Running Not In Generated (-)   \n"
            + "-------------------------------------------------------------------------\n"
            + "Total Additions:                 1  |  Total Deletions:                 1\n"
            + "                                    |  Script:                          1\n"
            + "Router:                          1  |                                    \n"
        ) in str(result.output)


@patch("canu.validate.switch.config.config.switch_vendor")
@patch("canu.validate.switch.config.config.netmiko_command")
def test_validate_network_config_timeout(netmiko_command, switch_vendor):
    """Test that the `canu validate network config` command errors on timeout."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        switch_vendor.return_value = "aruba"
        netmiko_command.side_effect = NetmikoTimeoutException
        mkdir("generated")
        with open("generated/sw-spine-001.cfg", "w") as f:
            f.writelines(switch_config_edit)

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "validate",
                "network",
                "config",
                "--ips",
                ips,
                "--username",
                username,
                "--password",
                password,
                "--generated",
                "generated/",
                "--csm",
                csm,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Errors\n"
            + "----------------------------------------------------------------------------------------------------\n"
            + "192.168.1.1     - Timeout error. Check the IP address and try again.\n"
        ) in str(result.output)


@patch("canu.validate.switch.config.config.switch_vendor")
@patch("canu.validate.switch.config.config.netmiko_command")
def test_validate_network_config_authentication(netmiko_command, switch_vendor):
    """Test that the `canu validate network config` command errors on authentication."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        switch_vendor.return_value = "aruba"
        netmiko_command.side_effect = NetmikoAuthenticationException
        mkdir("generated")
        with open("generated/sw-spine-001.cfg", "w") as f:
            f.writelines(switch_config_edit)

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "validate",
                "network",
                "config",
                "--ips",
                ips,
                "--username",
                username,
                "--password",
                password,
                "--generated",
                "generated/",
                "--csm",
                csm,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Errors\n"
            + "----------------------------------------------------------------------------------------------------\n"
            + "192.168.1.1     - Authentication error. Check the credentials or IP address and try again"
        ) in str(result.output)


def test_validate_network_config_bad_config_file():
    """Test that the `canu validate network config` command fails on bad file."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        mkdir("running")
        mkdir("generated")
        # Generate random binary file
        with open("running/bad.file", "wb") as f:
            f.write(urandom(128))

        with open("running/bad_config.cfg", "w") as f:
            f.write("bad")

        with open("running/switch.cfg", "w") as f:
            f.writelines(switch_config_edit)
        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "validate",
                "network",
                "config",
                "--running",
                "running/",
                "--generated",
                "generated/",
                "--csm",
                csm,
            ],
        )
        assert result.exit_code == 0
        assert (
            "running/bad_config.cfg - The file running/bad_config.cfg is not a valid config file."
        ) in str(result.output)
        assert (
            "sw-spine-001    - Could not find generated config file generated/sw-spine-001.cfg"
        ) in str(result.output)
        assert (
            "running/bad.file - The file running/bad.file is not a valid config file."
        ) in str(result.output)
