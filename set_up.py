import subprocess


# 安装中文字体包
def install_chinese_fonts():
    subprocess.run(
        ["apt install fontconfig -y"],
        capture_output=True,
        text=True,
        shell=True,
    )
    font_count = subprocess.run(
        ["fc-list :lang=zh | wc -l"],
        capture_output=True,
        text=True,
        shell=True,
    )
    print(font_count)
    if font_count.stdout.strip().strip("\n") == "0":
        output = subprocess.run(
            [
                "apt update && apt install fonts-wqy-zenhei fonts-wqy-microhei fonts-arphic-ukai fonts-arphic-uming -y"
            ],
            capture_output=True,
            text=True,
            shell=True,
        )
        print(output.stdout)
    else:
        pass


def install_environment():
    output = subprocess.run(
        [
            "apt install sshpass libgl1-mesa-glx libglib2.0-dev libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xkb1 libxcb-shape0 libxkbcommon-x11-0 -y"
        ],
        capture_output=True,
        text=True,
        shell=True,
    )
    print(output.stdout)
    output = subprocess.run(
        ["export XDG_RUNTIME_DIR=/usr/lib/"],
        capture_output=True,
        text=True,
        shell=True,
    )
    print(output)
    # 读取 requirements.txt 文件中的软件包列表
    with open("requirements.txt", "r") as file:
        required_packages = file.readlines()

    # 检查每个软件包是否已安装在本地环境中
    for package in required_packages:
        package = package.strip()  # 去除行尾换行符和空格
        # 获取包名
        package_name = package.split("==")[0]
        # 使用 subprocess 模块调用 pip 命令查看软件包是否已安装
        result = subprocess.run(
            ["pip3", "show", package_name],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"{package} 已安装，跳过安装过程")
        else:
            # 如果软件包未安装，则使用 pip 安装它
            print(f"{package} 未安装，正在安装...")
            subprocess.run(
                ["pip3", "install", package_name],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"{package} 安装完成")


if __name__ == "__main__":
    install_chinese_fonts()
    install_environment()
