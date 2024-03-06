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


@pytest.mark.none_bare_metal
def test_update_bios_inband_default():
    # 根据产品制造商选择配置
    script_default_downgrade, script_default_upgrade = get_update_bios_inband_script(
        retain=False, bare_metal=False
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

    # 使用BMC用户信息进行登录Redfish, 如果登录失败, 则抛出异常
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
    bios_settings_before = Redfish_Get_Bios_Settings(token)
    if "G220-BA-B" == machine_model:
        logging.info(f'CRBCI3: {bios_settings_before["CRBCI3"]}')
        assert (
            bios_settings_before["CRBCI3"] == "CRBCI3Disable"
        ), "Redfish Setting BIOS Settings Failed"
    else:
        logging.info(f'QuietBoot: {bios_settings_before["QuietBoot"]}')
        if (
            "S820-A3" == machine_model
            or "S820-A6" == machine_model
            or "S820-A9" == machine_model
            or "G225-B5" == machine_model
            or "G225-B6" == machine_model
            or "G225-B9" == machine_model
        ):
            assert (
                bios_settings_before["QuietBoot"] == True
            ), "Redfish Setting BIOS Settings Failed"
        else:
            assert (
                bios_settings_before["QuietBoot"] == "Enabled"
            ), "Redfish Setting BIOS Settings Failed"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"

    # 带内执行升降级脚本进行降级（不保留配置）
    logging.info("Inband Update BIOS Begin")
    inband_update_log = execute_command(
        command="cd {} && {}".format(inband_update_file_path, script_default_downgrade),
        command_type="outsystem",
    )
    assert inband_update_log, "Inband Update Failed"
    Command_Check("chassis power cycle")
    assert ping_ip(
        os_ip, timeout=30, ping_test="fail"
    ), "after power cycle 30s, ping os ip success"
    # ping OS IP,超时时间1800s，如果ping失败则抛出异常
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
    if "G220-BA-B" == machine_model:
        logging.info(f'CRBCI3: {bios_settings_middle["CRBCI3"]}')
        assert (
            bios_settings_middle["CRBCI3"] == "CRBCI3Enable"
        ), "Bios Downgrade Default, CRBCI3 Should Be CRBCI3Enable, But Now isn't CRBCI3Enable"
    else:
        logging.info(f'QuietBoot: {bios_settings_middle["QuietBoot"]}')
        if (
            "S820-A3" == machine_model
            or "S820-A6" == machine_model
            or "S820-A9" == machine_model
            or "G225-B5" == machine_model
            or "G225-B6" == machine_model
            or "G225-B9" == machine_model
        ):
            assert (
                bios_settings_middle["QuietBoot"] == False
            ), "Bios Downgrade Default, QuietBoot Should Be False, But Now isn't False"
        else:
            assert (
                bios_settings_middle["QuietBoot"] == "Disabled"
            ), "Bios Downgrade Default, QuietBoot Should Be Disabled, But Now isn't Disabled"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"

    # 获取sel并检查是否存在告警sel
    Sel_Check()

    # 使用BMC用户信息进行登录Redfish, 如果登录失败, 则抛出异常
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
    bios_settings_middle_change = Redfish_Get_Bios_Settings(token)
    if "G220-BA-B" == machine_model:
        logging.info(f'CRBCI3: {bios_settings_middle_change["CRBCI3"]}')
        assert (
            bios_settings_middle_change["CRBCI3"] == "CRBCI3Disable"
        ), "Redfish Setting BIOS Settings Failed"
    else:
        logging.info(f'QuietBoot: {bios_settings_middle_change["QuietBoot"]}')
        if (
            "S820-A3" == machine_model
            or "S820-A6" == machine_model
            or "S820-A9" == machine_model
            or "G225-B5" == machine_model
            or "G225-B6" == machine_model
            or "G225-B9" == machine_model
        ):
            assert (
                bios_settings_middle_change["QuietBoot"] == True
            ), "Redfish Setting BIOS Settings Failed"
        else:
            assert (
                bios_settings_middle_change["QuietBoot"] == "Enabled"
            ), "Redfish Setting BIOS Settings Failed"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"

    # 带内执行升降级脚本进行升级（不保留配置）
    logging.info("Inband Update BIOS Begin")
    inband_update_log = execute_command(
        command="cd {} && {}".format(inband_update_file_path, script_default_upgrade),
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
    if "G220-BA-B" == machine_model:
        logging.info(f'CRBCI3: {bios_settings_after["CRBCI3"]}')
        assert (
            bios_settings_after["CRBCI3"] == "CRBCI3Enable"
        ), "Bios Upgrade Default, CRBCI3 Should Be CRBCI3Enable, But Now isn't CRBCI3Enable"
    else:
        logging.info(f'QuietBoot: {bios_settings_after["QuietBoot"]}')
        if (
            "S820-A3" == machine_model
            or "S820-A6" == machine_model
            or "S820-A9" == machine_model
            or "G225-B5" == machine_model
            or "G225-B6" == machine_model
            or "G225-B9" == machine_model
        ):
            assert (
                bios_settings_after["QuietBoot"] == False
            ), "Bios Upgrade Default, QuietBoot Should Be False, But Now isn't False"
        else:
            assert (
                bios_settings_after["QuietBoot"] == "Disabled"
            ), "Bios Upgrade Default, QuietBoot Should Be Disabled, But Now isn't Disabled"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"

    # 获取sel并检查是否存在告警sel
    Sel_Check()
