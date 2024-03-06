import os
import sys
import pytest
import logging
import re

# 提取配置信息
config_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(config_path)

from Common.remote_ssh import *
from Common.execute_command import *
from Common.check_base import *
from Common.remote_redfish import *
from Common.get_config import *


@pytest.mark.none_bare_metal
@pytest.mark.bare_metal
def test_ping_bmc():
    if bmc_ip == "192.168.1.10":
        ping_bmc = ssh_execute_command(
            dpu_os_ip, os_username, os_password, f"ping -q -i 0.5 -c 1000 {bmc_ip}"
        )
        packet_loss = re.search(r"(\d+(?:\.\d+)?)% packet loss", ping_bmc)
        if packet_loss:
            packet_loss = packet_loss.group(1)
            logging.info("Packet loss: %s%%", packet_loss)
        else:
            logging.error("No packet loss information found")
        assert int(packet_loss) <= 1, "Error, Packet loss rate is greater than 1%"
    else:
        ping_bmc = execute_command(
            f"ping -q -i 0.5 -c 1000 {bmc_ip}",
            bmc_ip,
            bmc_username,
            bmc_password,
            command_type="outsystem",
        )
        packet_loss = re.search(r"(\d+(?:\.\d+)?)% packet loss", ping_bmc)
        if packet_loss:
            packet_loss = packet_loss.group(1)
            logging.info(f"Packet loss: {packet_loss}%")
        else:
            logging.error("No packet loss information found")
        assert int(packet_loss) <= 1, "Error, Packet loss rate is greater than 1%"
