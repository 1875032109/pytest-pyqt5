import os
import sys
import time
from pytest_assume.plugin import assume
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
def test_update_bmc_outband_default():
    # 根据产品制造商选择配置
    script_default_downgrade, script_default_upgrade = get_update_bios_outband_script(
        retain=False, bare_metal=False
    )

    # 清除sel并检查清除是否成功
    Sel_Clear()

    # 获取BMC版本是否为升级版本
    bmc_version = Get_BMC_FW_Version(os_ip, os_username, os_password)
    assert (
        bmc_version == upgrade_bmc_version
    ), "BMC Version Is Not The Upgrade Version OR Get BMC Version Failed"

    # 清除OS下的dmesg信息和messages信息
    assert Clear_Message_In_Os(
        os_ip, os_username, os_password
    ), "Clear Message In OS Failed"

    # 创建用户test
    Create_User("3", "test", "12345678", "OPERATOR")

    # 获取Fru, User, Network, Sdr, Seneor信息
    (
        fru_info_before,
        user_info_before,
        sdr_info_before,
        sensor_info_before,
    ) = Get_System_Info(os_ip, os_username, os_password)
    assert (
        fru_info_before and user_info_before and sdr_info_before and sensor_info_before
    ), "Get System Info Failed"
    sdr_info_before = Sdr_Info_Treat(sdr_info_before)
    sensor_info_before = Sensor_Info_Treat(sensor_info_before)
    assert sdr_info_before and sensor_info_before, "sdr or sensor info treat failed"
    bmc_network_before = Get_BMC_Network(os_ip, os_username, os_password, lan_channel)
    assert bmc_network_before, "Get BMC Network Failed"

    # 带外执行升降级脚本进行降级（不保留配置）
    logging.info("Outband Update BMC Begin")
    outband_update_log = execute_command(
        command="cd {} && {}".format(
            outband_update_file_path, script_default_downgrade
        ),
        command_type="outsystem",
    )
    assert outband_update_log, "Outband Update Failed"
    if machine_model == "G220-BA-B" or machine_model == "NF5468M7":
        pass
    else:
        time.sleep(360)
        bmc_status = Command_Check("mc info")
        if bmc_status:
            pass
        else:
            time.sleep(60)
    logging.info("Outband Update BMC Finish")

    # 检查网络模式是否恢复默认dhcp
    bmc_network_middle = Get_BMC_Network(os_ip, os_username, os_password, lan_channel)
    assert (
        bmc_network_middle["ip_source"] == "dhcp"
        and bmc_network_middle["ip"] == "0.0.0.0"
        and (
            bmc_network_middle["netmask"] == "0.0.0.0"
            or bmc_network_middle["netmask"] == "255.255.255.255"
        )
        and bmc_network_middle["gateway"] == "0.0.0.0"
    ), "After BMC Recover Factory Mode, Network Not Recover Default"
    assert bmc_network_before["mac"] == bmc_network_middle["mac"], "mac have changed"

    # 设置BMC网络信息
    Set_BMC_Network(os_ip, os_username, os_password, bmc_ip, lan_channel)

    # ping BMC IP,超时时间90s，如果ping失败则抛出异常
    assert ping_ip(ip=bmc_ip, timeout=90, ping_test="pass"), "Ping BMC IP Failed"

    # 通过SSH获取BMC用户信息。如果连接失败,则抛出异常
    users = ssh_get_user_info(os_ip, os_username, os_password)
    assert users, "ssh connect failed or ssh execute cmd failed"

    # 验证恢复出厂设置后,用户信息是否符合机型的要求,如果不符合则抛出异常
    assert validate_users(users, user_count), "validate users failed"

    # 获取OS下的dmesg信息和messages信息
    assert Get_Message_In_OS(
        os_ip, os_username, os_password
    ), "Get Message In OS Failed"

    # 获取BMC版本是否为降级版本
    bmc_version = Get_BMC_FW_Version(os_ip, os_username, os_password)
    assert (
        bmc_version == downgrade_bmc_version
    ), "BMC Version Is Not The Downgrade Version OR Get BMC Version Failed"

    # 获取Fru, User, Network, Sdr, Seneor信息
    (
        fru_info_middle,
        user_info_middle,
        sdr_info_middle,
        sensor_info_middle,
    ) = Get_System_Info(os_ip, os_username, os_password)
    assert (
        fru_info_middle and user_info_middle and sdr_info_middle and sensor_info_middle
    ), "Get System Info Failed"
    sdr_info_middle = Sdr_Info_Treat(sdr_info_middle)
    sensor_info_middle = Sensor_Info_Treat(sensor_info_middle)
    assert sdr_info_middle and sensor_info_middle, "sdr or sensor info treat failed"
    assume(
        list_diff(fru_info_before, fru_info_middle, "fru")
    ), "不保留配置降级后和初始fru信息不一致"
    assume(
        list_diff(sdr_info_before, sdr_info_middle, "sdr elist")
    ), "不保留配置降级后和初始sdr信息不一致"
    assume(
        list_diff(sensor_info_before, sensor_info_middle, "sensor list")
    ), "不保留配置降级后和初始sensor信息不一致"

    # 获取sel并检查是否存在告警sel
    Sel_Check()

    # 创建用户test
    Create_User("3", "test", "12345678", "OPERATOR")

    # 带外执行升降级脚本进行升级（不保留配置）
    logging.info("Outband Update BMC Begin")
    outband_update_log = execute_command(
        command="cd {} && {}".format(outband_update_file_path, script_default_upgrade),
        command_type="outsystem",
    )
    assert outband_update_log, "Outband Update Failed"
    if machine_model == "G220-BA-B":
        pass
    else:
        time.sleep(360)
        bmc_status = Command_Check("mc info")
        if bmc_status:
            pass
        else:
            time.sleep(60)
    logging.info("Outband Update BMC Finish")

    # 检查网络模式是否恢复默认dhcp
    bmc_network_after = Get_BMC_Network(os_ip, os_username, os_password, lan_channel)
    assert (
        bmc_network_after["ip_source"] == "dhcp"
        and bmc_network_after["ip"] == "0.0.0.0"
        and (
            bmc_network_after["netmask"] == "0.0.0.0"
            or bmc_network_after["netmask"] == "255.255.255.255"
        )
        and bmc_network_after["gateway"] == "0.0.0.0"
    ), "After BMC Recover Factory Mode, Network Not Recover Default"
    assert bmc_network_before["mac"] == bmc_network_after["mac"], "mac have changed"

    # 设置BMC网络信息
    Set_BMC_Network(os_ip, os_username, os_password, bmc_ip, lan_channel)

    # ping BMC IP,超时时间90s，如果ping失败则抛出异常
    assert ping_ip(ip=bmc_ip, timeout=90, ping_test="pass"), "Ping BMC IP Failed"

    # 通过SSH获取BMC用户信息。如果连接失败,则抛出异常
    users = ssh_get_user_info(os_ip, os_username, os_password)
    assert users, "ssh connect failed or ssh execute cmd failed"

    # 验证恢复出厂设置后,用户信息是否符合机型的要求,如果不符合则抛出异常
    assert validate_users(users, user_count), "validate users failed"

    # 获取OS下的dmesg信息和messages信息
    assert Get_Message_In_OS(
        os_ip, os_username, os_password
    ), "Get Message In OS Failed"

    # 获取BMC版本是否为升级版本
    bmc_version = Get_BMC_FW_Version(os_ip, os_username, os_password)
    assert (
        bmc_version == upgrade_bmc_version
    ), "BMC Version Is Not The Upgrade Version OR Get BMC Version Failed"
    (
        fru_info_after,
        user_info_after,
        sdr_info_after,
        sensor_info_after,
    ) = Get_System_Info(os_ip, os_username, os_password)
    assert (
        fru_info_after and user_info_after and sdr_info_after and sensor_info_after
    ), "Get System Info Failed"
    sdr_info_after = Sdr_Info_Treat(sdr_info_after)
    sensor_info_after = Sensor_Info_Treat(sensor_info_after)
    assert sdr_info_after and sensor_info_after, "sdr or sensor info treat failed"
    assume(
        list_diff(fru_info_before, fru_info_after, "fru")
    ), "不保留配置升级后和初始fru信息不一致"
    assume(
        list_diff(sdr_info_before, sdr_info_after, "sdr elist")
    ), "不保留配置升级后和初始sdr信息不一致"
    assume(
        list_diff(sensor_info_before, sensor_info_after, "sensor list")
    ), "不保留配置升级后和初始sensor信息不一致"

    # 获取sel并检查是否存在告警sel
    Sel_Check()
