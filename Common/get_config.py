import configparser
import os
import sys

path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(path)
# 读取配置文件
config = configparser.ConfigParser()
config.read("Common/Config/config.ini")
# 获取配置信息(注意返回的都是字符串)
machine_model = config["DEFAULT"]["machine_model"].strip()
os_ip = config["DEFAULT"]["os_ip"]
os_username = config["DEFAULT"]["os_username"]
os_password = config["DEFAULT"]["os_password"]
bmc_ip = config["DEFAULT"]["bmc_ip"]
redfish_bmc_ip = config["DEFAULT"]["redfish_bmc_ip"]
lan_channel = config["DEFAULT"]["lan_channel"]
bmc_username = config["DEFAULT"]["bmc_username"]
bmc_password = config["DEFAULT"]["bmc_password"]
bmc_ssh_username = config["DEFAULT"]["bmc_ssh_username"]
bmc_ssh_password = config["DEFAULT"]["bmc_ssh_password"]
bmc_ssh_error_password = config["DEFAULT"]["bmc_ssh_error_password"]
dpu_os_ip = config["DEFAULT"]["dpu_os_ip"]
dpu_bmc_ip = config["DEFAULT"]["dpu_bmc_ip"]
port = config["DEFAULT"]["port"]
sel_clear_log = config["DEFAULT"]["sel_clear_log"]
sel_fail_keywords = config["DEFAULT"]["sel_fail_keywords"].split(", ")
power_off_timeout = int(config["DEFAULT"]["power_off_timeout"])
power_on_timeout = int(config["DEFAULT"]["power_on_timeout"])
power_off_status = config["DEFAULT"]["power_off_status"]
power_on_status = config["DEFAULT"]["power_on_status"]
outband_update_file_path = config["DEFAULT"]["outband_update_file_path"]
inband_update_file_path = config["DEFAULT"]["inband_update_file_path"]
upgrade_bmc_file_name = config["DEFAULT"]["upgrade_bmc_file_name"]
downgrade_bmc_file_name = config["DEFAULT"]["downgrade_bmc_file_name"]
upgrade_bmc_version = config["DEFAULT"]["upgrade_bmc_version"]
downgrade_bmc_version = config["DEFAULT"]["downgrade_bmc_version"]
upgrade_bios_file_name = config["DEFAULT"]["upgrade_bios_file_name"]
downgrade_bios_file_name = config["DEFAULT"]["downgrade_bios_file_name"]
upgrade_bios_version = config["DEFAULT"]["upgrade_bios_version"]
downgrade_bios_version = config["DEFAULT"]["downgrade_bios_version"]


# 根据机型读取配置文件
product_config = configparser.ConfigParser()
if (
    machine_model == "G225-B5"
    or machine_model == "G225-B5-2"
    or machine_model == "G225-B6"
    or machine_model == "G225-B6-2"
    or machine_model == "G225-B9"
    or machine_model == "G225-B9-2"
):
    product_config.read("Common/Config/XiangYang/%s.ini" % machine_model)
elif (
    machine_model == "S820-A3"
    or machine_model == "S820-A6"
    or machine_model == "S820-A9"
):
    product_config.read("Common/Config/Poyanghu/%s.ini" % machine_model)
else:
    product_config.read("Common/Config/%s.ini" % machine_model)
category = product_config["DEFAULT"]["category"]
user_count = int(product_config["DEFAULT"]["user_count"])
soft_sel_log = product_config["DEFAULT"]["soft_sel_log"].split(", ")
off_sel_log = product_config["DEFAULT"]["off_sel_log"].split(", ")
on_sel_log = product_config["DEFAULT"]["on_sel_log"].split(", ")
cycle_sel_log = product_config["DEFAULT"]["cycle_sel_log"].split(", ")
reset_sel_log = product_config["DEFAULT"]["reset_sel_log"].split(", ")
system_id = product_config["DEFAULT"]["system_id"]
chassis_id = product_config["DEFAULT"]["chassis_id"]
manager_id = product_config["DEFAULT"]["manager_id"]
redfish_power_soft = product_config["DEFAULT"]["redfish_power_soft"]
redfish_power_on = product_config["DEFAULT"]["redfish_power_on"]
redfish_power_off = product_config["DEFAULT"]["redfish_power_off"]
redfish_power_reset = product_config["DEFAULT"]["redfish_power_reset"]
redfish_power_cycle = product_config["DEFAULT"]["redfish_power_cycle"]
