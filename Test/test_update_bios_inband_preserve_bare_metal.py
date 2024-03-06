import os
import sys
import random
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


@pytest.mark.bare_metal
def test_update_bios_inband_preserve_bare_metal():
    # 根据产品制造商选择配置
    script_preserve_downgrade, script_preserve_upgrade = get_update_bios_inband_script(
        retain=True, bare_metal=True
    )

    # 清除sel并检查清除是否成功
    Sel_Clear()

    # 获取BIOS版本是否为升级版本
    bios_version = Get_BIOS_FW_Version(os_ip, os_username, os_password)
    assert (
        bios_version == upgrade_bios_version
    ), "BIOS Version Is Not The Upgrade Version OR Get BIOS Version Failed"

    # 清除OS下的dmesg信息和messages信息
    assert Clear_Message_In_Os(
        os_ip, os_username, os_password
    ), "Clear Message In OS Failed"

    # 使用BMC用户信息进行登录Redfish,如果登录失败,则抛出异常
    token, session_id = login_to_redfish_bmc()
    assert token and session_id, "Redfish Create Session Fail"
    assert Redfish_Change_Bios_Settings(token)

    # 执行Power Cycle电源控制操作,并确认执行成功
    Command_Check("chassis power cycle")
    assert ping_ip(
        os_ip, timeout=30, ping_test="fail"
    ), "after power cycle 30s, ping os ip success"

    # ping OS IP, 超时时间600s, 如果ping失败则抛出异常
    assert ping_ip(
        os_ip, timeout=600, ping_test="pass"
    ), "after 600s, ping os ip failed, please check os status"

    # 获取BIOS设置
    bios_settings_before = Redfish_Get_Bios_Settings(redfish_bmc_ip, token, system_id)
    logging.info(f'QuietBoot: {bios_settings_before["QuietBoot"]}')
    if "R5500G5-2" == machine_model:
        assert (
            bios_settings_before["QuietBoot"] == "Disabled"
        ), "Redfish Setting BIOS Settings Failed"
    elif (
        "G225-B5-2" == machine_model
        or "G225-B6-2" == machine_model
        or "G225-B9-2" == machine_model
    ):
        assert (
            bios_settings_before["QuietBoot"] == False
        ), "Redfish Setting BIOS Settings Failed"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"

    # 带内执行升降级脚本进行降级（保留配置）
    logging.info("Inband Update BIOS Begin")
    inband_update_log = execute_command(
        command="cd {} && {}".format(
            inband_update_file_path, script_preserve_downgrade
        ),
        command_type="outsystem",
    )
    assert inband_update_log, "Inband Update Failed"
    Command_Check("chassis power cycle")
    assert ping_ip(
        os_ip, timeout=30, ping_test="fail"
    ), "after power cycle 30s, ping os ip success"
    # ping OS IP,超时时间1200s，如果ping失败则抛出异常
    assert ping_ip(
        os_ip, timeout=1800, ping_test="pass"
    ), "after 1800s, ping os ip failed, please check bios update result"
    logging.info("Inband Update BIOS Finish")

    # 获取OS下的dmesg信息和messages信息
    assert Get_Message_In_OS(
        os_ip, os_username, os_password
    ), "Get Message In OS Failed"

    # 获取BIOS版本是否为降级版本
    bios_version = Get_BIOS_FW_Version(os_ip, os_username, os_password)
    assert (
        bios_version == downgrade_bios_version
    ), "BIOS Version Is Not The Downgrade Version OR Get BIOS Version Failed"

    # 使用BMC用户信息进行登录Redfish,如果登录失败,则抛出异常
    token, session_id = login_to_redfish_bmc()
    assert token and session_id, "Redfish Create Session Fail"
    bios_settings_middle = Redfish_Get_Bios_Settings(token)
    logging.info(f'QuietBoot: {bios_settings_middle["QuietBoot"]}')
    if "R5500G5-2" == machine_model:
        assert (
            bios_settings_middle["QuietBoot"] == "Disabled"
        ), "Bios Downgrade Preserve, QuietBoot Should Be Disabled, But Now isn't Disabled"
    elif (
        "G225-B5-2" == machine_model
        or "G225-B6-2" == machine_model
        or "G225-B9-2" == machine_model
    ):
        assert (
            bios_settings_middle["QuietBoot"] == False
        ), "Bios Downgrade Preserve, QuietBoot Should Be False, But Now isn't False"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"

    # 获取sel并检查是否存在告警sel
    Sel_Check()

    # 带内执行升降级脚本进行升级（保留配置）
    logging.info("Inband Update BIOS Begin")
    inband_update_log = execute_command(
        command="cd {} && {}".format(inband_update_file_path, script_preserve_upgrade),
        command_type="outsystem",
    )
    assert inband_update_log, "Inband Update Failed"
    Command_Check("chassis power cycle")
    assert ping_ip(
        os_ip, timeout=30, ping_test="fail"
    ), "after power cycle 30s, ping os ip success"
    # ping OS IP,超时时间1200s，如果ping失败则抛出异常
    assert ping_ip(
        os_ip, timeout=1800, ping_test="pass"
    ), "after 1800s, ping os ip failed, please check bios update result"
    logging.info("Inband Update BIOS Finish")

    # 获取OS下的dmesg信息和messages信息
    assert Get_Message_In_OS(
        os_ip, os_username, os_password
    ), "Get Message In OS Failed"

    # 获取BIOS版本是否为升级版本
    bios_version = Get_BIOS_FW_Version(os_ip, os_username, os_password)
    assert (
        bios_version == upgrade_bios_version
    ), "BIOS Version Is Not The Upgrade Version OR Get BIOS Version Failed"

    # 使用BMC用户信息进行登录Redfish,如果登录失败,则抛出异常
    token, session_id = login_to_redfish_bmc()
    assert token and session_id, "Redfish Create Session Fail"
    bios_settings_after = Redfish_Get_Bios_Settings(token)
    logging.info(f'QuietBoot: {bios_settings_after["QuietBoot"]}')
    if "R5500G5-2" == machine_model:
        assert (
            bios_settings_after["QuietBoot"] == "Disabled"
        ), "Bios Upgrade Preserve, QuietBoot Should Be Disabled, But Now isn't Disabled"
    elif (
        "G225-B5-2" == machine_model
        or "G225-B6-2" == machine_model
        or "G225-B9-2" == machine_model
    ):
        assert (
            bios_settings_after["QuietBoot"] == False
        ), "Bios Upgrade Preserve, QuietBoot Should Be False, But Now isn't False"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"

    # 获取sel并检查是否存在告警sel
    Sel_Check()
