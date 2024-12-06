**一.安装说明**

1.首次使用请使用 **pip install -r requirements.txt**命令，安装必要的外部依赖包。

2.使用前，先填写用户信息[info]中的email和key，**fofa.ini**配置文件如下：

```
[info]
#fofa注册时的邮箱
email = 
#fofa会员的key
key = 

[fields]
#查询内容选项
fields = host,protocol,ip,port,title,domain,country
#fields可选项：['host', 'title', 'ip', 'domain', 'port', 'country', 'province', 'city', 'country_name', 'header',
#              'server','protocol', 'banner', 'cert', 'isp', 'as_number', 'as_organization', 'latitude',
#              'longitude', 'structinfo','icp', 'fid', 'cname']

[size]
#每页查询数量，默认为100条，最大支持10,000条/页
size = 10

[full]
#默认搜索一年内的数据，指定为true即可搜索全部数据，false为一年内数据
full = False

[output]
#默认不自动输出结果为Excel文件
output = False
```

**二.使用方法**

```
python fofa.py -h                                                                                                                                            
usage: fofa.py [-h] [-q QUERY] [-s SIZE] [-o OUTFILE]                                                                                                
FOFA API查询工具                                                                                                                                                                 
options:                                                                                      
  -h, --help            show this help message and exit
  
  -q QUERY, --query QUERY   FOFA查询语句                                                                                                                                               
  -s SIZE, --size SIZE  设置查询输出条数                                                                                                                                           
  -o OUTFILE, --outfile OUTFILE 保存查询结果文件名
```

<img width="1153" alt="Snipaste_2024-12-06_11-24-27" src="https://github.com/user-attachments/assets/fd995d2c-156a-4082-8732-815ce04cacee">


