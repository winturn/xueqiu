# xueqiu
收集券商雪球（xueqiu.com）上面某一用户的所有讨论内容。

# 修改配置文件
在项目目录下，创建配置文件
```shell
cp config.json.template config.json
```

然后修改文件内的配置，改为自己账号的session

# 运行
执行命令运行python
```shell
python main.py
```

# 查看结果
导出结果至桌面，文件名是当前日期，文件格式是excel文件


# 其他
如果想修改获取的字段，可参考 ./tmp/data_format.json 文件，这是GET数据时获取到的数据格式。
