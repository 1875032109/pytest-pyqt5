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
def test_onekey_collect():

    # 使用BMC用户信息进行登录Redfish,如果登录失败,则抛出异常
    token, session_id = login_to_redfish_bmc()
    assert token and session_id, "Redfish Create Session Fail"

    # 调用Redfish Collect BlackBox Info函数收集黑盒日志,并断言结果不为False,否则抛出异常
    assert redfish_collect_blackbox_info(token), "Redfish Collect BlackBox Info Fail"

    # 调用Redfish Download BlackBox Info函数下载黑盒日志，并断言结果不为False,否则抛出异常
    assert redfish_download_blackbox_info(token), "Redfish Download BlackBox Info Fail"

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"
