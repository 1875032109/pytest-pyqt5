import datetime
import time
import logging
import requests
import re
import json
import urllib3
from Common.get_config import *

SLEEP_TIME = 3
CHECK_SLEEP_TIME = 60


def login_to_redfish_bmc():
    """
    Redfish登录BMC并返回token和session_id
    Args:
    Returns:
        Tuple[str, str]: token和session_id的元组

    """
    try:
        logging.info("---------- Redfish Create Session ----------")
        if machine_model == "G220-BA-B":
            data = '{"UserName": "%s", "Password": "%s"}' % (
                bmc_username,
                bmc_password,
            )
        else:
            data = '{"UserName": "%s", "Password": "%s", "SessionTimeOut": 3600}' % (
                bmc_username,
                bmc_password,
            )
        login_url = "https://{}/redfish/v1/SessionService/Sessions".format(
            redfish_bmc_ip
        )
        headers = {"Content-Type": "application/json"}
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.info(f"POST request sent to {login_url}")
        logging.info(f"Body: {data}")
        response = requests.post(login_url, data=data, headers=headers, verify=False)
        logging.info(f"Status:{response.status_code}")
        logging.info(f"Body:\n{response.text}")
        if (
            response.status_code != 200
            and response.status_code != 201
            and response.status_code != 202
            and response.status_code != 204
        ):
            logging.error(
                "status code is not 200 or 201 or 202 or 204, Redfish Create Session Failed"
            )
            return False, False
        logging.info("---------- Redfish Create Session Succeed ----------")
        ### 裸金属
        if bmc_ip == "192.168.1.10":
            if "R5500G5-2" == machine_model:
                token = response.headers["X-Auth-Token"]
                session_id = json.loads(response.text)["Id"]
            else:
                token = json.loads(response.text)["Oem"][category]["X-Auth-Token"]
                session_id = json.loads(response.text)["Id"]
        ### 非裸金属
        elif "R5300G6" == machine_model or "R5500G6" == machine_model:
            token = re.findall('"X-Auth-Token": ".*?"', response.text)
            token = token[0].split(":")[1]
            token = token.strip().strip('"')
            session_id = re.findall('"@odata.id": ".*?"', response.text)
            session_id = session_id[0].split(":")[1].split("/").pop()
            session_id = session_id.strip().strip('"')
        else:
            token = json.loads(response.text)["Oem"][category]["X-Auth-Token"]
            session_id = json.loads(response.text)["Id"]
        logging.info("token: {}".format(token))
        logging.info("session_id: {}".format(session_id))
    except Exception as e:
        logging.error(e)
        return False, False
    return token, session_id


def logout_from_redfish_bmc(token, session_id):
    """
    删除Redfish中的会话
    Args:
    Returns:
        bool: 删除会话是否成功
    """
    try:
        logging.info("---------- Redfish Delete Session ----------")
        del_url = "https://{}/redfish/v1/SessionService/Sessions/{}".format(
            redfish_bmc_ip, session_id
        )
        headers = {"Content-Type": "application/json", "X-Auth-Token": f"{token}"}
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.info(f"DELETE request sent to {del_url}")
        logging.info(f"Headers: {headers}")
        response = requests.delete(del_url, headers=headers, verify=False)
        logging.info(f"Status:{response.status_code}")
        logging.info(f"Body:\n{response.text}")
        if (
            response.status_code != 200
            and response.status_code != 201
            and response.status_code != 202
            and response.status_code != 204
        ):
            logging.error(
                "status code is not 200 or 201 or 202 or 204, Redfish Delete Session Failed"
            )
            return False
        logging.info("---------- Redfish Delete Session Succeed ----------")
    except Exception as e:
        logging.error(e)
        return False
    return True


def Redfish_Power_Control(reset_type, token):
    """
    通过Redfish API控制服务器重启
    Args:
        reset_type (str): 重启类型, 可选值为GracefulShutdown, On, ForceOff, ForcePowerCycle, ForceRestart
        token (str): 认证token
    Returns:
        bool: 操作是否成功，成功返回True，失败返回False
    """
    try:
        logging.info("---------- Redfish Power Control:%s ----------" % reset_type)
        headers = {"Content-Type": "application/json", "X-Auth-Token": f"{token}"}
        reset_url = (
            "https://{}/redfish/v1/Systems/{}/Actions/ComputerSystem.Reset".format(
                redfish_bmc_ip, system_id
            )
        )
        data = '{"ResetType" : "%s"}' % reset_type
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.info(f"POST request sent to {reset_url}")
        logging.info(f"Headers: {headers}")
        logging.info(f"Body: {data}")
        response = requests.post(reset_url, data=data, headers=headers, verify=False)
        logging.info(f"Status:{response.status_code}")
        logging.info(f"Body:\n{response.text}")
        if (
            response.status_code != 200
            and response.status_code != 201
            and response.status_code != 202
            and response.status_code != 204
        ):
            logging.error(
                "status code is not 200 or 201 or 202 or 204, Redfish Power Control:%s Fail"
                % reset_type
            )
            return False
        logging.info(
            "---------- Redfish Power Control:%s Succeed ----------" % reset_type
        )
    except Exception as e:
        logging.error(e)
        return False
    return True


def redfish_collect_blackbox_info(token):
    """
    Redfish收集黑盒日志
    Args:
        token (str): 认证token
    Returns:
        bool: 返回True表示收集成功, 返回False表示收集失败
    """
    try:
        logging.info("---------- Collect BlackBox Info ----------")
        logging.info("---------- Begin To Collecting BlackBox Info ----------")
        headers = {"Content-Type": "application/json", "X-Auth-Token": f"{token}"}
        collect_url = "https://{}/redfish/v1/Managers/{}/LogServices/Actions/Oem/{}/CollectAllLog".format(
            redfish_bmc_ip, manager_id, category
        )
        data = "{}"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.info(f"POST request sent to {collect_url}")
        logging.info(f"Headers: {headers}")
        response = requests.post(collect_url, data=data, headers=headers, verify=False)
        logging.info(f"Status:{response.status_code}")
        logging.info(f"Body:\n{response.text}")
        if (
            response.status_code != 200
            and response.status_code != 201
            and response.status_code != 202
            and response.status_code != 204
        ):
            logging.error(
                "status code is not 200 or 201 or 202 or 204, Redfish Collect BlackBox Info Url Run Failed"
            )
            return False
        logging.info("Redfish Collect BlackBox Info Url Run Succeed")
        time.sleep(SLEEP_TIME)
        for i in range(1, 20):
            logging.info(
                "---------- The %s Cycle Check BlackBox Info Collecting Status ----------"
                % i
            )
            if "NF5468M7" == machine_model or "NF5668M7" == machine_model:
                collect_status_url = (
                    "https://{}/redfish/v1/TaskService/Tasks/99".format(redfish_bmc_ip)
                )
            else:
                collect_status_url = "https://{}/redfish/v1/Managers/{}/LogServices/Actions/Oem/{}/CollectAllLog.Status".format(
                    redfish_bmc_ip, manager_id, category
                )
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logging.info(f"GET request sent to {collect_status_url}")
            logging.info(f"Headers: {headers}")
            response = requests.get(collect_status_url, headers=headers, verify=False)
            logging.info(f"Status:{response.status_code}")
            logging.info(f"Body:\n{response.text}")
            if (
                response.status_code != 200
                and response.status_code != 201
                and response.status_code != 202
                and response.status_code != 204
            ):
                logging.error(
                    "status code is not 200 or 201 or 202 or 204, Redfish Check BlackBox Collect Status Url Run Failed"
                )
                return False
            logging.info("Redfish Check BlackBox Collect Status Url Run Succeed")
            if "NF5468M7" == machine_model or "NF5668M7" == machine_model:
                collect_status = json.loads(response.text)["TaskState"]
                logging.info(f"collect_status: {collect_status}")
                if collect_status == "Completed":
                    logging.info("---------- Collect BlackBox Info Succeed ----------")
                    time.sleep(SLEEP_TIME)
                    break
                else:
                    logging.info(
                        "---------- Waiting For Collect BlackBox Info ----------\n"
                    )
                    time.sleep(CHECK_SLEEP_TIME)
                if i == 10 and collect_status != "Completed":
                    logging.error(
                        "---------- Collect BlackBox Info Failed ----------\n"
                    )
                    return False
            else:
                collect_status = json.loads(response.text)["Oem"][category]["Status"]
                logging.info(f"collect_status: {collect_status}")
                if collect_status == 0:
                    logging.info("---------- Collect BlackBox Info Succeed ----------")
                    time.sleep(SLEEP_TIME)
                    break
                else:
                    logging.info(
                        "---------- Waiting For Collect BlackBox Info ----------\n"
                    )
                    time.sleep(CHECK_SLEEP_TIME)
                if i == 10 and collect_status != 0:
                    logging.error(
                        "---------- Collect BlackBox Info Failed ----------\n"
                    )
                    return False
    except Exception as e:
        logging.error(e)
        return False
    return True


def redfish_download_blackbox_info(token):
    """
    Redfish下载黑盒日志
    Args:
        token (str): 认证token
    Returns:
        bool: 返回True表示下载成功, 返回False表示下载失败
    """
    try:
        logging.info("---------- Begin To Download BlackBox Info ----------")
        headers = {"Content-Type": "application/json", "X-Auth-Token": f"{token}"}
        download_blackbox_url = "https://{}/redfish/v1/Managers/{}/LogServices/Actions/Oem/{}/DownloadAllLog".format(
            redfish_bmc_ip, manager_id, category
        )
        data = "{}"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.info(f"POST request sent to {download_blackbox_url}")
        logging.info(f"Headers: {headers}")
        response = requests.post(
            download_blackbox_url, data=data, headers=headers, verify=False
        )
        logging.info(f"Status:{response.status_code}")
        if (
            response.status_code != 200
            and response.status_code != 201
            and response.status_code != 202
            and response.status_code != 204
        ):
            logging.error(
                "status code is not 200 or 201 or 202 or 204, Redfish Download BlackBox Info Url Run Failed"
            )
            return False
        logging.info("Redfish Download BlackBox Info Url Run Succeed")
        filetime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = "dump_" + filetime + ".tar.gz"
        with open("./log/" + filename, "wb+") as f:
            f.write(response.content)
            logging.info("---------- Download BlackBox Info Succeed ----------")
    except Exception as e:
        logging.error(e)
        return False
    return True


def Redfish_Get_User_Info(token, real_id):
    try:
        logging.info("---------- Get User Info ----------")
        headers = {"Content-Type": "application/json", "X-Auth-Token": f"{token}"}
        if (
            "S820-A3" == machine_model
            or "S820-A6" == machine_model
            or "S820-A9" == machine_model
            or "G225-B5" == machine_model
            or "G225-B5-2" == machine_model
            or "G225-B6" == machine_model
            or "G225-B6-2" == machine_model
            or "G225-B9" == machine_model
            or "G225-B9-2" == machine_model
        ):
            get_user_info_url = "https://{}/redfish/v1/AccountService/Accounts".format(
                redfish_bmc_ip
            )
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logging.info(f"GET request sent to {get_user_info_url}")
            logging.info(f"Headers: {headers}")
            response = requests.get(get_user_info_url, headers=headers, verify=False)
            logging.info(f"Status:{response.status_code}")
            logging.info(f"Body:\n{response.text}")
            if (
                response.status_code != 200
                and response.status_code != 201
                and response.status_code != 202
                and response.status_code != 204
            ):
                logging.error(
                    "status code is not 200 or 201 or 202 or 204, Redfish Get User Info Url Run Failed"
                )
                return False
            logging.info("Redfish Get User Info Url Run Succeed")
            user_id = int(json.loads(response.text)[real_id - 1]["Id"])
            user_name = json.loads(response.text)[real_id - 1]["UserName"]
            user_role = json.loads(response.text)[real_id - 1]["RoleId"].upper()
        else:
            get_user_info_url = (
                "https://{}/redfish/v1/AccountService/Accounts/{}".format(
                    redfish_bmc_ip, real_id
                )
            )
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logging.info(f"GET request sent to {get_user_info_url}")
            logging.info(f"Headers: {headers}")
            response = requests.get(get_user_info_url, headers=headers, verify=False)
            logging.info(f"Status:{response.status_code}")
            logging.info(f"Body:\n{response.text}")
            if (
                response.status_code != 200
                and response.status_code != 201
                and response.status_code != 202
                and response.status_code != 204
            ):
                logging.error(
                    "status code is not 200 or 201 or 202 or 204, Redfish Get User Info Url Run Failed"
                )
                return False
            logging.info("Redfish Get User Info Url Run Succeed")
            if machine_model == "G220-BA-B":
                user_id = json.loads(response.text)["Id"]
            else:
                user_id = int(json.loads(response.text)["Id"])
            user_name = json.loads(response.text)["UserName"]
            user_role = json.loads(response.text)["RoleId"].upper()
            if user_role == "READONLY":
                user_role = "USER"
    except Exception as e:
        logging.error(e)
        return False
    user = {"user_id": user_id, "user_name": user_name, "user_role": user_role}
    if real_id == 2 or real_id == "toutiao":
        logging.info("Default User Info is: {}".format(user))
    else:
        logging.info("User Info is: {}".format(user))
    return user


def Redfish_Get_Bios_Settings(token):
    try:
        logging.info("---------- Get Bios Settings ----------")
        headers = {"Content-Type": "application/json", "X-Auth-Token": f"{token}"}
        get_bios_settings_url = "https://{}/redfish/v1/Systems/{}/Bios".format(
            redfish_bmc_ip, system_id
        )
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.info(f"GET request sent to {get_bios_settings_url}")
        logging.info(f"Headers: {headers}")
        response = requests.get(get_bios_settings_url, headers=headers, verify=False)
        logging.info(f"Status:{response.status_code}")
        logging.info(f"Body:\n{response.text}")
        if (
            response.status_code != 200
            and response.status_code != 201
            and response.status_code != 202
            and response.status_code != 204
        ):
            logging.error(
                "status code is not 200 or 201 or 202 or 204, Redfish Get BIOS Settings Url Run Failed"
            )
            return False
        logging.info("Redfish Get BIOS Settings Url Run Succeed")
        bios_settings = json.loads(response.text)["Attributes"]
    except Exception as e:
        logging.error(e)
        return False
    return bios_settings


def Redfish_Change_Bios_Settings(token):
    try:
        logging.info("---------- Change BIOS Settings ----------")
        headers = {"Content-Type": "application/json", "X-Auth-Token": f"{token}"}
        if "R5500G5-2" == machine_model:
            bios_settings = '{"Attributes": {"QuietBoot": "Disabled"}}'
        elif (
            "G225-B5-2" == machine_model
            or "G225-B6-2" == machine_model
            or "G225-B9-2" == machine_model
        ):
            bios_settings = '{"Attributes": {"QuietBoot": false}}'
        elif (
            "S820-A3" == machine_model
            or "S820-A6" == machine_model
            or "S820-A9" == machine_model
            or "G225-B5" == machine_model
            or "G225-B6" == machine_model
            or "G225-B9" == machine_model
        ):
            bios_settings = '{"Attributes": {"QuietBoot": true}}'
        elif machine_model == "G220-BA-B":
            bios_settings = '{"Attributes": {"CRBCI3": "CRBCI3Disable"}}'
        else:
            bios_settings = '{"Attributes": {"QuietBoot": "Enabled"}}'
        change_bios_settings_url = (
            "https://{}/redfish/v1/Systems/{}/Bios/Settings".format(
                redfish_bmc_ip, system_id
            )
        )
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.info(f"Patch request sent to {change_bios_settings_url}")
        logging.info(f"Headers: {headers}")
        logging.info(f"Body: {bios_settings}")
        response = requests.patch(
            change_bios_settings_url, data=bios_settings, headers=headers, verify=False
        )
        logging.info(f"Status:{response.status_code}")
        logging.info(f"Body:\n{response.text}")
        if (
            response.status_code != 200
            and response.status_code != 201
            and response.status_code != 202
            and response.status_code != 204
        ):
            logging.error(
                "status code is not 200 or 201 or 202 or 204, Redfish Change BIOS Settings Url Run Failed"
            )
            return False
        logging.info("Redfish Change BIOS Settings Url Run Succeed")
    except Exception as e:
        logging.error(e)
        return False
    return True
