### 引入测试自动化 ###
1、文件目录介绍
BMC_Python  ### 根目录
    .pytest_cache   ### Pytest的缓存目录，用于存储测试运行时的临时文件和缓存信息
    Common          ### 测试功能方法模块
		Config              ### 默认配置文件和各机型默认配置文件
			config.ini 		### 默认配置文件(包含IP信息和升降级版本工具等信息)
			项目号.ini      ### 各机型默认配置文件
        chec_base.py        ### 校验命令文件
        config.ini          ### 机器配置文件
        execute_command.py  ### 带外执行命令文件
        get_config.py       ### 获取机器配置文件
		get_machine.py      ### 获取各机型默认配置文件
        remote_redfish.py   ### 带外redfish文件
        remote_ssh.py       ### ssh方法文件
    log                 ### 运行日志存放目录
    outband_update      ### 带外升级文件和工具存放目录
    inband_update       ### 带内升级文件和工具存放目录
    Test                ### 测试用例目录
    conftest.py         ### 用于定义项目中的共享的fixture和插件
    pytest.ini          ### pytest的配置文件，用于配置pytest测试运行时的各种选项和参数
    requirements.txt    ### 列出项目所依赖的第三方库及其版本信息
    set_up.py           ### 环境检查和环境安装
    start_by_cmd.py     ### 通过手动输入命令运行测试
    ui_main.py          ### 运行主界面
    
2、使用介绍（所有操作都是在BMC_Python根目录下执行）（只能在linux环境使用）
    UI运行
        1.首次运行需要先执行 python3 set_up.py (安装第三方库和中文字体文件)
        2.执行 python3 ui_main.py (进入测试UI页面，UI界面共2个页面组成)
            Test Configuration 页面：填写机型配置，点击保存配置，出现保存配置成功提示则保存配置成功（会自动将机器配置保存到config.ini文件中）
            Test Case 页面：选择所要执行的用例，点击开始测试，进度条100%且出现测试完成提示则测试完成；测试日志会实时打印在页面空白框处（同时log文件夹下也会生成html类型的日志文件）
                1.选中所有非裸金属用例：会自动选择非裸金属用例，每个用例后面数字是执行顺序（从1开始执行）
                2.选中所有裸金属用例：会自动选择裸金属用例，每个用例后面数字是执行顺序（从1开始执行）
                3.单选用例：会根据单选的先后顺序去执行用例
        3.非首次运行-直接运行步骤2（python3 ui_main.py）
    非UI运行
        1.填写Common/Config/config.ini 配置文件
        2.python3 start_by_cmd.py -p 项目名称(eg:NF5468M7) （-t 测试用例 / -m 标记的测试用例） 

3、测试前准备
    1.确保本地有python3环境(python3.8+)
    2.将带外升级文件和工具放入本地 BMC_Python/outband_update 目录下（注意：带外工具和升级文件必须在outband_update目录下）
    3.将带内升级文件和工具放入机器 root/inband_update 目录下（注意：带内工具和升级文件必须在inband_update目录下）
    4.在自己本地环境命令行执行 kinit（确保本地能够和机器正常连通）