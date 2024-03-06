import os
import sys
import pytest

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
def test_bmc_access():
    # bmc ssh登录
    output = ssh_execute_command(
        bmc_ip, bmc_ssh_username, bmc_ssh_error_password, "pwd"
    )
    assert (
        output == False
    ), "Error,bmc ssh login success with error username/password, please check it"

    # ipmitool lanplus 远程访问
    outband_output = Command_Check("mc info")
    assert "IPMI Version" in outband_output, "Error, ipmitool lanplus failed"

    # ipmitool inband 访问
    inband_output = ssh_execute_command(
        os_ip, os_username, os_password, "ipmitool mc info"
    )
    assert "IPMI Version" in inband_output, "Error, ipmitool inband failed"
