---
tags: 软件开发
---



Expect 是采用TCL脚本语言的用于提供自动交互的工具。

主要命令：

###### 1、send——向进程发送字符串

```bash
send "hello world\n"
```

###### 2、expect——从进程接收字符串

```bash
expect "hi\n"

# $expect_out(buffer)存储了所有对expect的输入
# <$expect_out(0,string)>存储了匹配到expect参数的输入
expect "hi\n"
send "you typed <$expect_out(buffer)>"
send "but I only expected <$expect_out(0,string)>"

# 模式-动作
expect "hi" {send "You said hi"}
# 多分支模式
expect "hi" { send "You said hi\n" } \
"hello" { send "Hello yourself\n" } \
"bye" { send "That was unexpected\n" }
```

###### 3、spawn——启动新的进程

```bash
set timeout -1
spawn ftp ftp.test.com
expect "Name"
send "user\r"
expect "Password:"
send "123456\r"
expect "ftp> "
send "binary\r"
expect "ftp> "
send "get test.tar.gz\r"
```



###### 4、interact——允许用户交互

```bash
spawn ftp ftp.test.com
expect "Name"
send "user\r"
expect "Password:"
send "123456\r"
interact
```



[原文](https://blog.csdn.net/jacky0922/article/details/45071817)