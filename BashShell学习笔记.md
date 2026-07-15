# 创建一个脚本
## 脚本文件头
`#!/bin/bash`
## 赋予脚本文件可执行权限
`chmod +x bash_shell_script_file_path`
## 变量命名
变量名:字母数字下划线组成的文本字符串,长度不超过20个字符.

变量名区分字母大小写.
## 用户变量定义
## 变量赋值

变量赋值过程变量、等号和值之间不能出现空格.

[x]`var1 = 100`

[v]`var1=100`

## 变量作用域
### 全局变量
全局变量直接使用
`variable_name`

`variable_name=variable_value`
### 局部变量
#### 函数体内部的局部变量
注意:`local`关键字只能用于函数体内部,无法用于函数体外部的空间
`local variable_name`

`local variable_name=variable_value`

`local -n ref_variable_name=expr`
```bash
function foo {
    local value=$1  # 函数局部变量,赋值采用第一个参数值传递
    local -n ref=$2 # 函数局部变量,赋值采用第二个参数引用传递,-n表示引用
    g_value="hello" # 函数内部可以定义全局变量
}
echo "$g_value" # 可以访问函数内部定义的全局变量
local whats_this # 错误,不应在函数体外部使用local关键字
```
#### 函数体外部的局部变量
使用`()`包裹的子`shell`块作用域
```bash
(
    x="只在()块作用域内有效"
    echo "子shell内部: $x"
)
echo "外面看不见: $x" # 输出为空
```
## 变量类型
基本的数据类型
特殊的数据结构
### 数组
```bash
$ mytest=(one two three four five)
$ echo $mytest
one
$ echo ${mytest[2]}
three
$ echo ${mutest[*]}
one two three four five
$ mytest[2]=seven
$ echo ${mytest[*]}
one two seven four five
$ unset mytest[2]
$ echo ${mytest[*]}
one two four five
$ echo ${mytest[2]}

$ echo ${mytest[3]}
four
$ unset mytest
$ echo ${mytest[*]}

```
`(values...)`

`[index]`

`element& array::operator[](size_t index)`

`[*]`

`array array::operator[](placeholder _)`

`unset`

`unset variable`

`variable= `
## 引用表达式结果
```bash
`variable`
$variable
${variable}
"[...]$variable[...]"
"[...]${variable}[...]"
$(function_name args...)
```
## 逻辑运算
### 逻辑表达式
逻辑计算表达式可以如下的方式包裹起来求值.
```bash
condition
[ condition ]   # 老式逻辑表达式
[[ condition ]] # 新式逻辑表达式,提供了针对字符串比较的高级特性
```
#### test命令和单方括号
`[]`实际上是`test`命令的简写语法糖.
```bash
test condition
```
如果不写`condition`语句,默认返回非零退出状态码`false`
```bash
if test condition
then
    commands
fi
```
可以简写为
```bash
if [ condition ]
then
    commands
fi
```
### test命令下的数值比较
```bash
n1 -eq n2 # n1 == n2, -eq <=> equal
n1 -ge n2 # n1 > n2, -ge <=> greater
n1 -gt n2 # n1 >= n2, -gt <=> greater than
n1 -le n2 # n1 < n2, -le <=> less
n1 -lt n2 # n1 <= n2, -lt <=> less than
n1 -ne n2 # n1 != n2, -ne <=> not equal
```
### test命令下的字符串比较
```bash
str1 = str2 # str1 == str2
str1 != str2
str1 \< str2 # str1 < str2, 使用\转义<,避免<被识别为io重定义运算符<
str1 \> str2 # str1 > str2, 使用\转义>,避免>被识别为io重定义运算符>
-n str1 # str1.size() != 0
-z str1 # str1.size() == 0
```
在 Bash 中，**`=` 和 `==` 都可以用于字符串比较**，但具体用哪个**完全取决于你使用的测试结构**（`[ ]` 还是 `[[ ]]`），而且存在一个**关于模式匹配的致命细节**必须注意。
#### 1. 在 `[ ]`（传统 test 命令）中
- **POSIX 标准要求**：必须使用 **`=`**。
- **`==` 能否用？**：Bash 的 `[ ]` 内建命令**支持** `==` 作为扩展，但这不是 POSIX 标准。在某些极简的 sh 环境中（如 `dash`）会报错。
- **最佳实践**：为了兼容性，在 `[ ]` 中请**坚持使用 `=`**。
```bash
# 正确写法（推荐）
if [ "$str1" = "$str2" ]; then
    echo "相等"
fi

# 虽然在 Bash 中也能运行，但不推荐
if [ "$str1" == "$str2" ]; then
    echo "相等"  # 在 bash 下有效，但在 sh 下可能报错
fi
```
#### 2. 在 `[[ ]]`（增强型测试，Bash/Ksh/Zsh 特有）中
- **`=` 和 `==` 功能完全等价**，没有任何区别。
- **推荐写法**：为了代码可读性（一眼看出是字符串比较），大多数 Bash 程序员习惯使用 **`==`**。
```bash
# 两者完全等价
if [[ $str1 = $str2 ]]; then echo "相等"; fi
if [[ $str1 == $str2 ]]; then echo "相等"; fi
```
#### 3. ⚠️ 最大的坑：`==` 右边的“模式匹配”陷阱
当你使用 `[[ ]]` 时，**右边的字符串如果没有加双引号，它会被当作“通配符模式（Pattern）”进行匹配，而不是纯粹的字符串比较！**

| 写法 | 实际行为 | 结果 |
| :--- | :--- | :--- |
| `[[ "$str" == "abc*" ]]` | **字符串比较**（因为右边的 `abc*` 加了引号） | 检查是否完全等于字面量 `"abc*"` |
| `[[ $str == abc* ]]` | **模式匹配**（右边没加引号） | 检查 `$str` 是否以 `abc` **开头** |
| `[[ $str == *abc* ]]` | **模式匹配** | 检查 `$str` 是否**包含** `abc` |
| `[ "$str" == abc* ]` | **报错或行为诡异** | 老式 `[ ]` 不支持模式匹配，会解析失败 |

**实战翻车示例：**
```bash
str="hello world"

# 意图：检查是否等于 "hello*"（字面量）
if [[ $str == "hello*" ]]; then
    echo "匹配1"  # 不会执行（因为字符串不相等）
fi

# 意图：检查是否以 hello 开头（忘加引号）
if [[ $str == hello* ]]; then
    echo "匹配2"  # 会执行！（因为模式匹配成功）
fi
```
#### 4. 终极建议（抄作业版）
1. **首选组合**：**`[[ ]]` + `==` + 右侧变量加双引号**（最清晰、最安全）
   ```bash
   if [[ "$str1" == "$str2" ]]; then
       echo "严格字符串相等"
   fi
   ```

2. **如果需要做通配符匹配**：**去掉右侧的引号**（特意为之）
   ```bash
   if [[ "$str" == *error* ]]; then
       echo "包含 error 子串"
   fi
   ```

3. **如果脚本需要兼容 POSIX（不能在 `sh` 下用 `[[ ]]`）**：必须用 `[ ]` 和 **`=`**，并且所有变量**必须加双引号**。
   ```bash
   if [ "$str1" = "$str2" ]; then
       echo "POSIX 兼容写法"
   fi
   ```
#### 一句话总结

| 测试结构 | 推荐用什么 | 是否支持 `==` | 核心警告 |
| :--- | :--- | :--- | :--- |
| **`[ ]`**（兼容模式） | **`=`** | 支持（但不标准） | 变量必须加双引号，否则空变量会语法错误 |
| **`[[ ]]`**（Bash 原生） | **`==`**（可读性） | 完全支持 | **右侧不加引号时是通配符匹配，而非字符串比较！** |

**最保险的通用写法（适用于任何场景）**：  
`if [ "$var1" = "$var2" ]; then ...`（传统但绝对安全）  
或  
`if [[ "$var1" == "$var2" ]]; then ...`（现代 Bash 首选）
### test命令下的路径比较
```bash
-e path # 检查path是否存在, -e <=> exist
-d path # 检查path是否存在并指向一个目录, -d <=> directory
-f path # 检查path是否存在并指向一个文件, -f <=> file

-r path # 检查path是否存在并可读, -r <=> read
-w path # 检查path是否存在并可写, -w <=> write
-x path # 检查path是否存在并可执行, -x <=> exec

-s path # 检查path是否存在并非空

-O path # 检查path是否存在并属当前用户所有
-G path # 检查path是否存在并且默认组与当前用户相同

path1 -nt path2 # 检查path1是否比path2新, -nt <=> new than
path1 -ot path2 # 检查path1是否比path2旧, -ot <=> old than
```
#### 双方括号的高级特性
```bash
if [[ $USER == r* ]]
then
    echo "Hello $USER"
else
    echo "Sorry, I do not know you"
fi
```
上述代码使用了`==`来匹配正则表达式字符串`r*`,
注意:`r*`没有被双引号`""`包裹

在`[[ ]]`中如果字符串没有被双引号`""`包裹,视为一个正则表达式,不视为常规字符串.
#### 逻辑表达式的组合语句
```bash
condition # 定义一个逻辑表达式,推荐,因为大道至简
[ condition ] # 定义一个逻辑表达式,不推荐,使用()需要转义为\(\)
[[ condition ]] # 定义一个逻辑表达式,推荐,支持直接使用()
condition1 && condition2 # 逻辑与 AND
condition1 || condition2 # 逻辑或 OR
! condition # 逻辑非 NOT, 注意 ! 运算符前后都要有空格
( condition1 ) && condition2 # 使用()改变逻辑运算的优先级
```
逻辑运算符的优先级:`!`>`&&`>`||`.

看一个实际的例子:
```bash
if [[ ! ($num -eq 50) && ( $num -lt 100 || $num -gt 0) ]] ; then
    echo "$num"
fi
```
### 数学计算表达式
数学计算表达式需要使用`(())`包裹起来求值.
```bash
(( expression ))
```
下面列举常见的数学运算符
```bash
val++ # return val; val+=1;
val-- # return val; val-=1;
++val # val+=1; return val;
--val # val-=1; return val;
**    # x**y <=> x^y, 表示x的y次方
!     # not
&&    # and
||    # or
~     # bit not
&     # bit and
|     # bit or
<<    # bit <<
>>    # bit >>
```
## 结构化语句

### if
```bash
if command
then
    commands
fi
```

```bash
if command ; then
    commands
fi
```
### else
```bash
if command
then
    commands
else
    commands
fi
```

```bash
if command ; then
    commands
else
    commands
fi
```
### elif
`elif`是`else if`的语法糖.

```bash
if command
then
    commands
else
    if command
    then
        commands
    fi
fi
```
可以简化为
```bash
if command
then
    commands
elif command
then
    commands
fi
```
或
```bash
if command ; then
    commands
elif command ; then
    commands
fi
```
### do
### loop
### while
### for
### case
```bash
case variable in
pattern1 | pattern2) command1;;
pattern3) command2;;
*) default commands;;
esac
```
上述的语法有个特点:开头是`case`,结尾是`esac`,正好是`case`颠倒过来.

其中可以使用`|`在一行中来组合匹配多个模式.
```bash
if [ $USER = "rich" ]
then
    echo "Welcome $USER"
    echo "Please enjoy your visit"
elif [ $USER = "barbara" ]
then
    echo "Welcome $USER"
    echo "Please enjoy your visit"
elif [ $USER = "testing" ]
then
    echo "Special testing account"
elif [ $USER = "jessica" ]
then
    echo "Do not forget to logout when you're done"
else
    echo "Sorry, you are not allowed here"
fi
```
上面这一段示例代码可以使用如下的代码段代替.
```bash
case $USER in
rich | barbara)
    echo "Welcome $USER"
    echo "Please enjoy your visit";;
testing)
    echo "Special testing account";;
jessica)
    echo "Do not forget to logout when you're done";;
*)
    echo "Sorry, you are not allowed here";;
esac
```
### function
#### 函数定义
```bash
function name {
    commands
}
```
```bash
name() {
    commands
}
```
#### 函数返回值
##### echo 返回
```bash
function foo {
    local array
    array=(1 2 3 4 5)
    echo ${array[*]}
}

new_array=($(foo))
```
##### return 返回
`return [n]`

`n`是取值范围`0~255`的整数错误码.
```bash
function main {
    return 0
}
new_array=$? # 0
```
使用`$?`来获取最后一次调用的函数的错误码返回值.
#### 函数传递参数
##### 执行函数的方式
`function_name`

`function_name args...`
##### 获取传入参数的个数
使用`$#`来得到传入的参数的个数
```bash
function main {
    if [ $# -eq 2 ]
    then
        return -1
    fi
}
```
## 引用其他脚本文件
### source 或 `.`
## 输入输出重定向与管道
### `<`
### `>`
### `<<`
### `>>`
### 内联输入重定向
```bash
<< EOF
...
EOF
```
### 管道`|`
