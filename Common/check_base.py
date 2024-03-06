"""
基础功能检查
"""

import logging
import sys
import os
import re
import time
import configparser

path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(path)

from Common.remote_ssh import *
from Common.execute_command import *
from Common.get_config import *


def Sel_Clear():
    """
    清除sel并检查清除是否成功

    Args:
        无

    Returns:
        无

    """
    # 断言通过sel clear命令清除sel，并通过sel list命令检查sel是否清除成功
    Command_Check("sel clear")
    sel_list = Command_Check("sel list")
    assert sel_clear_log in sel_list, "Check Sel Clear Fail"
    logging.info("Check Sel Clear Success")


def Sel_Check(*sel):
    """
    检查BMC的SEL是否包含指定的关键字。

    Args:
        sel: 包含预期关键字列表的元组。

    Returns:
        None

    Raises:
        AssertionError: 如果命令执行失败或关键字检查失败。
    """
    # 断言执行命令“sel list”获取sel的详细信息，并检查命令执行结果
    outband = Command_Check("sel list")
    # 断言sel的详细信息中包含所有预期的关键字
    uncover_sel_info = []
    for sel_info in list(*sel):
        if sel_info not in outband:
            uncover_sel_info.append(sel_info)
    if uncover_sel_info != []:
        logging.error(f"uncover_sel_info: {uncover_sel_info}")
        assert uncover_sel_info == [], "Check Sel Info Failed"
    else:
        logging.info("Check Sel Info Success")

    # 断言sel的详细信息中不包含失败的关键字
    error_sel_info = []
    for error_sel in sel_fail_keywords:
        if error_sel in outband:
            error_sel_info.append(error_sel)
    if error_sel_info != []:
        logging.error(f"error_sel_info: {error_sel_info}")
        assert error_sel_info == [], "Sel Occur Error Info"
    else:
        logging.info("Sel UnOccur Error Info")


def Ping_Check(check):
    """
    检查Ping可达/不可达以及Power状态

    Args:
        check: on/off/both, 只能是 on/off/both 中的一个
        on: 通过ping命令检查目标IP可达, 并检查Power状态（power on）
        off: 通过ping命令检查目标IP不可达，并检查Power状态（power off/soft）
        both: 通过ping命令先检查目标IP不可达，再检查目标IP可达，并检查Power状态（power cycle/reset）

    Returns:
        None

    Raises:
        AssertionError: 如果命令执行失败或关键字检查失败。
    """
    if check == "off":
        # 断言通过ping命令检查目标IP不可达，并设置超时时间
        assert ping_ip(
            os_ip, timeout=power_off_timeout, ping_test="fail"
        ), "Check Ping 不可达 Fail"

        # 断言通过chasssis power status命令检查机器是否已off
        power_status = Command_Check("chassis power status")
        check_off_count = 0
        while check_off_count <= 3:
            if power_off_status not in power_status:
                check_off_count += 1
                time.sleep(5)
                power_status = Command_Check("chassis power status")
            else:
                break
        assert power_off_status in power_status, "Check Power Off Status Fail"
    elif check == "on":
        # 断言通过ping命令检查目标IP可达，并设置超时时间
        assert ping_ip(
            os_ip, timeout=power_on_timeout, ping_test="pass"
        ), "Check Ping 可达 Fail"

        # 断言通过chasssis power status命令检查机器是否已on
        power_status = Command_Check("chassis power status")
        check_on_count = 0
        while check_on_count <= 3:
            if power_on_status not in power_status:
                check_on_count += 1
                time.sleep(5)
                power_status = Command_Check("chassis power status")
            else:
                break
        assert power_on_status in power_status, "Check Power On Status Fail"
    elif check == "cycle":
        # 断言通过ping命令检查目标IP不可达，并设置超时时间
        assert ping_ip(
            os_ip, timeout=power_off_timeout, ping_test="fail"
        ), "Check Ping 不可达 Fail"

        # # 断言通过chasssis power status命令检查机器是否已off
        # power_status = Command_Check("chassis power status")
        # check_off_count = 0
        # while check_off_count <= 3:
        #     if power_off_status not in power_status:
        #         check_off_count += 1
        #         time.sleep(5)
        #         power_status = Command_Check("chassis power status")
        #     else:
        #         break
        # assert power_off_status in power_status, "Check Power Off Status Fail"

        # 断言通过ping命令检查目标IP可达，并设置超时时间
        assert ping_ip(
            os_ip, timeout=power_on_timeout, ping_test="pass"
        ), "Check Ping 可达 Fail"

        # 断言通过chasssis power status命令检查机器是否已on
        power_status = Command_Check("chassis power status")
        check_on_count = 0
        while check_on_count <= 3:
            if power_on_status not in power_status:
                check_on_count += 1
                time.sleep(5)
                power_status = Command_Check("chassis power status")
            else:
                break
        assert power_on_status in power_status, "Check Power On Status Fail"
    elif check == "reset":
        # 断言通过ping命令检查目标IP不可达，并设置超时时间
        assert ping_ip(
            os_ip, timeout=power_off_timeout, ping_test="fail"
        ), "Check Ping 不可达 Fail"

        # 断言通过chasssis power status命令检查机器是否已on
        power_status = Command_Check("chassis power status")
        check_on_count = 0
        while check_on_count <= 3:
            if power_on_status not in power_status:
                check_on_count += 1
                time.sleep(5)
                power_status = Command_Check("chassis power status")
            else:
                break
        assert power_on_status in power_status, "Check Power On Status Fail"

        # 断言通过ping命令检查目标IP可达，并设置超时时间
        assert ping_ip(
            os_ip, timeout=power_on_timeout, ping_test="pass"
        ), "Check Ping 可达 Fail"

        # 断言通过chasssis power status命令检查机器是否已on
        power_status = Command_Check("chassis power status")
        check_on_count = 0
        while check_on_count <= 3:
            if power_on_status not in power_status:
                check_on_count += 1
                time.sleep(5)
                power_status = Command_Check("chassis power status")
            else:
                break
        assert power_on_status in power_status, "Check Power On Status Fail"
    else:
        raise AssertionError("check must be on/off/both")


def Command_Check(command):
    """
    检查BMC是否能成功执行指令

    Args:
        command (str): 要执行的指令

    Returns:
        Any: 执行结果

    Raises:
        AssertionError: 如果执行指令失败，则会抛出 AssertionError 异常
    """
    if bmc_ip != "192.168.1.10":
        result = execute_command(command, bmc_ip, bmc_username, bmc_password, "outband")
    else:
        result = execute_command(
            command, dpu_os_ip, bmc_username, bmc_password, "outband"
        )
    return result


def User_Check(ipmi_user, redfish_user):
    """
    检查IPMI用户信息和Redfish用户信息是否相同

    Args:
        ipmi_user (str): IPMI用户信息
        redfish_user (str): Redfish用户信息

    Returns:
        bool: True表示IPMI用户名和Redfish用户名相同，False表示不相同
    """
    if machine_model == "G220-BA-B":
        if (
            ipmi_user["user_name"]
            == redfish_user["user_id"]
            == redfish_user["user_name"]
            and ipmi_user["user_role"] == redfish_user["user_role"]
        ):
            logging.info("Ipmi Get User Info And Redfish Get User Info Check Succeed")
            return True
        else:
            logging.info("Ipmi Get User Info And Redfish Get User Info Check Failed")
            logging.error(f"ipmi user info: {ipmi_user}")
            logging.error(f"redfish user info: {redfish_user}")
            return False
    else:
        if ipmi_user == redfish_user:
            logging.info("Ipmi Get User Info And Redfish Get User Info Check Succeed")
            return True
        else:
            logging.info("Ipmi Get User Info And Redfish Get User Info Check Failed")
            logging.error(f"ipmi user info: {ipmi_user}")
            logging.error(f"redfish user info: {redfish_user}")
            return False


def Create_User(user_id, user_name, user_password, user_role):
    """
    创建用户

    Args:
        user_id (str): 用户ID
        user_name (str): 用户名称
        user_password (str): 用户密码
        user_role (str): 用户权限

    Returns:
        bool: 创建成功返回True，失败返回False
    """
    try:
        if user_role == "ADMINISTRATOR":
            user_role = 4
        elif user_role == "OPERATOR":
            user_role = 3
        elif user_role == "USER":
            user_role = 2
        else:
            user_role = 1
        Command_Check(f"user set name {user_id} {user_name}")
        Command_Check(f"user set password {user_id} {user_password}")
        Command_Check(f"user priv {user_id} {user_role}")
        Command_Check(f"user enable {user_id}")
        Command_Check(f"channel setaccess 1 {user_id} ipmi=on")
    except AssertionError:
        logging.error("Create User Failed")
        return False
    logging.info(
        """Create User Succeed: 
        user_id: {}, 
        user_name: {},
        user_password: {}, 
        user_role: {}""".format(
            user_id, user_name, user_password, user_role
        )
    )
    return True


def Sdr_Info_Treat(sdr_info):
    """
    将Sdr信息处理成二维列表，并返回。

    Args:
        sdr_info (str): SDR信息字符串，每行格式为"数据1|数据2|...|数据n"。

    Returns:
        List[List[str]]: 处理后的二维列表，每个子列表对应一行SDR信息，列表元素为原始数据的字符串类型。

    """
    try:
        sdr_info_treat = []
        for m in range(len(sdr_info)):
            temp = sdr_info[m].split("|")
            temp.pop()
            for n in range(len(temp)):
                temp[n] = temp[n].strip()
            sdr_info_treat.append(temp)
    except Exception as e:
        logging.error(e)
        return False
    return sdr_info_treat


def Sensor_Info_Treat(sensor_info):
    """
    将Sensor的信息列表按照规定格式进行转化。

    Args:
        sensor_info (str): 传感器的信息，格式为每行一个传感器，每个传感器信息用竖线(|)分隔。

    Returns:
        List[List[str]]: 转化后的传感器信息列表，每个传感器信息用列表表示，列表中的每个元素为字符串类型。

    """
    try:
        sensor_info_treat = []
        for m in range(len(sensor_info)):
            temp = sensor_info[m].split("|")
            temp.pop(1)
            for n in range(len(temp)):
                temp[n] = temp[n].strip()
            sensor_info_treat.append(temp)
    except Exception as e:
        logging.error(e)
        return False
    return sensor_info_treat


def list_diff(list1, list2, check_key):
    """
    对比两个列表是否完全相同

    Args:
        list1 (list): 第一个列表
        list2 (list): 第二个列表

    Returns:
        bool: 若两个列表完全相同则返回True，否则返回False

    """
    try:
        diff = [(x, y) for x, y in zip(list1, list2) if x != y]
        if diff == []:
            logging.info("Diff %s info PASS" % check_key)
            return True
        else:
            logging.error("Diff %s info Failed" % check_key)
            for item in diff:
                logging.error(f"Different items: {item[0]} vs {item[1]}")
            return False
    except Exception as e:
        logging.error(e)
        return False


def dict_diff(dict1, dict2, check_key):
    """
    对比两个字典是否完全相同

    Args:
        dict1 (dict): 第一个字典
        dict2 (dict): 第二个字典
        key (str): 比较的键

    Returns:
        bool: 若两个字典完全相同则返回True，否则返回False

    """
    try:
        diff_items = {
            k: (dict1[k], dict2[k])
            for k in dict1.keys() & dict2.keys()
            if dict1[k] != dict2[k]
        }
        diff_items.update({k: (dict1[k], None) for k in dict1.keys() - dict2.keys()})
        diff_items.update({k: (None, dict2[k]) for k in dict2.keys() - dict1.keys()})
        if diff_items == {}:
            logging.info("Diff %s info PASS" % check_key)
            return True
        else:
            logging.error("Diff %s info Failed" % check_key)
            for k, v in diff_items.items():
                logging.error(f"Different items: 键: {k}, 值: {v}")
            return False
    except Exception as e:
        logging.error(e)
        return False


def fru_change(info):
    fru_data = re.findall(
        r"(FRU Device Description) : (.+?) \(ID (\d+)\)|(\w+\s+\w+)\s+:\s(.+)", info
    )
    # 生成返回的列表
    output = []
    extra_info = ""
    current_id = None
    current_description = None
    for match in fru_data:
        if match[0] == "FRU Device Description":
            if current_id is not None:
                output.append(
                    {
                        "id": current_id,
                        "description": current_description,
                        "extra": extra_info.strip(),
                    }
                )
            current_id = int(match[2])
            current_description = match[1].strip()
            extra_info = ""
        else:
            extra_info += f"{match[3]}: {match[4].strip()}\n"

    # 添加最后一个ID的附加信息
    if current_id is not None:
        output.append(
            {
                "id": current_id,
                "description": current_description,
                "extra": extra_info.strip(),
            }
        )
    return output


def get_update_bmc_inband_script(retain=True, bare_metal=False):
    if bare_metal:
        if retain:
            G225_B5_2_Foxconn = (
                "bash FwUpdate_Foxconn.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B6_2_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B9_2_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
        else:
            G225_B5_2_Foxconn = (
                "bash FwUpdate_Foxconn.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B6_2_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B9_2_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
    else:
        if retain:
            G220_BA_B_Nettrix = "python3 bytebmctool.py -v update -f %s -c keep"  # c: clear为不保留配置，keep为保留配置
            S820_A3_Inspur = (
                "bash FwUpdate_Inspur.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            S820_A6_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            S820_A9_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B5_Foxconn = (
                "bash FwUpdate_Foxconn.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B6_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B9_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            NF5468M7_Inspur = ""
            G228_AD_ZTE = (
                "bash Updater_ZTE.sh -O 0 -F %s"  # O： 0为保留配置，1为不保留配置
            )
        else:
            G220_BA_B_Nettrix = "python3 bytebmctool.py -v update -f %s -c clear"  # c: clear为不保留配置，keep为保留配置
            S820_A3_Inspur = (
                "bash FwUpdate_Inspur.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            S820_A6_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            S820_A9_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B5_Foxconn = (
                "bash FwUpdate_Foxconn.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B6_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B9_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            NF5468M7_Inspur = ""
            G228_AD_ZTE = (
                "bash Updater_ZTE.sh -O 1 -F %s"  # O： 0为保留配置，1为不保留配置
            )
    if "G225-B5-2" == machine_model:
        script = G225_B5_2_Foxconn
    elif "G225-B6-2" == machine_model:
        script = G225_B6_2_Inventec
    elif "G225-B9-2" == machine_model:
        script = G225_B9_2_Lenovo
    elif "S820-A3" == machine_model:
        script = S820_A3_Inspur
    elif "S820-A6" == machine_model:
        script = S820_A6_Inventec
    elif "S820-A9" == machine_model:
        script = S820_A9_Lenovo
    elif "G225-B5" == machine_model:
        script = G225_B5_Foxconn
    elif "G225-B6" == machine_model:
        script = G225_B6_Inventec
    elif "G225-B9" == machine_model:
        script = G225_B9_Lenovo
    elif "NF5468M7" == machine_model:
        script = NF5468M7_Inspur
    elif "G228-AD" == machine_model:
        script = G228_AD_ZTE
    elif "G220-BA-B" == machine_model:
        script = G220_BA_B_Nettrix
    script_downgrade = script % downgrade_bios_file_name
    script_upgrade = script % upgrade_bios_file_name
    return script_downgrade, script_upgrade


def get_update_bmc_outband_script(retain=True, bare_metal=False):
    if bare_metal:
        if retain:
            R5500G5_2_H3C = "./curl.sh -I {} -O {} -S 1 -U {} -P {} -T HDM -M main -F %s -R 0 -K 0 -V 1".format(  # K: 0为保留配置，1为不保留配置   # S：0为http，1为https
                dpu_os_ip, port, bmc_username, bmc_password
            )
            G225_B5_2_Foxconn = "bash FwUpdate_Foxconn.sh -H {} -U {} -P {} -p {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
            G225_B6_2_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -p {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
            G225_B9_2_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -p {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
        else:
            R5500G5_2_H3C = "./curl.sh -I {} -O {} -S 1 -U {} -P {} -T HDM -M main -F %s -R 0 -K 1 -V 1".format(  # K: 0为保留配置，1为不保留配置   # S：0为http，1为https
                dpu_os_ip, port, bmc_username, bmc_password
            )
            G225_B5_2_Foxconn = "bash FwUpdate_Foxconn.sh -H {} -U {} -P {} -p {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
            G225_B6_2_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -p {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
            G225_B9_2_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -p {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
    else:
        if retain:
            G220_BA_B_Nettrix = "python3 bytebmctool.py -v -u {} -p {} -b {} update -f %s -c keep".format(  # c: clear为不保留配置，keep为保留配置
                bmc_username, bmc_password, bmc_ip
            )
            R5300G6_H3C = "./curl.sh -I {} -U {} -P {} -F %s -R 0 -K 0".format(  # K: 0为保留配置，1为不保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A3_Inspur = "bash FwUpdate_Inspur.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A6_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A9_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B5_Foxconn = "bash FwUpdate_Foxconn.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B6_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B9_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            NF5468M7_Inspur = "./imscli -H {} -U {} -P {} updatebmc -O 1 -F %s".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G228_AD_ZTE = "bash Updater_ZTE.sh -H {} -U {} -P {} -O 0 -F %s".format(  # O： 0为保留配置，1为不保留配置
                bmc_ip, bmc_username, bmc_password
            )
        else:
            G220_BA_B_Nettrix = "python3 bytebmctool.py -v -u {} -p {} -b {} update -f %s -c clear".format(  # c: clear为不保留配置，keep为保留配置
                bmc_username, bmc_password, bmc_ip
            )
            R5300G6_H3C = (
                "./curl.sh -I {} -U {} -P {} -F %s -R 0 -K 1"  # K: 0为保留配置，1为不保留配置
            ).format(bmc_ip, bmc_username, bmc_password)
            S820_A3_Inspur = "bash FwUpdate_Inspur.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A6_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A9_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B5_Foxconn = "bash FwUpdate_Foxconn.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B6_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B9_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            NF5468M7_Inspur = "./imscli -H {} -U {} -P {} updatebmc -O 0 -F %s".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G228_AD_ZTE = "bash Updater_ZTE.sh -H {} -U {} -P {} -O 1 -F %s".format(  # O： 0为保留配置，1为不保留配置
                bmc_ip, bmc_username, bmc_password
            )
    if "G225-B5-2" == machine_model:
        script = G225_B5_2_Foxconn
    elif "G225-B6-2" == machine_model:
        script = G225_B6_2_Inventec
    elif "G225-B9-2" == machine_model:
        script = G225_B9_2_Lenovo
    elif "S820-A3" == machine_model:
        script = S820_A3_Inspur
    elif "S820-A6" == machine_model:
        script = S820_A6_Inventec
    elif "S820-A9" == machine_model:
        script = S820_A9_Lenovo
    elif "G225-B5" == machine_model:
        script = G225_B5_Foxconn
    elif "G225-B6" == machine_model:
        script = G225_B6_Inventec
    elif "G225-B9" == machine_model:
        script = G225_B9_Lenovo
    elif "NF5468M7" == machine_model:
        script = NF5468M7_Inspur
    elif "G228-AD" == machine_model:
        script = G228_AD_ZTE
    elif "G220-BA-B" == machine_model:
        script = G220_BA_B_Nettrix
    elif "R5500G5-2" == machine_model:
        script = R5500G5_2_H3C
    elif "R5300G6" == machine_model:
        script = R5300G6_H3C
    script_downgrade = script % downgrade_bios_file_name
    script_upgrade = script % upgrade_bios_file_name
    return script_downgrade, script_upgrade


def get_update_bios_inband_script(retain=True, bare_metal=False):
    if bare_metal:
        if retain:
            G225_B5_2_Foxconn = (
                "bash FwUpdate_Foxconn.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B6_2_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B9_2_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
        else:
            G225_B5_2_Foxconn = (
                "bash FwUpdate_Foxconn.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B6_2_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B9_2_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
    else:
        if retain:
            G220_BA_B_Nettrix = "python3 bytebmctool.py -v update -f %s"
            S820_A3_Inspur = (
                "bash FwUpdate_Inspur.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            S820_A6_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            S820_A9_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B5_Foxconn = (
                "bash FwUpdate_Foxconn.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B6_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            G225_B9_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 1"  # O: 0为不保留配置，1为保留配置
            )
            NF5468M7_Inspur = (
                "./imscli updatebios -O 1 -F %s"  # O: 0为不保留配置，1为保留配置
            )
            G228_AD_ZTE = (
                "bash Updater_ZTE.sh -O 0 -F %s"  # O： 0为保留配置，1为不保留配置
            )
        else:
            G220_BA_B_Nettrix = "python3 bytebmctool.py -v update -f %s -s clear"
            S820_A3_Inspur = (
                "bash FwUpdate_Inspur.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            S820_A6_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            S820_A9_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B5_Foxconn = (
                "bash FwUpdate_Foxconn.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B6_Inventec = (
                "bash FwUpdate_Inventec.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            G225_B9_Lenovo = (
                "bash FwUpdate_Lenovo.sh -F %s -O 0"  # O: 0为不保留配置，1为保留配置
            )
            NF5468M7_Inspur = (
                "./imscli updatebios -O 0 -F %s"  # O: 0为不保留配置，1为保留配置
            )
            G228_AD_ZTE = (
                "bash Updater_ZTE.sh -O 1 -F %s"  # O： 0为保留配置，1为不保留配置
            )
    if "G225-B5-2" == machine_model:
        script = G225_B5_2_Foxconn
    elif "G225-B6-2" == machine_model:
        script = G225_B6_2_Inventec
    elif "G225-B9-2" == machine_model:
        script = G225_B9_2_Lenovo
    elif "S820-A3" == machine_model:
        script = S820_A3_Inspur
    elif "S820-A6" == machine_model:
        script = S820_A6_Inventec
    elif "S820-A9" == machine_model:
        script = S820_A9_Lenovo
    elif "G225-B5" == machine_model:
        script = G225_B5_Foxconn
    elif "G225-B6" == machine_model:
        script = G225_B6_Inventec
    elif "G225-B9" == machine_model:
        script = G225_B9_Lenovo
    elif "NF5468M7" == machine_model:
        script = NF5468M7_Inspur
    elif "G228-AD" == machine_model:
        script = G228_AD_ZTE
    elif "G220-BA-B" == machine_model:
        script = G220_BA_B_Nettrix
    script_downgrade = script % downgrade_bios_file_name
    script_upgrade = script % upgrade_bios_file_name
    return script_downgrade, script_upgrade


def get_update_bios_outband_script(retain=True, bare_metal=False):
    if bare_metal:
        if retain:
            R5500G5_2_H3C = "./curl.sh -I {} -O {} -S 1 -U {} -P {} -F %s -T BIOS -R 2 -K 0 -V 1".format(  # K: 0为保留配置，2为不保留配置
                dpu_os_ip, port, bmc_username, bmc_password
            )
            G225_B5_2_Foxconn = "bash FwUpdate_Foxconn.sh -H {} -U {} -P {} -p {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
            G225_B6_2_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -p {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
            G225_B9_2_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -p {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
        else:
            R5500G5_2_H3C = "./curl.sh -I {} -O {} -S 1 -U {} -P {} -F %s -T BIOS -R 2 -K 2 -V 1".format(  # K: 0为保留配置，2为不保留配置
                dpu_os_ip, port, bmc_username, bmc_password
            )
            G225_B5_2_Foxconn = "bash FwUpdate_Foxconn.sh -H {} -U {} -P {} -p {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
            G225_B6_2_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -p {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
            G225_B9_2_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -p {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                dpu_os_ip, bmc_username, bmc_password, port
            )
    else:
        if retain:
            G220_BA_B_Nettrix = (
                "python3 bytebmctool.py -u {} -p {} -b {} update -f %s".format(
                    bmc_username, bmc_password, bmc_ip
                )
            )
            R5300G6_H3C = "./curl.sh -I {} -U {} -P {} -F %s -R 1 -K 0".format(  # K: 0为保留配置，1为不保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A3_Inspur = "bash FwUpdate_Inspur.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A6_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A9_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B5_Foxconn = "bash FwUpdate_Foxconn.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B6_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B9_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -F %s -O 1".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            NF5468M7_Inspur = "./imscli -H {} -U {} -P {} updatebios -O 1 -F %s".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G228_AD_ZTE = "bash Updater_ZTE.sh -H {} -U {} -P {} -O 0 -F %s".format(  # O： 0为保留配置，1为不保留配置
                bmc_ip, bmc_username, bmc_password
            )
        else:
            G220_BA_B_Nettrix = (
                "python3 bytebmctool.py -u {} -p {} -b {} update -f %s -s clear".format(
                    bmc_username, bmc_password, bmc_ip
                )
            )
            R5300G6_H3C = "./curl.sh -I {} -U {} -P {} -F %s -R 1 -K 1".format(  # K: 0为保留配置，1为不保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A3_Inspur = "bash FwUpdate_Inspur.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A6_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            S820_A9_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B5_Foxconn = "bash FwUpdate_Foxconn.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B6_Inventec = "bash FwUpdate_Inventec.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G225_B9_Lenovo = "bash FwUpdate_Lenovo.sh -H {} -U {} -P {} -F %s -O 0".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            NF5468M7_Inspur = "./imscli -H {} -U {} -P {} updatebios -O 0 -F %s".format(  # O: 0为不保留配置，1为保留配置
                bmc_ip, bmc_username, bmc_password
            )
            G228_AD_ZTE = "bash Updater_ZTE.sh -H {} -U {} -P {} -O 1 -F %s".format(  # O： 0为保留配置，1为不保留配置
                bmc_ip, bmc_username, bmc_password
            )
    if "G225-B5-2" == machine_model:
        script = G225_B5_2_Foxconn
    elif "G225-B6-2" == machine_model:
        script = G225_B6_2_Inventec
    elif "G225-B9-2" == machine_model:
        script = G225_B9_2_Lenovo
    elif "S820-A3" == machine_model:
        script = S820_A3_Inspur
    elif "S820-A6" == machine_model:
        script = S820_A6_Inventec
    elif "S820-A9" == machine_model:
        script = S820_A9_Lenovo
    elif "G225-B5" == machine_model:
        script = G225_B5_Foxconn
    elif "G225-B6" == machine_model:
        script = G225_B6_Inventec
    elif "G225-B9" == machine_model:
        script = G225_B9_Lenovo
    elif "NF5468M7" == machine_model:
        script = NF5468M7_Inspur
    elif "G228-AD" == machine_model:
        script = G228_AD_ZTE
    elif "G220-BA-B" == machine_model:
        script = G220_BA_B_Nettrix
    elif "R5300G6" == machine_model:
        script = R5300G6_H3C
    elif "R5500G5-2" == machine_model:
        script = R5500G5_2_H3C
    script_downgrade = script % downgrade_bios_file_name
    script_upgrade = script % upgrade_bios_file_name
    return script_downgrade, script_upgrade
