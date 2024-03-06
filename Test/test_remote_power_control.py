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
def test_remote_power_control():
    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行软关机电源控制操作,并确认执行成功
    Command_Check("chassis power soft")

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("off")

    # 检测关机日志是否正确以及是否存在告警日志
    Sel_Check(soft_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行开机电源控制操作,并确认执行成功
    Command_Check("chassis power on")

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("on")

    # 检测开机日志是否正确以及是否存在告警日志
    Sel_Check(on_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行关机电源控制操作,并确认执行成功
    Command_Check("chassis power off")

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("off")

    # 检测关机日志是否正确以及是否存在告警日志
    Sel_Check(off_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行开机电源控制操作,并确认执行成功
    Command_Check("chassis power on")

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("on")

    # 检测开机日志是否正确以及是否存在告警日志
    Sel_Check(on_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行Power Cycle电源控制操作,并确认执行成功
    Command_Check("chassis power cycle")

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("cycle")

    # 检测Power Cycle日志是否正确以及是否存在告警日志
    Sel_Check(cycle_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行Power Reset电源控制操作,并确认执行成功
    Command_Check("chassis power reset")

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("reset")

    # 检测Power Reset日志是否正确以及是否存在告警日志
    Sel_Check(reset_sel_log)

    # 使用BMC用户信息进行登录Redfish,如果登录失败,则抛出异常
    token, session_id = login_to_redfish_bmc()
    assert token and session_id, "Redfish Create Session Fail"

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行软关机电源控制操作,并确认执行成功
    assert Redfish_Power_Control(redfish_power_soft, token), "power soft failed"

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("off")

    # 检测关机日志是否正确以及是否存在告警日志
    Sel_Check(soft_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行开机电源控制操作,并确认执行成功
    assert Redfish_Power_Control(redfish_power_on, token), "power on failed"

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("on")

    # 检测开机日志是否正确以及是否存在告警日志
    Sel_Check(on_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行关机电源控制操作,并确认执行成功
    assert Redfish_Power_Control(redfish_power_off, token), "power off failed"

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("off")

    # 检测关机日志是否正确以及是否存在告警日志
    Sel_Check(off_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行开机电源控制操作,并确认执行成功
    assert Redfish_Power_Control(redfish_power_on, token), "power on failed"

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("on")

    # 检测开机日志是否正确以及是否存在告警日志
    Sel_Check(on_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行Power Cycle电源控制操作,并确认执行成功
    assert Redfish_Power_Control(redfish_power_cycle, token), "power cycle failed"

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("cycle")

    # 检测Power Cycle日志是否正确以及是否存在告警日志
    Sel_Check(cycle_sel_log)

    # 清除sel日志,并确认清除成功
    Sel_Clear()

    # 执行Power Reset电源控制操作,并确认执行成功
    assert Redfish_Power_Control(redfish_power_reset, token), "power reset failed"

    # Ping OS IP,并检测Power Status是否正确
    Ping_Check("reset")

    # 检测Power Reset日志是否正确以及是否存在告警日志
    Sel_Check(reset_sel_log)

    # 登出Redfish会话,如果登出失败则抛出异常
    assert logout_from_redfish_bmc(token, session_id), "Redfish Delete Session Fail"
