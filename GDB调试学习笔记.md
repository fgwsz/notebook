# `GDB`调试学习笔记
学习使用`GDB`来调试`Debug`可执行程序
## 安装`GDB`
```bash
sudo apt install gdb
```
## 使用`GDB`打开`Debug`可执行程序
```txt
语法:
    gdb [binary file path]
使用案例:
    gdb ./binary-debug # 使用gdb打开当前目录下的binary-debug可执行程序
```
## 显示行号和视图
命令格式                |作用                           |示例
:-----------------------|:------------------------------|:-------------------
`l`                     |显示当前暂停位置附近的10行代码 |`l`
`list`                  |显示当前暂停位置附近的10行代码 |`list`
`l [行号]`              |显示指定行号附近的代码         |`l 25`
`list [行号]`           |显示指定行号附近的代码         |`list 25`
`l [函数名]`            |显示函数的开头部分             |`l calculate_sum`
`list [函数名]`         |显示函数的开头部分             |`list calculate_sum`
`l [文件]:[行号]`       |显示其他文件的指定行           |`list utils.c:42`
`list [文件]:[行号]`    |显示其他文件的指定行           |`list utils.c:42`
`l [起始行],[结束行]`   |显示代码区间                   |`l 10,30`
`list [起始行],[结束行]`|显示代码区间                   |`list 10,30`
## 标记断点
### 文件断点
```txt
语法:
    b [file name]:[line number]
使用案例:
    b filename.c:20 # 在指定文件的第20行设置断点
```
### 函数断点
```txt
语法:
    b [function name]
使用案例:
    b main          # 在main函数入口设置断点
    b Person::say   # 在Person::say函数入口设置断点
```
### 条件断点
```txt
语法:
    b [line number] [condition]
使用案例:
    b 45 if i > 100 # 当变量i>100时触发第45行的断点
```
## 管理断点
### 查看断点编号
```bash
info breakpoints # 查看所有断点编号(ID)
```
### 移除指定编号的断点
```txt
语法:
    delete [ID]...
使用案例:
    delete 2     # 删除ID=2的断点
    delete 2 3 4 # 删除ID=2|3|4的断点
```
### 临时禁用指定编号的断点
```txt
语法:
    disable [ID]...
使用案例:
    disable 1     # 临时禁用ID=1的断点
    disable 1 2 3 # 临时禁用ID=1|2|3的断点
```
### 重新启用被临时禁用的指定编号的断点
```txt
用法:
    enable [ID]...
使用案例:
    enable 2        # 重新启用编号为2的断点
    enable 2 4 5    # 重新启用编号为2|4|5的断点
```
### 删除某函数的所有断点
```txt
语法:
    clear [function name]
使用案例:
    clear main # 删除main函数的所有断点

语法:
    clear [file name]:[function name]
使用案例:
    若函数在多个文件中定义,
    clear person.c:say # 删除person.c中的say函数的所有断点
```
### 临时禁用某函数的所有断点
```txt
方案一:结合info break与disable
    info break my_function  # 列出该函数所有断点ID
    disable 1 3 5           # 禁用ID为1|3|5的断点
方案二:通过正则表达式批量禁用(需GDB 7.0+):
    disable -r my_function.*
```
### 重新启用被临时禁用的某函数的所有断点
```txt
方案:与禁用操作类似,替换为enable
    info break my_function  # 获取断点ID
    enable 1 3 5            # 启用对应ID
```
### 删除所有的断点
```bash
d       # 删除所有的断点
delete  # 删除所有的断点
```
### 临时禁用所有的断点
```bash
disable # 临时禁用所有的断点
disable -r [regex]
    disable -r get_.* # 临时禁用所有get_前缀的函数断点
```
### 重新启用被临时禁用的所有的断点
```bash
enable # 重新启用被临时禁用的所有断点
enable -r [regex]
    enable -r get_.* # 重新启用被临时禁用所有get_前缀的函数断点
```
## 单步执行(进入函数内部)
```bash
s       # 执行一行代码,若遇到函数则进入其内部
step    # 同上(完整命令)
```
## 跳出函数内部
```bash
finish  # 执行完当前函数并返回到调用处
```
## 单步执行(不进入函数内部)
```bash
n       # 执行下一行代码,不进入函数内部
next    # 同上(完整命令)
```
## 查看变量值
```txt
p variable_name # 打印变量值(如`p sum`)
p &array        # 十六进制格式打印地址
x &array        # 十六进制格式打印地址
info locals     # 查看当前栈帧所有局部变量
```
## 查看函数返回值
```txt
1.在函数返回前设断点(如b actual_calc).
2.执行finish跳出函数,GDB自动显示返回值.
```
## 修改变量值
```txt
set var i = 0           # 将变量i赋值为0
set var ptr = 0x7ffffff # 修改指针地址
```
## 继续执行当前中断的程序
```bash
c        # 继续执行到下一断点
continue # 继续执行到下一断点
until 30 # 直接执行到第30行
```
## 重启调试进程
```bash
kill # 终止当前调试进程
run  # 重新启动
r    # 重新启动
run arg1 arg2 # 重新启动并指定main函数参数
r arg1 arg2   # 重新启动并指定main函数参数
```
## 退出`GDB`
```bash
exit
```
## 历史命令
```txt
使用上方向键可以调取之前输入的命令.
```
## 一些常见的调试问题
### `C++`中`step`无法进入内联函数
检查一下函数是否是内联函数:  
```bash
disas /m main # 查看main函数的反汇编
    # 若未出现call [inline funciton name]指令,说明函数被内联
```
使用如下指令,强制进入内联函数内部:  
```bash
stepi # 单步执行汇编指令,绕过内联
```
