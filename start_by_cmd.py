import datetime
import os
import pytest
import logging
import argparse
import configparser


def add_args():
    parser = argparse.ArgumentParser(
        description="Add parameter for start_by_cmd.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="项目名称，eg: G225-B5,S820-A3,....",
    )
    parser.add_argument(
        "-t",
        "--test",
        type=str,
        nargs="+",
        required=False,
        help="测试用例选择，可选一个或者多个用例",
    )
    parser.add_argument(
        "-m",
        "--mark",
        type=str,
        required=False,
        help="运行标记用例，none_bare_metal/bare_metal 可选",
        choices=["none_bare_metal", "bare_metal"],
    )
    parser.add_argument(
        "-oa",
        "--other_args",
        type=str,
        required=False,
        help="方便手动添加pytest的其他多个命令行参数, 添加的参数以双引号括起来；如果只添加一个参数，参数末尾以空格结束",
    )
    # 解析命令行参数
    args = parser.parse_args()
    # 检查是否至少提供了一个必需参数
    if not (args.test or args.mark):
        parser.error("At least one of -t or -m is required")
    return args


def pytest_run():
    args = add_args()
    config = configparser.ConfigParser()
    config.read("Common/Config/config.ini")
    # 保存UI界面配置参数到Common/config.ini文件中
    config["DEFAULT"]["machine_model"] = args.project

    with open("Common/Config/config.ini", "w+") as configfile:
        config.write(configfile)
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = rf"log/{args.project}_{now}"
    html_log_path = rf"{log_path}/report.html"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    args_list = []
    if args.test:
        tests = " or ".join(args.test) if len(args.test) > 1 else "".join(args.test)
        args_list += ["-k", tests]
    if args.mark:
        args_list += ["-m", args.mark]
    if args.other_args:
        args_list += args.other_args.split(" ")
    args_list += [f"--html={html_log_path}"]
    # for a in args_list:
    #     print(a)
    try:
        pytest.main(args_list)
        return True
    except KeyboardInterrupt:
        logging.warning("Manual Interrupt By Keyboard, Stop The Test Process!")


if __name__ == "__main__":
    pytest_run()
