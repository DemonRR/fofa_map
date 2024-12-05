import time
import base64
import requests
import argparse
import configparser
import pandas as pd
from tabulate import tabulate
from colorama import Fore, Style


# 检测账号状态
def check_status(key):
    url = f'https://fofa.info/api/v1/info/my?key={key}'
    response = requests.get(url).json()
    if response.get('error'):
        return False
    else:
        return True

# 查询用户信息
def my_info(key):
    url = f'https://fofa.info/api/v1/info/my?key={key}'
    response = requests.get(url).json()
    print(Fore.CYAN + "======账号信息=======" + Style.RESET_ALL)
    print(f"[+] 用户名：{response.get('username')}")
    print(f"[+] F币剩余数量：{response.get('fcoin')}")
    print(f"[+] VIP状态：{response.get('isvip')}")
    print(f"[+] VIP等级：{response.get('vip_level')}")

# FOFA查询主题
def get_search(q, size, email, key, fields):
    qb = base64.b64encode(q.encode('utf-8')).decode('utf-8')
    url = f'https://fofa.info/api/v1/search/all?email={email}&key={key}&size={size}&fields={fields}&qbase64={qb}'
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
        quit()

# 保存查询结果为Excel
def save_excel(result_data, headers_list, filename):
    df = pd.DataFrame(result_data, columns=headers_list)
    filename_time = f"查询结果_{int(time.time())}.xlsx"
    if filename:
        df.to_excel(filename, index=False)
        print(Fore.CYAN + "======保存文件=======" + Style.RESET_ALL)
        print(f"[+] 文件保存成功，文件名为：{filename}")
    else:
        df.to_excel(filename_time, index=False)
        print(Fore.CYAN + "======保存文件=======" + Style.RESET_ALL)
        print(f"[+] 文件保存成功，默认文件名为：{filename_time}")

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('fofa.ini', encoding='utf-8')
    email = config.get('info', 'email')
    key = config.get('info', 'key')
    fields = config.get('fields', 'fields')
    default_size = config.get('size', 'size')

    parser = argparse.ArgumentParser(description="FOFA API查询工具")
    parser.add_argument('-q', '--query', type=str, help='FOFA查询语句')
    parser.add_argument('-s', '--size', help='设置查询输出条数')
    parser.add_argument('-o', '--outfile', help='保存查询结果')
    args = parser.parse_args()
    filename = args.outfile
    if check_status(key):
        if args.size:
            size = args.size
        else:
            size = default_size

        if args.query:
            my_info(key)
            result_data, headers_list = get_search(args.query, size, email, key, fields)
            save_excel(result_data, headers_list, filename)
        else:
            my_info(key)
    else:
        print(Fore.RED + 'key无效!,请检测配置文件是否填写正确!' + Style.RESET_ALL)