"""Test CANU validate network config commands."""
from unittest.mock import patch

import click.testing
from netmiko import ssh_exception

from canu.cli import cli
from .test_validate_switch_config import switch_config


def netmiko_mock(*args):
    """Mock netmiko command."""
    return switch_config


def netmiko_mock_timeout(*args):
    """Mock netmiko NetmikoTimeoutException."""
    raise ssh_exception.NetmikoTimeoutException


def netmiko_mock_authentication(*args):
    """Mock netmiko NetmikoAuthenticationException."""
    raise ssh_exception.NetmikoAuthenticationException


username = "admin"
password = "admin"
ips = "192.168.1.1"
credentials = {"username": username, "password": password}
cache_minutes = 0
shasta = "1.4"
# config_file = "sw-spine-001.cfg"
runner = click.testing.CliRunner()


@patch("canu.validate.network.config.config.netmiko_command", side_effect=netmiko_mock)
def test_validate_network_config(*args):
    """Test that the `canu validate network config` command runs."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        with open("sw-spine-001.cfg", "w") as f:
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
                "--config",
                ".",
                "-s",
                shasta,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Switch: sw-spine-001 (192.168.1.1)\n"
            "Differences\n"
            "-------------------------------------------------------------------------\n"
            "In Generated Not In Running (+)     |  In Running Not In Generated (-)   \n"
            "-------------------------------------------------------------------------\n"
            "Total Additions:                 1  |  Total Deletions:                 1\n"
            "                                    |  Script:                          1\n"
            "Router:                          1  |                                    \n"
        ) in str(result.output)


@patch("canu.validate.network.config.config.netmiko_command", side_effect=netmiko_mock)
def test_validate_network_config_file(*args):
    """Test that the `canu validate network config` command runs from a file."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("192.168.1.1")

        with open("sw-spine-001.cfg", "w") as f:
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
                "--config",
                ".",
                "-s",
                shasta,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Switch: sw-spine-001 (192.168.1.1)\n"
            "Differences\n"
            "-------------------------------------------------------------------------\n"
            "In Generated Not In Running (+)     |  In Running Not In Generated (-)   \n"
            "-------------------------------------------------------------------------\n"
            "Total Additions:                 1  |  Total Deletions:                 1\n"
            "                                    |  Script:                          1\n"
            "Router:                          1  |                                    \n"
        ) in str(result.output)


@patch(
    "canu.validate.network.config.config.netmiko_command",
    side_effect=netmiko_mock_timeout,
)
def test_validate_network_config_timeout(*args):
    """Test that the `canu validate network config` command errors on timeout."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        with open("sw-spine-001.cfg", "w") as f:
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
                "--config",
                ".",
                "-s",
                shasta,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Errors\n"
            "----------------------------------------------------------------------------------------------------\n"
            "192.168.1.1     - Timeout error connecting to switch 192.168.1.1, check the IP address and try again.\n"
        ) in str(result.output)


@patch(
    "canu.validate.network.config.config.netmiko_command",
    side_effect=netmiko_mock_authentication,
)
def test_validate_network_config_authentication(*args):
    """Test that the `canu validate network config` command errors on authentication."""
    switch_config_edit = switch_config[:-15] + "router add\n"
    with runner.isolated_filesystem():
        with open("sw-spine-001.cfg", "w") as f:
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
                "--config",
                ".",
                "-s",
                shasta,
            ],
        )
        assert result.exit_code == 0
        assert (
            "Errors\n"
            "----------------------------------------------------------------------------------------------------\n"
            "192.168.1.1     - Authentication error connecting to switch 192.168.1.1, check the credentials or IP ad"
        ) in str(result.output)