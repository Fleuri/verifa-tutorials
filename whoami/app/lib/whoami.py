"""Displays information on the environment it's currently running in."""

import os
from pip import __version__ as pip_version
import platform
import socket
from typing import Collection, Dict, List, Tuple
from uuid import getnode

from flask import __version__ as flask_version  # type: ignore


class Whoami:
    """Displays information on the environment it's currently running in."""

    def __init__(self) -> None:
        # Creates a new Whoami instance
        self.status = []  # type: List[str]
        self._set_mac("unknown")
        self._set_environment_vars_to_print(["USER", "LANG"], "undefined")

    # Getters should be mostly self-explanatory

    def get_environment_variables(self) -> Tuple[str]:
        return (", ".join(map(str, list(os.environ.keys()))),)

    def get_mac(self) -> str:
        return self.mac

    def get_ip(self) -> str:
        return socket.gethostbyname(socket.gethostname())

    def get_hostname(self) -> str:
        return socket.gethostname()

    def get_platform(self) -> str:
        return platform.platform()

    def get_python_version(self) -> str:
        return platform.python_version()

    def get_status(self) -> str:
        """
        Checks the current status of the Whoami instance.

        Returns:
            "running" if a valid MAC address and all desired environment
            variables were found.
            A comma-separated list of error messages as a string
            otherwise.
        """
        if not self.status:
            return "running"
        else:
            return ", ".join(map(str, self.status))

    def format_mac(self, address_to_format: int) -> str:
        """
        Formats an integer as a MAC address.

        Returns:
            A semicolon-delimited string of hexadecimal digit pairs.
        """
        return ":".join(
            ("%012X" % address_to_format)[i : i + 2] for i in range(0, 12, 2)
        )

    def to_json(self) -> Dict[str, Collection[str]]:
        """
        Returns the current Whoami instance as Json.

        Returns:
            The current Whoami instance as a dictionary of
            Json-formatted strings.
        """
        return {
            "whoami": {
                "hostname": self.get_hostname(),
                "IP address": self.get_ip(),
                "platform": self.get_platform(),
                "MAC address": self.get_mac(),
                "environment variables": self.get_environment_variables(),
                "selected variables": self.environment_vars_to_print,
            },
            "version": {
                "python": self.get_python_version(),
                "flask": flask_version,
                "pip": pip_version,
            },
            "status": self.get_status(),
        }

    # Internal methods below

    def _set_mac(self, error_message: str) -> None:
        # Set the MAC address
        mac = getnode()
        if (mac >> 40) % 2:
            # Check if getnode() returned a spoofed address
            self.status.append("MAC address {msg}".format(msg=error_message))
            self.mac = error_message
        else:
            # Format the MAC address in the familiar fashion
            self.mac = self.format_mac(mac)

    def _set_environment_vars_to_print(
        self, vars_to_print: List[str], error_message: str
    ) -> None:
        # Retrieve the environment variables which should be printed (if they exist)
        self.environment_vars_to_print = {}
        for var in vars_to_print:
            if os.environ.get(var) is None:
                self.status.append(
                    "environment variable {var} {msg}".format(
                        var=var, msg=error_message
                    )
                )
                self.environment_vars_to_print[var] = error_message
            else:
                self.environment_vars_to_print[var] = str(os.environ.get(var))
