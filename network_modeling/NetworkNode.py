import copy
import logging

import click

log = logging.getLogger(__name__)


class NetworkNode:
    def __init__(self, id=None, hardware=None, architecture=None):
        self.__hw = hardware
        self.__arch = architecture

        self.__id = id
        self.__common_name = None
        self.__total_ports = copy.deepcopy(
            hardware["ports"]
        )  # TODO: Do we need this as deepcopy?
        self.__available_ports_by_speed = copy.deepcopy(
            hardware["ports"]
        )  # TODO: Do we need this as deepcopy?
        self.__edge_connections = []  # A mathematical edge, not a port

        self.__calculate_port_costs()

    # Annotate port information with inherent costs of using this port.
    # TODO:  Replace simple logic in __port_select with this metadata
    def __calculate_port_costs(self):
        pass

    # Select a singular port type from a device given a port speed.
    # This seems trivial, but it's possible that a devices's hardware
    # may have port (sets/list) that have different max speeds and counts
    # but supported (sub-speeds) in the ports overlap:
    #     ports:
    #      - count: 8
    #        speed: [100, 25]
    #      - count: 48
    #        speed: 25
    # Here the port speed of 25 overlaps.  By default the selection would be
    # determined based on the order in the hardware definition file.
    # Here we make this deterministic based on a "cost" based on the highest
    # port speed available: inherently depending on the implication that there
    # will be fewer ports of higher port speed.
    def __port_select(self, speed=None):
        if not isinstance(speed, int):
            raise Exception(
                click.secho(f"{__name__}: Port speed must be an integer", fg="red")
            )
        port = None
        current = None
        speed_cost = 0
        for entry in self.__available_ports_by_speed:
            if speed not in entry["speed"]:
                continue

            # Default to the first entry found
            # TODO: this may have some caveats
            if current is None:
                current = entry

            # Pick the lowest cost by speed (only)
            if max(entry["speed"]) > speed_cost:
                speed_cost = max(entry["speed"])
            else:
                current = entry
        port = current
        return port

    def available_ports(self, speed=None):
        available = self.__port_select(speed=speed)

        if available is None:
            msg = f"{__name__}: Available port at speed {speed} "
            msg += f"not found for {self.common_name()} "
            msg += f'of type {self.__arch["name"]} and '
            msg += f'model {self.__arch["model"]}'
            raise Exception(click.secho(msg, fg="red"))

        # TODO: Do we need to check count?  Probably not since it's required in schema
        # if 'count' not in available:
        #     raise Exception('{}: Port needs a count member'.format(__name__))
        available = available["count"]
        return available

    def __decrement_available_ports(self, speed=None, count=1):
        port = self.__port_select(speed=speed)

        # print(self.__hw)
        # print(self.__available_ports_by_speed)
        # print(port)
        if port is None:
            raise Exception(
                click.secho(
                    f"{__name__}: Port with speed {speed} not available in hardware",
                    fg="red",
                )
            )

        if port["count"] <= 0:
            raise Exception(
                click.secho(
                    f"{__name__}: Port count with speed {speed} cannot be below zero",
                    fg="red",
                )
            )

        port["count"] -= count

        return self.__available_ports_by_speed

    # Determine if a connection is allowed between components.
    #   Returns:  >0 speed of allowed connection if connection is allowed.
    #   Raises:   Exception of the connection is not architecturally allowed.
    #
    # The architectural definition only specifies upward/northbound
    # allowed connections.  Here we have no idea which node is north
    # of the other so we compare "bi-directionally" and return the speed
    # of the south-to-north direction.
    def __connection_allowed(self, node):
        connection_speed = None
        south_node = None
        north_node = None
        match_count = 0

        for connection in self.device_connections():
            if connection["name"] == node.arch_type():
                match_count += 1
                south_node = self
                north_node = node
                connection_speed = connection["speed"]
        for connection in node.device_connections():
            if connection["name"] == self.arch_type():
                match_count += 1
                south_node = node
                north_node = self
                connection_speed = connection["speed"]

        if match_count == 0:
            msg = "No architectural definition found to allow connection between "
            msg += f"{self.common_name()} ({self.arch_type()}) "
            msg += f"and {node.common_name()} ({node.arch_type()}). "
            msg += "\nCheck that the correct architectural was selected."
            raise Exception(click.secho(msg, fg="red"))

        if match_count != 1:
            msg = "Multiple architectural connection matches found between "
            msg += f"{self.common_name()} ({self.arch_type()}) "
            msg += f"and {node.common_name()} ({node.arch_type()}). "
            msg += "Check architectural definition."
            log.warning(msg)

        if south_node is None or north_node is None:
            msg = "Cannot determine architectural direction between "
            msg += f"{self.common_name()} ({self.arch_type()}) "
            msg += f"and {node.common_name()} ({node.arch_type()}).  "
            msg += "Check architectural definition."
            raise Exception(click.secho(msg, fg="red"))

        if connection_speed is None:
            msg = "Connection not architecturally allowed between "
            msg += f"{self.common_name()} ({self.arch_type()}) "
            msg += f"and {node.common_name()} ({node.arch_type()}) at any speed. "
            msg += "Check architectural definition."
            raise Exception(click.secho(msg, fg="red"))

        log.debug(
            f"Connection from {south_node.arch_type()} to {north_node.arch_type()} allowed at speed {connection_speed}"
        )

        return connection_speed

    # TODO:  Get rid of these
    def get_hw(self):
        return self.__hw

    def get_arch(self):
        return self.__arch

    # Unique node ID
    def id(self):
        return self.__id

    def arch_type(self):
        return self.__arch["name"]

    # Get/Set node common name
    # TODO: This is a quick hack.  Could enforce naming standards via arch yaml and/or have
    #       name specified via constructor.
    def common_name(self, name=None):
        if name is not None:
            self.__common_name = name
        return self.__common_name

    # Architecturally allowed connections.
    def device_connections(self):
        # Returns list
        return self.__arch["connections"]

    # Connect one device to another.
    # From a mathematical node-edge perspective, not physical ports
    def connect(self, node, bidirectional=True):

        # Defensively check input node type.
        if not isinstance(node, NetworkNode):
            raise Exception(click.secho("Node needs to be type NetworkNode", fg="red"))

        # Implicit defensive check whether this connection is allowed
        connection_speed = self.__connection_allowed(node)
        log.debug(
            f"Node {self.__id} requests connection to node {node.id()} at speed {connection_speed}"
        )
        log.debug(f"    {len(self.__edge_connections)} existing connections")
        log.debug(
            f"    {self.available_ports(connection_speed)} remaining ports at speed {connection_speed}"
        )

        # Check to make sure we have local ports available
        if self.available_ports(speed=connection_speed) < 1:
            log.debug(f"No ports available at speed {connection_speed}")
            return False

        # First connect the local node to the remote with recursion break
        # If this fails then we "roll back" by exiting out.
        if bidirectional:
            if not node.connect(self, bidirectional=False):
                log.debug(
                    "Connection local to remote connect failed - usually lack of ports"
                )
                return False

        # Second, connect the remote node to the local
        if node.id() not in self.edges():
            self.__edge_connections.append(node.id())
            self.__decrement_available_ports(speed=connection_speed)
            log.debug(
                f"  Successfully connected {node.common_name()} to {self.common_name()} at speed {connection_speed}"
            )
        return True

    # Disconnect one device from another.
    def disconnect(self, node):
        # Defensively check input node type.
        if not isinstance(node, NetworkNode):
            raise Exception(click.secho("Node needs to be type NetworkNode", fg="red"))

        # TODO:  this for real
        return False

    # Return a list of all connections.
    def edges(self):
        return self.__edge_connections