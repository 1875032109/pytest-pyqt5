import logging
import subprocess
import re


def ssh_execute_command(ip, username, password, cmd):
    """
    通过ssh远程执行命令并返回命令的输出

    Args:
        client (paramiko.SSHClient): ssh客户端对象
        command (str): 要执行的命令

    Returns:
        output (str): 命令的输出

    """
    try:
        result = subprocess.run(
            [
                "sshpass",
                "-p",
                password,
                "ssh",
                "-o",
                "StrictHostKeyChecking=no",
                f"{username}@{ip}",
                cmd,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            if result.returncode == 1 and "grep" in cmd:
                logging.info("The grep command did not match any results")
            elif result.returncode == 1 and result.stdout != "":
                pass
            else:
                logging.error(
                    f"ssh execute cmd: {cmd} failed with exit code {result.returncode}"
                )
                return False
        output = result.stdout.strip()
        outerr = result.stderr.strip()
        logging.info(f"ssh execute cmd: {cmd} successfully")
        logging.info(f"output: {output}")
        logging.info(f"outerr: {outerr}")
        return output
    except subprocess.CalledProcessError as e:
        logging.error(f"ssh execute cmd error: {e}")
        return False


def ssh_get_machine_info(os_ip, os_username, os_password):
    """
    带内获取产品的制造商信息和项目名称

    Args:
        os_ip (str): OS地址
        os_username (str): OS用户名

    Returns:
        Union[str, bool]: 如果成功获取到产品制造商信息，则返回产品制造商信息，否则返回False

    """
    try:
        product_manufacturer = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool fru print 0 | grep -i 'Product Manufacturer' | awk -F : '{print $2}' | sed 's/ //g'",
        )
        product_name = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool fru print 0 | grep -i 'Product Name' | awk -F : '{print $2}' | sed 's/ //g'",
        )
        if product_manufacturer == False or product_name == False:
            return False, False
    except Exception as e:
        logging.error(e)
        return False, False
    return product_manufacturer, product_name


def ssh_get_user_count(os_ip, os_username, os_password):
    """
    带内获取指定BMC用户总数量

    Args:
        os_ip (str): OS地址
        os_username (str): OS用户名

    Returns:
        int: 用户总数量，如果获取失败则返回 False
    """
    try:
        user_count = int(
            ssh_execute_command(
                os_ip,
                os_username,
                os_password,
                "ipmitool user list 1 | awk 'END{print NR-1}'",
            )
        )
        if user_count == False:
            return False
    except Exception as e:
        logging.error(e)
        return False
    return user_count


def ssh_get_user_info(os_ip, os_username, os_password):
    """
    获取系统的用户信息

    Args:
        os_ip (str): OS地址
        os_username (str): OS用户名

    Returns:
        list: 包含用户信息的列表，每个元素是一个字典，包含以下键值对：
            - user_id (int): 用户ID
            - user_name (str): 用户名
            - user_role (str): 用户角色

    """
    try:
        user_info = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool user list 1",
        )
        if user_info == False:
            return False
    except Exception as e:
        logging.error(e)
        return False
    users = []
    response_lines = user_info.strip().splitlines()
    title_line = response_lines.pop(0)
    start_index_id = title_line.find("ID")
    start_index_name = title_line.find("Name")
    end_index_id = start_index_name
    end_index_name = title_line.find("Callin")
    for line in response_lines:
        user_id = int(line[start_index_id:end_index_id].strip())
        user_name = line[start_index_name:end_index_name].strip()
        user_role = " ".join(line[end_index_name:].strip().split()[3:])
        user = {"user_id": user_id, "user_name": user_name, "user_role": user_role}
        users.append(user)
    return users


def validate_users(users, user_count):
    """
    验证用户信息是否合法

    Args:
        users (list): 用户列表，每个元素为一个字典，包含"user_id", "user_name", "user_role"三个键
        user1_role (str, optional): 第一个用户的角色，默认为"NO ACCESS"
        user_count (int, optional): 用户数量，默认为15

    Returns:
        bool: 如果用户信息合法返回True，否则返回False

    """
    try:
        if len(users) != user_count:
            error_message = "非法用户个数: " + str(len(users)) + "\n"
            logging.info(error_message)
            return False
        for user in users:
            error_message = "ID:" + str(user["user_id"]) + ", "
            if user["user_id"] == 1:
                if user["user_name"] != "":
                    error_message += "用户名不为空: " + user["user_name"] + "\n"
                    logging.error(error_message)
                    return False
                # if user["user_role"].upper() != "ADMINISTRATOR":
                #     error_message += "非法用户权限: " + user["user_role"] + "\n"
                #     logging.error(error_message)
                #     return False
            elif user["user_id"] == 2:
                if user["user_name"] != "toutiao":
                    error_message += "非法用户名: " + user["user_name"] + "\n"
                    logging.error(error_message)
                    return False
                if user["user_role"].upper() != "ADMINISTRATOR":
                    error_message += "非法用户权限: " + user["user_role"] + "\n"
                    logging.error(error_message)
                    return False
            else:
                if user["user_name"] != "":
                    error_message += "用户名不为空: " + user["user_name"] + "\n"
                    logging.error(error_message)
                    return False
                if user["user_role"].upper() != "NO ACCESS":
                    error_message += "非法用户权限: " + user["user_role"] + "\n"
                    logging.error(error_message)
                    return False
    except Exception as e:
        logging.error(e)
        return False
    logging.info("validate users succeed")
    return True


def Set_BMC_Network(os_ip, os_username, os_password, bmc_ip, lan_channel):
    """
    设置BMC网络

    Args:
        os_ip (str): OS IP
        os_username (str): OS用户名
        bmc_ip (str): BMC IP
        lan_channel (str): LAN通道

    Returns:
        bool: 如果设置成功，则返回 True；否则返回 False。

    """
    try:
        set_ipsrc = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool lan set {} ipsrc static".format(lan_channel),
        )
        if set_ipsrc == False:
            logging.error("set ipsrc failed")
            return False
        set_ipaddr = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool lan set {} ipaddr {}".format(lan_channel, bmc_ip),
        )
        if set_ipaddr == False:
            logging.error("set ipaddr failed")
            return False
        set_netmask = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool lan set {} netmask 255.255.255.192".format(lan_channel),
        )
        if set_netmask == False:
            logging.error("set netmask failed")
            return False
        parts = bmc_ip.rsplit(".", 1)  # 在最后一个点之前拆分
        last_digit = parts[-1]
        if int(last_digit) <= 64:
            gateway_ip = parts[0] + ".1"
        elif 64 < int(last_digit) <= 128:
            gateway_ip = parts[0] + ".65"
        elif 128 < int(last_digit) <= 192:
            gateway_ip = parts[0] + ".129"
        elif 192 < int(last_digit) <= 255:
            gateway_ip = parts[0] + ".193"
        set_gateway_ipaddr = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool lan set {} defgw ipaddr {}".format(lan_channel, gateway_ip),
        )
        if set_gateway_ipaddr == False:
            logging.error("set gateway ipaddr failed")
            return False
    except Exception as e:
        logging.error(e)
        return False
    return True


def Get_BMC_Network(os_ip, os_username, os_password, lan_channel):
    """
    检查BMC网络模式

    Args:
        os_ip (str): OS IP地址
        os_username (str): OS 用户名
        lan_channel (int): BMC的LAN通道号

    Returns:
        dict: BMC网络信息字典，包含以下键值对：
            - ip_source (str): IP地址来源，可能的值为 "dhcp" 或 "static"
            - ip (str): BMC的IP地址
            - mac (str): BMC的MAC地址
            - netmask (str): 子网掩码地址
            - gateway (str): 默认网关地址
    """
    try:
        response = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool lan print {}".format(lan_channel),
        )
        if response == False:
            logging.error("get bmc network info failed")
            return False
        lines = [line.strip() for line in response.split("\n") if line.strip()]
        data_dict = {}
        for line in lines:
            key, value = line.split(":", 1)
            data_dict[key.strip()] = value.strip()
        bmc_network_info = {}
        if data_dict["IP Address Source"] == "DHCP Address":
            bmc_network_info["ip_source"] = "dhcp"
        else:
            bmc_network_info["ip_source"] = "static"
        bmc_network_info["ip"] = data_dict["IP Address"]
        bmc_network_info["mac"] = data_dict["MAC Address"]
        bmc_network_info["netmask"] = data_dict["Subnet Mask"]
        bmc_network_info["gateway"] = data_dict["Default Gateway IP"]
        logging.info("bmc network info: {}".format(bmc_network_info))
    except Exception as e:
        logging.error(e)
        return False
    return bmc_network_info


def Get_BMC_Network_IPV6(os_ip, os_username, os_password, lan_channel):
    """
    检查BMC网络模式

    Args:
        os_ip (str): OS IP地址
        os_username (str): OS 用户名
        lan_channel (int): BMC的LAN通道号

    Returns:
        dict: BMC网络信息字典，包含以下键值对：
            - ip_info (dict): BMC的IP地址
            - static_router (dict): BMC的路由地址
    """
    try:
        response = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool lan6 print {}".format(lan_channel),
        )
        if response == False:
            logging.error("get bmc network info failed")
            return False
        data_dict = BMC_IPV6_Treat(response)
        bmc_network_info = {}
        bmc_network_info["ip_info"] = data_dict["IPv6 Static Address 0"]
        bmc_network_info["static_router"] = data_dict["IPv6 Static Router 1"]
        logging.info("bmc network info: {}".format(bmc_network_info))
    except Exception as e:
        logging.error(e)
        return False
    return bmc_network_info


def BMC_IPV6_Treat(data):
    result = {}
    lines = data.split("\n")
    current_key = ""
    for line in lines:
        line = line.strip()
        if line.endswith(":") and not line.endswith("::"):
            current_key = line[:-1]
            result[current_key] = {}
        elif ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            result[current_key][key] = value
    return result


def Get_BMC_FW_Version(os_ip, os_username, os_password):
    """
    获取BMC固件版本

    Args:
        os_ip (str): OS IP地址
        os_username (str): OS用户名

    Returns:
        str: BMC固件版本号，格式为"主版本号.辅助版本号"

    """
    try:
        response = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "ipmitool mc info",
        )
        if response == False:
            logging.error("get bmc version failed")
            return False
        lines = [line.strip() for line in response.split("\n") if line.strip()]
        data_dict = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                data_dict[key.strip()] = value.strip()
            else:
                data_dict[key.strip()] += f"\n{line.strip()}"
        indented_values = re.findall(r"\s+(.+)", data_dict["Aux Firmware Rev Info"])
        data_dict["Aux Firmware Rev Info"] = indented_values

        main_version = data_dict["Firmware Revision"].strip()
        secondary_version = data_dict["Aux Firmware Rev Info"][0][2:].strip()
        bmc_version = ".".join([main_version, secondary_version])
        logging.info("bmc version: {}".format(bmc_version))
    except Exception as e:
        logging.error(e)
        return False
    return bmc_version


def Get_BIOS_FW_Version(os_ip, os_username, os_password):
    """
    获取BIOS固件版本

    Args:
        os_ip (str): OS IP地址
        os_username (str): OS用户名

    Returns:
        str: BIOS固件版本号

    """
    try:
        bios_version = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "dmidecode -t 0 | grep -i 'version:'|awk -F : '{print $2}'|sed 's/ //g'",
        )
        if bios_version == False:
            logging.error("get bios version failed")
            return False
    except Exception as e:
        logging.error(e)
        return False
    return bios_version


def Clear_Message_In_Os(os_ip, os_username, os_password):
    """
    清除dmesg/message消息

    Args:
        os_ip (str): 操作系统IP地址
        os_username (str): 操作系统用户名

    Returns:
        bool: 清除操作是否成功

    """
    try:
        response = ssh_execute_command(os_ip, os_username, os_password, "dmesg -C")
        if response == False:
            logging.error("clear dmesg failed")
            return False
        response = ssh_execute_command(
            os_ip, os_username, os_password, "truncate -s 0 /var/log/messages"
        )
        if response == False:
            logging.error("clear messages failed")
            return False
    except Exception as e:
        logging.error(e)
        return False
    return True


def Get_Message_In_OS(os_ip, os_username, os_password):
    """
    获取系统中dmesg/message的错误信息

    Args:
        os_ip (str): 操作系统的IP地址
        os_username (str): 操作系统的用户名

    Returns:
        bool: 获取错误信息是否成功，成功返回True，失败返回False
    """
    try:
        response = ssh_execute_command(
            os_ip, os_username, os_password, "dmesg | grep -i -E 'error|fail'"
        )
        if response == False:
            logging.error("get dmesg failed")
            return False
        response = ssh_execute_command(
            os_ip,
            os_username,
            os_password,
            "cat /var/log/messages | grep -i -E 'error|fail'",
        )
        if response == False:
            logging.error("get messages failed")
            return False
    except Exception as e:
        logging.error(e)
        return False
    return True


def Get_System_Info(os_ip, os_username, os_password):
    """
    获取服务器信息

    Args:
        os_ip (str): 服务器IP地址
        os_username (str): 服务器用户名

    Returns:
        Tuple[fru[str], user_info[str], sdr_info[str], sensor_info[str]]: 包含服务器信息的元组，如果获取失败则返回False

    """
    try:
        fru_info = ssh_execute_command(
            os_ip, os_username, os_password, "ipmitool fru print"
        )
        if fru_info == False:
            logging.error("get fru info failed")
            return False
        user_info = ssh_execute_command(
            os_ip, os_username, os_password, "ipmitool user list 1"
        )
        if user_info == False:
            logging.error("get user info failed")
            return False
        sdr_info = ssh_execute_command(
            os_ip, os_username, os_password, "ipmitool sdr elist"
        )
        if sdr_info == False:
            logging.error("get sdr info failed")
            return False
        sensor_info = ssh_execute_command(
            os_ip, os_username, os_password, "ipmitool sensor list"
        )
        if sensor_info == False:
            logging.error("get sensor info failed")
            return False
    except Exception as e:
        logging.error(e)
        return False, False, False, False
    fru_info = fru_info.strip().split("\n")
    user_info = user_info.strip().split("\n")
    sdr_info = sdr_info.strip().split("\n")
    sensor_info = sensor_info.strip().split("\n")
    return fru_info, user_info, sdr_info, sensor_info
