import sys
import time
import base64
import requests
import argparse
import configparser
import pandas as pd
from wcwidth import wcswidth    # 打印表格自动调整宽度，很重要
from tabulate import tabulate
from colorama import Fore, Style


# 检测账号状态
def check_status(key):
    url = f'https://fofa.info/api/v1/info/my?key={key}'
    try:
        response = requests.get(url).json()
        if response.get('error'):
            return False
        else:
            return True
    except requests.RequestException as e:
        print(Fore.RED + f'请求账号状态信息时出现异常: {e}' + Style.RESET_ALL)
        return False

# 查询用户信息
def my_info(key):
    url = f'https://fofa.info/api/v1/info/my?key={key}'
    try:
        response = requests.get(url).json()
        print(Fore.CYAN + "======账号信息=======" + Style.RESET_ALL)
        print(f"[+] 用户名：{response.get('username')}")
        print(f"[+] F币剩余数量：{response.get('fcoin')}")
        print(f"[+] VIP状态：{response.get('isvip')}")
        print(f"[+] VIP等级：{response.get('vip_level')}")
    except requests.RequestException as e:
        print(Fore.RED + f'获取用户信息时出现异常: {e}' + Style.RESET_ALL)

# FOFA查询主题
def get_search(q, size, email, key, fields):
    qb = base64.b64encode(q.encode('utf-8')).decode('utf-8')
    url = f'https://fofa.info/api/v1/search/all?email={email}&key={key}&size={size}&fields={fields}&qbase64={qb}'
    try:
        response = requests.get(url).json()
        result_data = response.get('results')
        if result_data:
            headers_list = list(fields.split(','))
            table = tabulate(result_data, headers=headers_list, tablefmt="psql")
            print(Fore.CYAN + "======查询内容=======" + Style.RESET_ALL)
            print(f"[+] 查询语句：{q}")
            print(f"[+] 查询字段：{fields}")
            print(f"[+] 查询条数：{size}")
            print(Fore.CYAN + "======查询结果=======" + Style.RESET_ALL)
            print(table)
            return result_data, headers_list
        else:
            print(Fore.RED + '查询无结果!' + Style.RESET_ALL)
            return [], []  # 如果没有查询结果，返回空列表
    except requests.RequestException as e:
        print(Fore.RED + f'执行查询时出现异常: {e}' + Style.RESET_ALL)
        return [], []  # 如果请求失败，返回空列表

# 保存查询结果为Excel
def save_excel(result_data, headers_list, filename):
    if result_data:  # 只有当查询有结果时才进行保存
        df = pd.DataFrame(result_data, columns=headers_list)
        filename_time = f"查询结果_{int(time.time())}.xlsx"
        if filename or output:      # 如果没有指定输出文件名，且配置中的output为True，才自动保存默认文件名的文件
            output_filename = filename or filename_time  # 如果指定了文件名，则使用指定的，否则使用默认文件名
            df.to_excel(output_filename, index=False)
            print(Fore.CYAN + "======保存文件=======" + Style.RESET_ALL)
            print(f"[+] 文件保存成功，文件名为：{output_filename}")
    else:
        print(Fore.RED + '没有查询结果可保存!' + Style.RESET_ALL)

# 从配置文件加载设置
def load_config():
    config = configparser.ConfigParser()
    config.read('fofa.ini', encoding='utf-8')
    email = config.get('info', 'email', fallback=None)
    key = config.get('info', 'key', fallback=None)
    fields = config.get('fields', 'fields')
    default_size = config.get('size', 'size', fallback='100')
    full = config.get('full', 'full', fallback='true').lower() == 'true'
    output = config.get('output', 'output', fallback='true').lower() == 'true'
    return email, key, fields, default_size, full, output


if __name__ == '__main__':
    email, key, fields, default_size, full, output = load_config()    # 加载配置

    if not email or not key:
        print(Fore.RED + '配置文件缺少必要的email或key!' + Style.RESET_ALL)
        sys.exit(1)

    # 解析命令行参数
    parser = argparse.ArgumentParser(description="FOFA API查询工具")
    parser.add_argument('-q', '--query', type=str, help='FOFA查询语句')
    parser.add_argument('-s', '--size', type=int, help='设置查询输出条数', default=default_size)
    parser.add_argument('-o', '--outfile', help='保存查询结果文件名')
    args = parser.parse_args()

    if check_status(key):   # 判断运行方式
        if args.query:
            my_info(key)
            result_data, headers_list = get_search(args.query, args.size, email, key, fields)
            save_excel(result_data, headers_list, args.outfile)
        else:
            my_info(key)
    else:
        print(Fore.RED + 'key无效!,请检查配置文件是否填写正确!' + Style.RESET_ALL)
