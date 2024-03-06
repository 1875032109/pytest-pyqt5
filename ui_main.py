# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QComboBox,
    QMessageBox,
    QStackedWidget,
    QProgressBar,
    QFrame,
    QLabel,
    QTextEdit,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from configparser import ConfigParser
import subprocess


class TestConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 创建输入框
        self.os_ip_label = QLabel("OS IP:")
        self.os_ip_input = QLineEdit(self)

        self.os_user_label = QLabel("OS User:")
        self.os_user_input = QLineEdit(self)
        self.os_user_input.setText("root")
        self.os_user_input.setReadOnly(True)

        self.os_password_label = QLabel("OS Password:")
        self.os_password_input = QLineEdit(self)
        self.os_password_input.setText("Duduadmin@1234")
        self.os_password_input.setReadOnly(True)

        self.bmc_ip_label = QLabel("BMC IP:")
        self.bmc_ip_input = QLineEdit(self)

        self.bmc_user_label = QLabel("BMC User:")
        self.bmc_user_input = QLineEdit(self)
        self.bmc_user_input.setText("toutiao")
        self.bmc_user_input.setReadOnly(True)

        self.bmc_password_label = QLabel("BMC Password:")
        self.bmc_password_input = QLineEdit(self)
        self.bmc_password_input.setText("toutiao!@#")
        self.bmc_password_input.setReadOnly(True)

        self.redfish_bmc_ip_label = QLabel("Redfish BMC IP:")
        self.redfish_bmc_ip_input = QLineEdit(self)
        self.redfish_bmc_ip_input.setPlaceholderText(
            "非裸金属机型直接填BMC IP，裸金属机型需要接端口号DPU OS IP:8443/DPU OS IP:9443"
        )

        self.dpu_os_ip_label = QLabel("DPU OS IP:")
        self.dpu_os_ip_input = QLineEdit(self)
        self.dpu_os_ip_input.setDisabled(True)

        self.dpu_bmc_ip_label = QLabel("DPU BMC IP:")
        self.dpu_bmc_ip_input = QLineEdit(self)
        self.dpu_bmc_ip_input.setDisabled(True)

        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit(self)
        self.port_input.setDisabled(True)
        self.port_input.setPlaceholderText("8443/9443")

        self.bmc_ssh_username_label = QLabel("BMC SSH Username:")
        self.bmc_ssh_username_input = QLineEdit(self)
        self.bmc_ssh_username_input.setText("sysadmin")
        # self.bmc_ssh_username_input.setReadOnly(True)

        self.bmc_ssh_password_label = QLabel("BMC SSH Password:")
        self.bmc_ssh_password_input = QLineEdit(self)
        self.bmc_ssh_password_input.setText("Byte@2023")
        # self.bmc_ssh_password_input.setReadOnly(True)

        self.bmc_ssh_error_password_label = QLabel("BMC SSH Error Password:")
        self.bmc_ssh_error_password_input = QLineEdit(self)
        self.bmc_ssh_error_password_input.setText("superuser")
        # self.bmc_ssh_error_password_input.setReadOnly(True)

        self.outband_update_file_path_label = QLabel("Outband Update File Path:")
        self.outband_update_file_path_input = QLineEdit(self)
        self.outband_update_file_path_input.setText("./outband_update")
        # self.outband_update_file_path_input.setReadOnly(True)

        self.inband_update_file_path_label = QLabel("Inband Update File Path:")
        self.inband_update_file_path_input = QLineEdit(self)
        self.inband_update_file_path_input.setText("/root/inband_update")
        # self.inband_update_file_path_input.setReadOnly(True)

        self.upgrade_bmc_file_name_label = QLabel("Upgrade BMC File Name:")
        self.upgrade_bmc_file_name_input = QLineEdit(self)

        self.downgrade_bmc_file_name_label = QLabel("Downgrade BMC File Name:")
        self.downgrade_bmc_file_name_input = QLineEdit(self)

        self.upgrade_bmc_version_label = QLabel("Upgrade BMC Version:")
        self.upgrade_bmc_version_input = QLineEdit(self)

        self.downgrade_bmc_version_label = QLabel("Downgrade BMC Version:")
        self.downgrade_bmc_version_input = QLineEdit(self)

        self.upgrade_bios_file_name_label = QLabel("Upgrade BIOS File Name:")
        self.upgrade_bios_file_name_input = QLineEdit(self)

        self.downgrade_bios_file_name_label = QLabel("Downgrade BIOS File Name:")
        self.downgrade_bios_file_name_input = QLineEdit(self)

        self.upgrade_bios_version_label = QLabel("Upgrade BIOS Version:")
        self.upgrade_bios_version_input = QLineEdit(self)

        self.downgrade_bios_version_label = QLabel("Downgrade BIOS Version:")
        self.downgrade_bios_version_input = QLineEdit(self)

        self.sel_clear_log_label = QLabel("Sel Clear Log:")
        self.sel_clear_log_input = QLineEdit(self)
        self.sel_clear_log_input.setText("Log area reset/cleared")
        self.sel_clear_log_input.setReadOnly(True)

        self.sel_fail_keywords_label = QLabel("Sel Fail Keywords:")
        self.sel_fail_keywords_input = QLineEdit(self)
        self.sel_fail_keywords_input.setText(
            "ecc, error, bus, upper, low, fail, correctable, lost, record"
        )
        self.sel_fail_keywords_input.setReadOnly(True)

        self.power_off_timeout_label = QLabel("Power Off Timeout:")
        self.power_off_timeout_input = QLineEdit(self)
        self.power_off_timeout_input.setText("90")
        self.power_off_timeout_input.setReadOnly(True)

        self.power_off_status_label = QLabel("Power Off Status:")
        self.power_off_status_input = QLineEdit(self)
        self.power_off_status_input.setText("Chassis Power is off")
        self.power_off_status_input.setReadOnly(True)

        self.power_on_timeout_label = QLabel("Power On Timeout:")
        self.power_on_timeout_input = QLineEdit(self)
        self.power_on_timeout_input.setText("300")
        self.power_on_timeout_input.setReadOnly(True)

        self.power_on_status_label = QLabel("Power On Status:")
        self.power_on_status_input = QLineEdit(self)
        self.power_on_status_input.setText("Chassis Power is on")
        self.power_on_status_input.setReadOnly(True)

        # 创建复选框
        self.bare_metal_checkbox = QCheckBox("是否是裸金属机型")
        self.bare_metal_checkbox.stateChanged.connect(self.show_dpu_fields)

        # 创建下拉列表
        self.lan_channel_label = QLabel("Lan Channel:")
        self.lan_channel_combo_box = QComboBox()
        self.lan_channel_combo_box.addItems(["1", "8"])

        self.machine_model_label = QLabel("Machine Model:")
        self.machine_model_combo_box = QComboBox()
        self.machine_model_combo_box.addItems(
            [
                "S820-A3",
                "S820-A6",
                "S820-A9",
                "G225-B5",
                "G225-B5-2",
                "G225-B6",
                "G225-B6-2",
                "G225-B9",
                "G225-B9-2",
                "G220-BA-B",
                "G228-AD",
                "NF5468M7",
                "R5300G6",
                "R5500G5-2",
            ]
        )

        # 添加保存配置的按钮
        self.save_button = QPushButton("保存配置")
        self.save_button.clicked.connect(self.save_config)

        # 创建布局
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        hbox7 = QHBoxLayout()
        hbox8 = QHBoxLayout()
        hbox9 = QHBoxLayout()
        hbox10 = QHBoxLayout()
        hbox11 = QHBoxLayout()
        hbox12 = QHBoxLayout()
        hbox13 = QHBoxLayout()
        hbox14 = QHBoxLayout()

        # 创建水平布局
        hbox1.addWidget(self.os_ip_label)
        hbox1.addWidget(self.os_ip_input)
        hbox1.addWidget(self.os_user_label)
        hbox1.addWidget(self.os_user_input)
        hbox1.addWidget(self.os_password_label)
        hbox1.addWidget(self.os_password_input)

        hbox2.addWidget(self.bmc_ip_label)
        hbox2.addWidget(self.bmc_ip_input)
        hbox2.addWidget(self.bmc_user_label)
        hbox2.addWidget(self.bmc_user_input)
        hbox2.addWidget(self.bmc_password_label)
        hbox2.addWidget(self.bmc_password_input)

        hbox3.addWidget(self.redfish_bmc_ip_label)
        hbox3.addWidget(self.redfish_bmc_ip_input)
        hbox3.addWidget(self.lan_channel_label)
        hbox3.addWidget(self.lan_channel_combo_box)

        hbox4.addWidget(self.bare_metal_checkbox, 2)
        hbox4.addWidget(self.machine_model_label)
        hbox4.addWidget(self.machine_model_combo_box, 4)

        hbox5.addWidget(self.dpu_os_ip_label)
        hbox5.addWidget(self.dpu_os_ip_input)
        hbox5.addWidget(self.dpu_bmc_ip_label)
        hbox5.addWidget(self.dpu_bmc_ip_input)
        hbox5.addWidget(self.port_label)
        hbox5.addWidget(self.port_input)

        hbox6.addWidget(self.bmc_ssh_username_label)
        hbox6.addWidget(self.bmc_ssh_username_input)
        hbox6.addWidget(self.bmc_ssh_password_label)
        hbox6.addWidget(self.bmc_ssh_password_input)
        hbox6.addWidget(self.bmc_ssh_error_password_label)
        hbox6.addWidget(self.bmc_ssh_error_password_input)

        hbox7.addWidget(self.outband_update_file_path_label)
        hbox7.addWidget(self.outband_update_file_path_input)
        hbox7.addWidget(self.inband_update_file_path_label)
        hbox7.addWidget(self.inband_update_file_path_input)

        hbox8.addWidget(self.upgrade_bmc_file_name_label)
        hbox8.addWidget(self.upgrade_bmc_file_name_input)
        hbox8.addWidget(self.downgrade_bmc_file_name_label)
        hbox8.addWidget(self.downgrade_bmc_file_name_input)

        hbox9.addWidget(self.upgrade_bmc_version_label)
        hbox9.addWidget(self.upgrade_bmc_version_input)
        hbox9.addWidget(self.downgrade_bmc_version_label)
        hbox9.addWidget(self.downgrade_bmc_version_input)

        hbox10.addWidget(self.upgrade_bios_file_name_label)
        hbox10.addWidget(self.upgrade_bios_file_name_input)
        hbox10.addWidget(self.downgrade_bios_file_name_label)
        hbox10.addWidget(self.downgrade_bios_file_name_input)

        hbox11.addWidget(self.upgrade_bios_version_label)
        hbox11.addWidget(self.upgrade_bios_version_input)
        hbox11.addWidget(self.downgrade_bios_version_label)
        hbox11.addWidget(self.downgrade_bios_version_input)

        hbox12.addWidget(self.sel_clear_log_label)
        hbox12.addWidget(self.sel_clear_log_input, 2)
        hbox12.addWidget(self.sel_fail_keywords_label)
        hbox12.addWidget(self.sel_fail_keywords_input, 5)

        hbox13.addWidget(self.power_off_timeout_label)
        hbox13.addWidget(self.power_off_timeout_input, 3)
        hbox13.addWidget(self.power_off_status_label)
        hbox13.addWidget(self.power_off_status_input)
        hbox13.addWidget(self.power_on_timeout_label)
        hbox13.addWidget(self.power_on_timeout_input, 3)
        hbox13.addWidget(self.power_on_status_label)
        hbox13.addWidget(self.power_on_status_input)

        hbox14.addWidget(self.save_button)

        # 添加水平布局到垂直布局
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)
        vbox.addLayout(hbox9)
        vbox.addLayout(hbox10)
        vbox.addLayout(hbox11)
        vbox.addLayout(hbox12)
        vbox.addLayout(hbox13)
        vbox.addLayout(hbox14)

        # 将布局应用到窗口
        self.setLayout(vbox)

    def show_dpu_fields(self, state):
        if state == 0:
            self.dpu_os_ip_input.setDisabled(True)
            self.dpu_bmc_ip_input.setDisabled(True)
            self.port_input.setDisabled(True)
            self.dpu_os_ip_input.clear()
            self.dpu_bmc_ip_input.clear()
            self.port_input.clear()
        else:
            self.dpu_os_ip_input.setDisabled(False)
            self.dpu_bmc_ip_input.setDisabled(False)
            self.port_input.setDisabled(False)

    def show_save_configuration_message(self, result, content):
        # 创建消息框
        msg_box = QMessageBox()
        msg_box.setWindowTitle(result)
        msg_box.setText(content)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    def save_config(self):
        config = ConfigParser()
        config.read("Common/Config/config.ini")
        # 保存UI界面配置参数到Common/config.ini文件中
        config["DEFAULT"] = {
            "machine_model": self.machine_model_combo_box.currentText(),
            "os_ip": self.os_ip_input.text(),
            "os_username": self.os_user_input.text(),
            "os_password": self.os_password_input.text(),
            "bmc_ip": self.bmc_ip_input.text(),
            "bmc_username": self.bmc_user_input.text(),
            "bmc_password": self.bmc_password_input.text(),
            "redfish_bmc_ip": self.redfish_bmc_ip_input.text(),
            "dpu_os_ip": self.dpu_os_ip_input.text(),
            "dpu_bmc_ip": self.dpu_bmc_ip_input.text(),
            "port": self.port_input.text(),
            "bmc_ssh_username": self.bmc_ssh_username_input.text(),
            "bmc_ssh_password": self.bmc_ssh_password_input.text(),
            "bmc_ssh_error_password": self.bmc_ssh_error_password_input.text(),
            "lan_channel": self.lan_channel_combo_box.currentText(),
            "outband_update_file_path": self.outband_update_file_path_input.text(),
            "inband_update_file_path": self.inband_update_file_path_input.text(),
            "upgrade_bmc_file_name": self.upgrade_bmc_file_name_input.text(),
            "downgrade_bmc_file_name": self.downgrade_bmc_file_name_input.text(),
            "upgrade_bmc_version": self.upgrade_bmc_version_input.text(),
            "downgrade_bmc_version": self.downgrade_bmc_version_input.text(),
            "upgrade_bios_file_name": self.upgrade_bios_file_name_input.text(),
            "downgrade_bios_file_name": self.downgrade_bios_file_name_input.text(),
            "upgrade_bios_version": self.upgrade_bios_version_input.text(),
            "downgrade_bios_version": self.downgrade_bios_version_input.text(),
            "sel_clear_log": self.sel_clear_log_input.text(),
            "sel_fail_keywords": self.sel_fail_keywords_input.text(),
            "power_off_timeout": self.power_off_timeout_input.text(),
            "power_off_status": self.power_off_status_input.text(),
            "power_on_timeout": self.power_on_timeout_input.text(),
            "power_on_status": self.power_on_status_input.text(),
        }

        with open("Common/Config/config.ini", "w+") as configfile:
            config.write(configfile)
        # 降本地的带内升降级工具和FW包上传到机器OS下
        output = subprocess.run(
            f"sshpass -p {self.os_password_input.text()} scp -o 'StrictHostKeyChecking=no' -r inband_update {self.os_user_input.text()}@{self.os_ip_input.text()}:/root",
            capture_output=True,
            shell=True,
            text=True,
        )
        if int(output.returncode) == 0:
            self.show_save_configuration_message(
                result="Success",
                content="保存配置成功 && 上传本地inband_update文件夹到机器OS下/root成功",
            )
        else:
            self.show_save_configuration_message(
                result="Failed",
                content="上传本地inband_update文件夹到机器OS下/root失败",
            )


class TestCaseWidget(QWidget):
    change_title_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker_thread = None

    def init_ui(self):
        # 非裸金属用例
        self.none_bare_matal_case_checkbox = QCheckBox("选中所有非裸金属用例")
        self.none_bare_matal_case_checkbox.stateChanged.connect(
            self.select_all_none_bare_metal_case
        )
        # 裸金属用例
        self.bare_matal_case_checkbox = QCheckBox("选中所有裸金属用例")
        self.bare_matal_case_checkbox.stateChanged.connect(
            self.select_all_bare_metal_case
        )
        # 创建复选框和数字显示测试顺序
        self.onekey_collect_checkbox = QCheckBox("一键收集日志")
        self.remote_power_control_checkbox = QCheckBox("远程电源管理")
        self.user_check_checkbox = QCheckBox("默认用户检查")
        self.bmc_access_checkbox = QCheckBox("BMC访问")
        self.ping_bmc_checkbox = QCheckBox("BMC连通稳定性")

        self.bmc_inupdate_default_checkbox = QCheckBox(
            "BMC带内不保留配置升降级-非裸金属"
        )
        self.bmc_inupdate_preserve_checkbox = QCheckBox(
            "BMC带内保留配置升降级-非裸金属"
        )
        self.bmc_outupdate_default_checkbox = QCheckBox(
            "BMC带外不保留配置升降级-非裸金属"
        )
        self.bmc_outupdate_preserve_checkbox = QCheckBox(
            "BMC带外保留配置升降级-非裸金属"
        )
        self.bios_inupdate_default_checkbox = QCheckBox(
            "BIOS带内不保留配置升降级-非裸金属"
        )
        self.bios_inupdate_preserve_checkbox = QCheckBox(
            "BIOS带内保留配置升降级-非裸金属"
        )
        self.bios_outupdate_default_checkbox = QCheckBox(
            "BIOS带外不保留配置升降级-非裸金属"
        )
        self.bios_outupdate_preserve_checkbox = QCheckBox(
            "BIOS带外保留配置升降级-非裸金属"
        )

        self.bmc_inupdate_default_bare_metal_checkbox = QCheckBox(
            "BMC带内不保留配置升降级-裸金属"
        )
        self.bmc_inupdate_preserve_bare_metal_checkbox = QCheckBox(
            "BMC带内保留配置升降级-裸金属"
        )
        self.bmc_outupdate_default_bare_metal_checkbox = QCheckBox(
            "BMC带外不保留配置升降级-裸金属"
        )
        self.bmc_outupdate_preserve_bare_metal_checkbox = QCheckBox(
            "BMC带外保留配置升降级-裸金属"
        )
        self.bios_inupdate_default_bare_metal_checkbox = QCheckBox(
            "BIOS带内不保留配置升降级-裸金属"
        )
        self.bios_inupdate_preserve_bare_metal_checkbox = QCheckBox(
            "BIOS带内保留配置升降级-裸金属"
        )
        self.bios_outupdate_default_bare_metal_checkbox = QCheckBox(
            "BIOS带外不保留配置升降级-裸金属"
        )
        self.bios_outupdate_preserve_bare_metal_checkbox = QCheckBox(
            "BIOS带外保留配置升降级-裸金属"
        )
        ### 测试用例执行顺序数字标记
        self.onekey_collect_number = QLabel()
        self.remote_power_control_number = QLabel()
        self.user_check_number = QLabel()
        self.bmc_access_number = QLabel()
        self.ping_bmc_number = QLabel()
        self.bios_outupdate_default_number = QLabel()
        self.bios_outupdate_preserve_number = QLabel()
        self.bios_outupdate_default_bare_metal_number = QLabel()
        self.bios_outupdate_preserve_bare_metal_number = QLabel()
        self.bios_inupdate_default_number = QLabel()
        self.bios_inupdate_preserve_number = QLabel()
        self.bios_inupdate_default_bare_metal_number = QLabel()
        self.bios_inupdate_preserve_bare_metal_number = QLabel()

        self.bmc_outupdate_default_number = QLabel()
        self.bmc_outupdate_preserve_number = QLabel()
        self.bmc_outupdate_default_bare_metal_number = QLabel()
        self.bmc_outupdate_preserve_bare_metal_number = QLabel()
        self.bmc_inupdate_default_number = QLabel()
        self.bmc_inupdate_preserve_number = QLabel()
        self.bmc_inupdate_default_bare_metal_number = QLabel()
        self.bmc_inupdate_preserve_bare_metal_number = QLabel()

        self.checkbox_name = [
            self.onekey_collect_checkbox,
            self.remote_power_control_checkbox,
            self.user_check_checkbox,
            self.bmc_access_checkbox,
            self.ping_bmc_checkbox,
            self.bios_outupdate_default_checkbox,
            self.bios_outupdate_preserve_checkbox,
            self.bios_outupdate_default_bare_metal_checkbox,
            self.bios_outupdate_preserve_bare_metal_checkbox,
            self.bios_inupdate_default_checkbox,
            self.bios_inupdate_preserve_checkbox,
            self.bios_inupdate_default_bare_metal_checkbox,
            self.bios_inupdate_preserve_bare_metal_checkbox,
            self.bmc_outupdate_default_checkbox,
            self.bmc_outupdate_preserve_checkbox,
            self.bmc_outupdate_default_bare_metal_checkbox,
            self.bmc_outupdate_preserve_bare_metal_checkbox,
            self.bmc_inupdate_default_checkbox,
            self.bmc_inupdate_preserve_checkbox,
            self.bmc_inupdate_default_bare_metal_checkbox,
            self.bmc_inupdate_preserve_bare_metal_checkbox,
        ]
        self.label_name = [
            self.onekey_collect_number,
            self.remote_power_control_number,
            self.user_check_number,
            self.bmc_access_number,
            self.ping_bmc_number,
            self.bios_outupdate_default_number,
            self.bios_outupdate_preserve_number,
            self.bios_outupdate_default_bare_metal_number,
            self.bios_outupdate_preserve_bare_metal_number,
            self.bios_inupdate_default_number,
            self.bios_inupdate_preserve_number,
            self.bios_inupdate_default_bare_metal_number,
            self.bios_inupdate_preserve_bare_metal_number,
            self.bmc_outupdate_default_number,
            self.bmc_outupdate_preserve_number,
            self.bmc_outupdate_default_bare_metal_number,
            self.bmc_outupdate_preserve_bare_metal_number,
            self.bmc_inupdate_default_number,
            self.bmc_inupdate_preserve_number,
            self.bmc_inupdate_default_bare_metal_number,
            self.bmc_inupdate_preserve_bare_metal_number,
        ]
        for checkbox in self.checkbox_name:
            checkbox.stateChanged.connect(self.update_label)
        # 添加开始测试的按钮
        self.begin_test_button = QPushButton("开始测试")
        self.begin_test_button.clicked.connect(self.clear_progress_and_log)
        self.begin_test_button.clicked.connect(self.begin_test)
        # 创建并设置 QProcessbar
        self.progressBar = QProgressBar(self)  # 创建
        self.progressBar.setMinimum(0)  # 设置进度条最小值
        self.progressBar.setMaximum(100)  # 设置进度条最大值
        self.progressBar.setValue(0)  # 进度条初始值为0
        # 创建日志显示区域
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)

        # 创建布局
        vbox = QVBoxLayout()
        vlog_box = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        hbox7 = QHBoxLayout()
        hbox8 = QHBoxLayout()
        hbox9 = QHBoxLayout()
        hbox10 = QHBoxLayout()
        hbox11 = QHBoxLayout()
        hbox12 = QHBoxLayout()
        hbox13 = QHBoxLayout()

        # 创建水平布局
        hbox1.addWidget(self.none_bare_matal_case_checkbox)
        hbox1.addWidget(self.bare_matal_case_checkbox)

        hbox2.addWidget(self.onekey_collect_checkbox)
        hbox2.addWidget(self.onekey_collect_number)
        hbox2.addWidget(self.remote_power_control_checkbox)
        hbox2.addWidget(self.remote_power_control_number)

        hbox3.addWidget(self.user_check_checkbox)
        hbox3.addWidget(self.user_check_number)
        hbox3.addWidget(self.bmc_access_checkbox)
        hbox3.addWidget(self.bmc_access_number)

        hbox4.addWidget(self.bmc_inupdate_default_checkbox)
        hbox4.addWidget(self.bmc_inupdate_default_number)
        hbox4.addWidget(self.bmc_inupdate_preserve_checkbox)
        hbox4.addWidget(self.bmc_inupdate_preserve_number)

        hbox5.addWidget(self.bmc_outupdate_default_checkbox)
        hbox5.addWidget(self.bmc_outupdate_default_number)
        hbox5.addWidget(self.bmc_outupdate_preserve_checkbox)
        hbox5.addWidget(self.bmc_outupdate_preserve_number)

        hbox6.addWidget(self.bios_inupdate_default_checkbox)
        hbox6.addWidget(self.bios_inupdate_default_number)
        hbox6.addWidget(self.bios_inupdate_preserve_checkbox)
        hbox6.addWidget(self.bios_inupdate_preserve_number)

        hbox7.addWidget(self.bios_outupdate_default_checkbox)
        hbox7.addWidget(self.bios_outupdate_default_number)
        hbox7.addWidget(self.bios_outupdate_preserve_checkbox)
        hbox7.addWidget(self.bios_outupdate_preserve_number)

        hbox8.addWidget(self.bmc_inupdate_default_bare_metal_checkbox)
        hbox8.addWidget(self.bmc_inupdate_default_bare_metal_number)
        hbox8.addWidget(self.bmc_inupdate_preserve_bare_metal_checkbox)
        hbox8.addWidget(self.bmc_inupdate_preserve_bare_metal_number)

        hbox9.addWidget(self.bmc_outupdate_default_bare_metal_checkbox)
        hbox9.addWidget(self.bmc_outupdate_default_bare_metal_number)
        hbox9.addWidget(self.bmc_outupdate_preserve_bare_metal_checkbox)
        hbox9.addWidget(self.bmc_outupdate_preserve_bare_metal_number)

        hbox10.addWidget(self.bios_inupdate_default_bare_metal_checkbox)
        hbox10.addWidget(self.bios_inupdate_default_bare_metal_number)
        hbox10.addWidget(self.bios_inupdate_preserve_bare_metal_checkbox)
        hbox10.addWidget(self.bios_inupdate_preserve_bare_metal_number)

        hbox11.addWidget(self.bios_outupdate_default_bare_metal_checkbox)
        hbox11.addWidget(self.bios_outupdate_default_bare_metal_number)
        hbox11.addWidget(self.bios_outupdate_preserve_bare_metal_checkbox)
        hbox11.addWidget(self.bios_outupdate_preserve_bare_metal_number)

        hbox12.addWidget(self.ping_bmc_checkbox)
        hbox12.addWidget(self.ping_bmc_number)

        vlog_box.addWidget(self.log_text_edit)

        hbox13.addWidget(self.begin_test_button)
        hbox13.addWidget(self.progressBar)

        # 创建分割线
        self.separator_line = QFrame()
        self.separator_line.setFrameShape(QFrame.HLine)
        self.separator_line.setFrameShadow(QFrame.Sunken)

        # 添加水平布局到垂直布局
        vbox.addLayout(hbox1)
        vbox.addWidget(self.separator_line)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)
        vbox.addLayout(hbox9)
        vbox.addLayout(hbox10)
        vbox.addLayout(hbox11)
        vbox.addLayout(hbox12)
        vbox.addLayout(vlog_box)
        vbox.addLayout(hbox13)

        # 将布局应用到窗口
        self.setLayout(vbox)

    def select_all_none_bare_metal_case(self, state):
        if state == 0:
            self.onekey_collect_checkbox.setChecked(False)
            self.remote_power_control_checkbox.setChecked(False)
            self.user_check_checkbox.setChecked(False)
            self.bmc_access_checkbox.setChecked(False)
            self.ping_bmc_checkbox.setChecked(False)
            self.bios_outupdate_default_checkbox.setChecked(False)
            self.bios_outupdate_preserve_checkbox.setChecked(False)
            self.bios_inupdate_default_checkbox.setChecked(False)
            self.bios_inupdate_preserve_checkbox.setChecked(False)
            self.bmc_outupdate_default_checkbox.setChecked(False)
            self.bmc_outupdate_preserve_checkbox.setChecked(False)
            self.bmc_inupdate_default_checkbox.setChecked(False)
            self.bmc_inupdate_preserve_checkbox.setChecked(False)
        else:
            if self.bare_matal_case_checkbox.isChecked():
                self.bare_matal_case_checkbox.setChecked(False)
            self.clear_all_select()
            self.onekey_collect_checkbox.setChecked(True)
            self.remote_power_control_checkbox.setChecked(True)
            self.user_check_checkbox.setChecked(True)
            self.bmc_access_checkbox.setChecked(True)
            self.ping_bmc_checkbox.setChecked(True)
            self.bios_outupdate_default_checkbox.setChecked(True)
            self.bios_outupdate_preserve_checkbox.setChecked(True)
            self.bios_inupdate_default_checkbox.setChecked(True)
            self.bios_inupdate_preserve_checkbox.setChecked(True)
            self.bmc_outupdate_default_checkbox.setChecked(True)
            self.bmc_outupdate_preserve_checkbox.setChecked(True)
            self.bmc_inupdate_default_checkbox.setChecked(True)
            self.bmc_inupdate_preserve_checkbox.setChecked(True)

    def select_all_bare_metal_case(self, state):
        if state == 0:
            self.onekey_collect_checkbox.setChecked(False)
            self.remote_power_control_checkbox.setChecked(False)
            self.user_check_checkbox.setChecked(False)
            self.bmc_access_checkbox.setChecked(False)
            self.ping_bmc_checkbox.setChecked(False)
            self.bios_outupdate_default_bare_metal_checkbox.setChecked(False)
            self.bios_outupdate_preserve_bare_metal_checkbox.setChecked(False)
            self.bios_inupdate_default_bare_metal_checkbox.setChecked(False)
            self.bios_inupdate_preserve_bare_metal_checkbox.setChecked(False)
            self.bmc_outupdate_default_bare_metal_checkbox.setChecked(False)
            self.bmc_outupdate_preserve_bare_metal_checkbox.setChecked(False)
            self.bmc_inupdate_default_bare_metal_checkbox.setChecked(False)
            self.bmc_inupdate_preserve_bare_metal_checkbox.setChecked(False)
        else:
            if self.none_bare_matal_case_checkbox.isChecked():
                self.none_bare_matal_case_checkbox.setChecked(False)
            self.clear_all_select()
            self.onekey_collect_checkbox.setChecked(True)
            self.remote_power_control_checkbox.setChecked(True)
            self.user_check_checkbox.setChecked(True)
            self.bmc_access_checkbox.setChecked(True)
            self.ping_bmc_checkbox.setChecked(True)
            self.bios_outupdate_default_bare_metal_checkbox.setChecked(True)
            self.bios_outupdate_preserve_bare_metal_checkbox.setChecked(True)
            self.bios_inupdate_default_bare_metal_checkbox.setChecked(True)
            self.bios_inupdate_preserve_bare_metal_checkbox.setChecked(True)
            self.bmc_outupdate_default_bare_metal_checkbox.setChecked(True)
            self.bmc_outupdate_preserve_bare_metal_checkbox.setChecked(True)
            self.bmc_inupdate_default_bare_metal_checkbox.setChecked(True)
            self.bmc_inupdate_preserve_bare_metal_checkbox.setChecked(True)

    def clear_all_select(self):
        for i in self.checkbox_name:
            i.setChecked(False)

    def get_selected_case(self):
        test_cases_mapping = {
            self.onekey_collect_checkbox: "test_onekey_collect.py",
            self.remote_power_control_checkbox: "test_remote_power_control.py",
            self.user_check_checkbox: "test_user_check.py",
            self.bmc_access_checkbox: "test_bmc_access.py",
            self.ping_bmc_checkbox: "test_ping_bmc.py",
            self.bmc_outupdate_default_checkbox: "test_update_bmc_outband_default.py",
            self.bmc_outupdate_preserve_checkbox: "test_update_bmc_outband_preserve.py",
            self.bmc_outupdate_default_bare_metal_checkbox: "test_update_bmc_outband_default_bare_metal.py",
            self.bmc_outupdate_preserve_bare_metal_checkbox: "test_update_bmc_outband_preserve_bare_metal.py",
            self.bmc_inupdate_default_checkbox: "test_update_bmc_inband_default.py",
            self.bmc_inupdate_preserve_checkbox: "test_update_bmc_inband_preserve.py",
            self.bmc_inupdate_default_bare_metal_checkbox: "test_update_bmc_inband_default_bare_metal.py",
            self.bmc_inupdate_preserve_bare_metal_checkbox: "test_update_bmc_inband_preserve_bare_metal.py",
            self.bios_inupdate_default_checkbox: "test_update_bios_inband_default.py",
            self.bios_inupdate_preserve_checkbox: "test_update_bios_inband_preserve.py",
            self.bios_inupdate_default_bare_metal_checkbox: "test_update_bios_inband_default_bare_metal.py",
            self.bios_inupdate_preserve_bare_metal_checkbox: "test_update_bios_inband_preserve_bare_metal.py",
            self.bios_outupdate_default_checkbox: "test_update_bios_outband_default.py",
            self.bios_outupdate_preserve_checkbox: "test_update_bios_outband_preserve.py",
            self.bios_outupdate_default_bare_metal_checkbox: "test_update_bios_outband_default_bare_metal.py",
            self.bios_outupdate_preserve_bare_metal_checkbox: "test_update_bios_outband_preserve_bare_metal.py",
        }

        # 创建一个字典，将复选框与标签进行映射
        # 创建复选框和标签的映射关系
        checkbox_label_map = {}
        for checkbox, label in zip(self.checkbox_name, self.label_name):
            checkbox_label_map[checkbox] = label

        # 获取已选中的复选框
        selected_checkboxes = [
            checkbox for checkbox in self.checkbox_name if checkbox.isChecked()
        ]
        # 根据复选框对应的标签编号大小进行排序
        sorted_selected_checkboxes = sorted(
            selected_checkboxes,
            key=lambda checkbox: int(checkbox_label_map[checkbox].text()),
        )
        # 根据排序后的复选框获取对应的测试用例并存放到 self.selected_case 中
        self.selected_case = [
            test_cases_mapping[checkbox] for checkbox in sorted_selected_checkboxes
        ]
        return self.selected_case

    def update_label(self, state):
        checked_count = sum(checkbox.isChecked() for checkbox in self.checkbox_name)
        sender_checkbox = self.sender()
        if state == Qt.Checked:
            for checkbox, label in zip(self.checkbox_name, self.label_name):
                if checkbox.isChecked():
                    if checkbox is sender_checkbox:
                        label.setText(str(checked_count))
        else:
            for checkbox, label in zip(self.checkbox_name, self.label_name):
                if checkbox is sender_checkbox:
                    uncheck_label_number = int(label.text())
                    label.setText("")
            for checkbox, label in zip(self.checkbox_name, self.label_name):
                if checkbox.isChecked():
                    if int(label.text()) > uncheck_label_number:
                        label.setText(str(int(label.text()) - 1))
                if checkbox is sender_checkbox:
                    label.setText("")

    def begin_test(self):
        # 创建并启动后台线程
        self.worker_thread = WorkerThread(test_case_window=self)
        self.worker_thread.update_title.connect(self.updateTitle)
        self.worker_thread.update_progress.connect(self.updateProgress)
        self.worker_thread.new_log.connect(self.update_log_area)
        self.worker_thread.start()

    def updateProgress(self, value):
        self.progressBar.setValue(value)
        if int(value) == 100:
            self.change_title_signal.emit("测试完成")
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Success")
            msg_box.setText("测试完成")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()

    def updateTitle(self, task, total_tasks):
        if task == 0 and total_tasks == 0:
            self.change_title_signal.emit("请选择测试用例")
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Warning")
            msg_box.setText("请选择测试用例")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()
        else:
            label = "正在处理：第{}个任务/共{}个任务".format(task, total_tasks)
            self.change_title_signal.emit(label)

    def update_log_area(self, new_log_data):
        # 将新日志数据追加到日志显示区域
        self.log_text_edit.append(new_log_data)

    def clear_progress_and_log(self):
        self.updateProgress(0)
        self.log_text_edit.clear()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建测试配置和测试用例界面
        self.test_config_widget = TestConfigWidget()
        self.test_case_widget = TestCaseWidget()

        # 创建侧边栏按钮
        self.test_config_button = QPushButton("Test Configuration")
        self.test_case_button = QPushButton("Test Case")

        # 创建堆叠窗口
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.test_config_widget)
        self.stacked_widget.addWidget(self.test_case_widget)

        # 创建分割线
        self.separator_line = QFrame()
        self.separator_line.setFrameShape(QFrame.VLine)
        self.separator_line.setFrameShadow(QFrame.Sunken)

        # 连接按钮点击事件
        self.test_config_button.clicked.connect(self.show_test_config)
        self.test_case_button.clicked.connect(self.show_test_case)

        # 创建布局
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.addWidget(self.test_config_button)
        self.sidebar_layout.addWidget(self.test_case_button)
        self.sidebar_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addLayout(self.sidebar_layout)
        main_layout.addWidget(self.separator_line)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def show_test_config(self):
        self.stacked_widget.setCurrentIndex(0)  # 显示测试配置界面

    def show_test_case(self):
        self.stacked_widget.setCurrentIndex(1)  # 显示测试用例界面
        self.test_case_widget.change_title_signal.connect(self.change_title)

    def change_title(self, title):
        self.setWindowTitle(title)


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)  # 定义进度条信号
    update_title = pyqtSignal(int, int)  # 定义标题更新信号
    new_log = pyqtSignal(str)  # 定义新日志信号

    def __init__(self, parent=None, test_case_window=None):
        super().__init__(parent)
        self.test_case_window = test_case_window

    def run(self):
        all_task = ""
        if self.test_case_window:
            self.selected_case = self.test_case_window.get_selected_case()

        self.total_tasks = len(self.selected_case)
        for task in self.selected_case:
            all_task += f"Test/{task} "
        if all_task == "":
            self.update_title.emit(self.total_tasks, self.total_tasks)
            self.update_progress.emit(0)
        else:
            self.run_process(all_task)

    def run_process(self, all_task):
        process = subprocess.Popen(
            f"pytest -v {all_task}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        while True:
            line = process.stdout.readline()
            if not line:
                break
            self.new_log.emit(line.strip())
            for case_name in self.selected_case:
                if f"Test/{case_name}::{case_name[:-3]}" in line:
                    task = self.selected_case.index(case_name)
                    progress_value = int((task) * 100 / self.total_tasks)
                    self.update_title.emit(task + 1, self.total_tasks)
                    self.update_progress.emit(progress_value)
        process.stdout.close()
        process.wait()
        self.update_progress.emit(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowTitle("Test Application")
    main_window.show()
    sys.exit(app.exec_())
