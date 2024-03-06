import os
import sys
import random
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
def test_user_check():
    # 通过SSH获取BMC用户数量。如果连接失败,则抛出异常
    ipmi_user_count = ssh_get_user_count(os_ip, os_username, os_password)
    assert ipmi_user_count, "ssh connect failed or ssh execute cmd failed"

    # 通过SSH获取BMC用户信息。如果连接失败,则抛出异常
    users = ssh_get_user_info(os_ip, os_username, os_password)
    assert users, "ssh connect failed or ssh execute cmd failed"
    ipmi_default_user_info = users[1]
    logging.info("Ipmi Default User Info:{}".format(ipmi_default_user_info))

    # 验证用户信息是否符合机型的要求,如果不符合则抛出异常
    assert validate_users(users, user_count), "validate users failed"

    # 使用BMC用户信息进行登录Redfish,如果登录失败,则抛出异常
    token, session_id = login_to_redfish_bmc()
    assert token and session_id, "Redfish Create Session Fail"

    # Redfish获取用户信息,如果获取失败,则抛出异常
    if machine_model == "G220-BA-B":
        real_id = "toutiao"
    else:
        real_id = 2
    redfish_default_user_info = Redfish_Get_User_Info(token, real_id)
    assert redfish_default_user_info, "Redfish Get User Info Fail"

    # 检查IPMI获取的默认用户信息和Redfish获取的默认用户信息是否一致,如果不一致则抛出异常
    assert User_Check(
        ipmi_default_user_info,
        redfish_default_user_info,
    ), "Ipmi Get Default User Info Not Equal To Redfish Get Default User Info"

    # 循环创建3到用户数量（ipmi_user_count）之间的随机用户,并检查IPMI和Redfish获取的用户信息是否一致,如果不一致则抛出异常
    for i in range(3, ipmi_user_count + 1):
        if i == 16:
            break
        dymical_username = "test" + str(i)
        dymical_password = "toutiao@" + str(i)
        dymical_roles = ["ADMINISTRATOR", "OPERATOR", "USER"]
        dymical_role = str(random.choices(dymical_roles))[2:-2]
        Create_User(
            user_id=i,
            user_name=dymical_username,
            user_password=dymical_password,
            user_role=dymical_role,
        )
        users = ssh_get_user_info(os_ip, os_username, os_password)
        assert users, "ssh connect failed or ssh execute cmd failed"
        ipmi_user = users[i - 1]
        logging.info("Ipmi Get User Info: {}".format(ipmi_user))

        # Redfish获取用户信息,如果获取失败,则抛出异常
        if machine_model == "G220-BA-B":
            real_id = dymical_username
        else:
            real_id = i
        redfish_user = Redfish_Get_User_Info(token, real_id)
        assert redfish_user, "Redfish Get User Info Fail"
        assert User_Check(
            ipmi_user, redfish_user
        ), "Ipmi Get User Info Not Equal To Redfish Get User Info"

        # 对新创建的用户执行一些命令检查,如果命令执行失败则抛出异常
        if bmc_ip != "192.168.1.10":
            result = execute_command(
                "-L {} mc info".format(dymical_role),
                bmc_ip,
                dymical_username,
                dymical_password,
                "outband",
            )
        else:
            result = execute_command(
                "-L {} mc info".format(dymical_role),
                dpu_os_ip,
                dymical_username,
                dymical_password,
                "outband",
            )
        assert result, "new created user execute command failed"

    # 修改默认用户权限,如果命令执行失败则抛出异常
    Command_Check("user priv 2 3 1")

    # 通过SSH获取BMC用户信息。如果连接失败,则抛出异常
    users = ssh_get_user_info(os_ip, os_username, os_password)
    assert users, "ssh connect failed or ssh execute cmd failed"
    ipmi_default_user_info = users[1]
    logging.info("Ipmi Default User Info:{}".format(ipmi_default_user_info))

    # Redfish获取用户信息,如果获取失败,则抛出异常
    if machine_model == "G220-BA-B":
        real_id = "toutiao"
    else:
        real_id = 2
    redfish_default_user_info = Redfish_Get_User_Info(token, real_id)
    assert redfish_default_user_info, "Redfish Get User Info Fail"

    # 检查IPMI获取的默认用户信息和Redfish获取的默认用户信息是否一致,如果不一致则抛出异常
    assert User_Check(
        ipmi_default_user_info, redfish_default_user_info
    ), "Ipmi Get Default User Info Not Equal To Redfish Get Default User Info"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"

    # BMC恢复出厂设置,如果命令执行失败则抛出异常
    output = ssh_execute_command(
        os_ip, os_username, os_password, "ipmitool raw 0x32 0x66"
    )
    assert output == "", "ssh connect failed or ssh execute cmd failed"

    # sleep 300s,等待BMC恢复出厂设置完成
    time.sleep(300)

    if bmc_ip == "192.168.1.10":
        pass
    else:
        # 检查网络模式是否恢复默认dhcp
        bmc_network_info = Get_BMC_Network(os_ip, os_username, os_password, lan_channel)
        assert (
            bmc_network_info["ip_source"] == "dhcp"
            and bmc_network_info["ip"] == "0.0.0.0"
            and (
                bmc_network_info["netmask"] == "0.0.0.0"
                or bmc_network_info["netmask"] == "255.255.255.255"
            )
            and bmc_network_info["gateway"] == "0.0.0.0"
        ), "After BMC Recover Factory Mode, Network Not Recover Default"

        # 设置BMC网络信息
        Set_BMC_Network(os_ip, os_username, os_password, bmc_ip, lan_channel)

        # ping BMC IP,超时时间90s，如果ping失败则抛出异常
        assert ping_ip(ip=bmc_ip, timeout=90, ping_test="pass"), "Ping BMC IP Failed"

    time.sleep(60)
    # 通过SSH获取BMC用户信息。如果连接失败,则抛出异常
    users = ssh_get_user_info(os_ip, os_username, os_password)
    assert users, "ssh connect failed or ssh execute cmd failed"
    ipmi_default_user_info = users[1]
    logging.info("Ipmi Default User Info:{}".format(ipmi_default_user_info))

    # 验证恢复出厂设置后,用户信息是否符合机型的要求,如果不符合则抛出异常
    assert validate_users(users, user_count), "validate users failed"

    # 使用BMC用户信息进行登录Redfish,如果登录失败,则抛出异常
    token, session_id = login_to_redfish_bmc()
    assert token and session_id, "Redfish Create Session Fail"

    # Redfish获取用户信息,如果获取失败,则抛出异常
    if machine_model == "G220-BA-B":
        real_id = "toutiao"
    else:
        real_id = 2
    redfish_default_user_info = Redfish_Get_User_Info(token, real_id)
    assert redfish_default_user_info, "Redfish Get User Info Fail"

    # 检查IPMI获取的默认用户信息和Redfish获取的默认用户信息是否一致,如果不一致则抛出异常
    assert User_Check(
        ipmi_default_user_info, redfish_default_user_info
    ), "Ipmi Get Default User Info Not Equal To Redfish Get Default User Info"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"
