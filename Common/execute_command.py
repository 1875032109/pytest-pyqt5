import subprocess
import time
import logging


def execute_command(
    command, bmc_ip=None, bmc_username=None, bmc_password=None, command_type="outband"
):
    """
    Execute shell command.

    Args:
        command (str): Shell command to execute.
        bmc_ip (str): BMC IP address.
        bmc_username (str): BMC username.
        bmc_password (str): BMC password.
        command_type (str): Execution type, either "outband" or "outsystem".

    Returns:
        output (str): Command execution result.

    """
    try:
        if command_type == "outband":
            commands = f"ipmitool -I lanplus -H {bmc_ip} -U {bmc_username} -P {bmc_password} {command}"
        elif command_type == "outsystem":
            commands = command
        else:
            logging.error("Invalid command type specified.")
            return False

        result = subprocess.run(commands, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            if result.returncode == 1 and result.stdout != "":
                pass
            else:
                logging.error(
                    f"Command execution: {commands} failed with exit code {result.returncode}"
                )
                return False
        output = result.stdout.strip()
        outerr = result.stderr.strip()
        logging.info(f"Command execution success: {commands}")
        logging.info(f"output: {output}")
        logging.info(f"outerr: {outerr}")
    except Exception as e:
        logging.error(f"Command execution error: {e}")
        return False
    return output


def ping_ip(ip, timeout=300, ping_test="pass"):
    """
    Ping 一个 IP 地址，如果在超时期限内可达，则返回True, 否则返回False。
    参数：
        ip (str)：要ping的IP地址。
        timeout（int，可选）：超时时间（以秒为单位）, 默认为 300 秒。
        ping_test (str, 可选): 是否检查IP是否可达, 默认为"pass", 可选"pass"或"fail", 为"pass"时检查可达，为"fail"时检查不可达

    返回：
        bool：如果ip在超时时间内可达/不可达，则为True，否则为False。
    """
    start_time = time.time()
    while True:
        result = subprocess.run("ping -c 1 %s" % ip, shell=True)
        logging.info(result)
        if ping_test == "pass":
            if result.returncode == 0:
                logging.info(f"Ping {ip} 可达 success")
                return True
            elif time.time() - start_time > timeout:
                logging.error(f"Ping {ip} 可达 fail")
                return False
        elif ping_test == "fail":
            if result.returncode != 0:
                logging.info(f"Ping {ip} 不可达 success")
                return True
            elif time.time() - start_time > timeout:
                logging.error(f"Ping {ip} 不可达 fail")
                return False
        else:
            logging.error(f"ping_test must be 'pass' or 'fail'")
            return False
        time.sleep(1)
