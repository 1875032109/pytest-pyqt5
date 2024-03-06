# content of conftest.py
import pytest
import os
from datetime import datetime


# 编辑报告标题
def pytest_html_report_title(report):
    report.title = "引入测试报告"


# def pytest_configure(config):
#     # 生成当前时间的文件名
#     current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
#     report_file = f"report-{current_time}.html"
#     # 设置 pytest-html 报告的文件名
#     config.option.htmlpath = "./log/" + report_file


# 测试结果表格
def pytest_html_results_table_header(cells):
    cells.insert(1, '<th class="sortable time" data-column-type="time">Time</th>')
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(1, f'<td class="col-time">{datetime.now()}</td>')
    cells.pop()
