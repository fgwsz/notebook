# Bash Shell 脚本编程笔记（完整初稿）

---

## 目录

1. [脚本基础](#1-脚本基础)
2. [变量与作用域](#2-变量与作用域)
3. [数据类型](#3-数据类型)
4. [测试与条件判断](#4-测试与条件判断)
5. [逻辑运算与优先级](#5-逻辑运算与优先级)
6. [数学计算](#6-数学计算)
7. [流程控制](#7-流程控制)
8. [函数](#8-函数)
9. [输入输出重定向与管道](#9-输入输出重定向与管道)
10. [引用其他脚本文件](#10-引用其他脚本文件)
11. [调试与错误处理](#11-调试与错误处理)

---

## 1. 脚本基础

### 1.1 创建脚本文件
- 使用任意文本编辑器（如 `vim`, `nano`）创建以 `.sh` 为后缀的文件，如 `myscript.sh`。
- 文件第一行指定解释器：`#!/bin/bash`（称为 shebang）。

### 1.2 赋予可执行权限
```bash
chmod +x myscript.sh
```
之后可通过 `./myscript.sh` 直接运行。

### 1.3 脚本执行方式
- `./myscript.sh`（需可执行权限）
- `bash myscript.sh`（无需可执行权限）
- `source myscript.sh` 或 `. myscript.sh`（在当前 Shell 环境中执行，不影响权限）

### 1.4 注释
- 单行注释：`# 这是注释`
- 没有多行注释，可以用 `: << 'END' ... END` 模拟，但不常用。

---

## 2. 变量与作用域

### 2.1 变量命名规则
- 由字母、数字、下划线组成，不能以数字开头。
- 区分大小写。
- **无长度限制**（实际受内存限制）。
- 建议使用有意义的名称，如 `user_name`，避免使用关键字（如 `if`, `then` 等）。

### 2.2 变量赋值
- **等号两侧不能有空格**。
```bash
var1=100          # 正确
var2="Hello World" # 包含空格需引号
var3='Single quotes' # 单引号保留原义
var4=$(date)      # 命令替换
var5=$((1+2))     # 算术扩展
```
- 变量默认类型为字符串，但可进行算术运算。

### 2.3 变量引用
```bash
echo $var1        # 简单引用
echo ${var1}      # 花括号有助于区分边界，如 ${var1}abc
echo "$var1"      # 双引号内会展开变量
echo '$var1'      # 单引号内原样输出
```
推荐始终使用双引号包裹变量引用，以防空值或特殊字符导致错误。

### 2.4 变量作用域

#### 2.4.1 全局变量
- 在脚本顶层（任何函数外部）声明的变量默认为**全局变量**，在整个脚本中可见。
- 在函数内部未使用 `local` 声明的变量也会修改全局变量（若存在同名）或创建全局变量。

#### 2.4.2 局部变量（函数内部）
- 使用 `local` 关键字声明，仅在该函数内有效。
- `local` **只能用于函数内部**，在函数外部使用会报错。
```bash
function myfunc {
    local local_var="I am local"
    global_var="I am global"   # 没有 local，默认为全局（若已存在则修改）
}
myfunc
echo "$global_var"   # 输出 "I am global"
echo "$local_var"    # 空，因为已销毁
```

#### 2.4.3 引用变量（nameref）
- 使用 `local -n` 或 `declare -n` 创建变量的别名，用于函数内部修改外部数组/变量。
- **要求 Bash 4.3+**。
```bash
function modify_array {
    local -n arr=$1   # arr 是外部数组的别名
    arr[0]="changed"
}
my_array=(original)
modify_array my_array
echo "${my_array[0]}"   # 输出 "changed"
```
注意：调用时传递的是**变量名**（字符串），而非变量值。

#### 2.4.4 子 Shell 作用域
- 使用 `( )` 包裹的代码块会在子 Shell 中执行，其中定义的变量不影响父 Shell。
```bash
(
    x="only in subshell"
    echo "$x"   # 输出 "only in subshell"
)
echo "$x"       # 空（未定义）
```

#### 2.4.5 环境变量（导出变量）
- 使用 `export` 将变量标记为环境变量，会传递给子进程（如子 Shell 或外部命令）。
- 子进程修改自己的副本不会影响父进程。
```bash
export MY_ENV="hello"
bash -c 'echo $MY_ENV'   # 输出 "hello"
```

---

## 3. 数据类型

Bash 变量默认为**字符串**，但可以按需进行算术运算或数组操作。

### 3.1 整数
- 可使用 `declare -i` 声明为整数类型，后续赋值会自动进行算术求值。
```bash
declare -i num=10
num="5+3"        # num 变为 8
num="hello"      # 非数字转为 0
```

### 3.2 只读变量
- 使用 `readonly` 或 `declare -r` 声明，之后无法修改。
```bash
readonly PI=3.14159
PI=3.14          # 报错：readonly variable
```

### 3.3 数组（索引数组）

#### 3.3.1 定义与访问
```bash
arr=(one two three four five)        # 初始化
arr[0]="first"                       # 单独赋值
echo "${arr[2]}"                     # 输出 "three"
echo "${arr[*]}"                     # 所有元素作为一个单词（以 IFS 第一个字符分隔）
echo "${arr[@]}"                     # 所有元素作为独立单词（推荐用于循环）
```

#### 3.3.2 获取长度
```bash
echo "${#arr[@]}"   # 元素个数
echo "${#arr[2]}"   # 索引 2 元素的字符串长度
```

#### 3.3.3 获取所有索引
```bash
echo "${!arr[@]}"   # 输出所有索引，如 "0 1 2 3 4"
```

#### 3.3.4 修改与删除
```bash
arr[2]="seven"                     # 修改
unset arr[2]                       # 删除索引 2（索引不连续）
unset arr                          # 删除整个数组
```

#### 3.3.5 重新索引（使连续）
删除元素后索引可能不连续，可用以下方式重建：
```bash
arr=("${arr[@]}")   # 将现有元素重新赋给数组，索引从 0 开始连续
```

#### 3.3.6 数组切片
```bash
slice=("${arr[@]:1:2}")   # 从索引 1 开始取 2 个元素
```

### 3.4 关联数组（字典，Bash 4.0+）
需要先声明：`declare -A`
```bash
declare -A dict
dict["name"]="Alice"
dict["age"]=30
echo "${dict["name"]}"   # 输出 "Alice"
# 获取所有键
echo "${!dict[@]}"       # 输出 "name age"
# 获取所有值
echo "${dict[@]}"        # 输出 "Alice 30"
```

---

## 4. 测试与条件判断

### 4.1 `test` 命令与 `[ ]`
- `[ condition ]` 是 `test condition` 的简写。
- 条件为真时返回退出码 0，否则返回非 0。
- **注意**：`[` 是一个命令，其后必须有空格，且 `]` 前必须有空格。
- 变量建议**始终用双引号**包裹，以防空值或含空格导致错误。

#### 4.1.1 数值比较（`[ ]` 或 `test`）
| 运算符 | 含义 |
|--------|------|
| `n1 -eq n2` | n1 == n2 |
| `n1 -ne n2` | n1 != n2 |
| `n1 -gt n2` | n1 > n2 |
| `n1 -ge n2` | n1 >= n2 |
| `n1 -lt n2` | n1 < n2 |
| `n1 -le n2` | n1 <= n2 |

```bash
if [ "$num" -eq 10 ]; then
    echo "num 等于 10"
fi
```

#### 4.1.2 字符串比较（`[ ]` 内）
- **必须使用 `=`**（POSIX 标准），虽然 Bash 允许 `==`，但不推荐。
- 使用 `\>` 和 `\<` 进行字典序比较（需转义）。
| 运算符 | 含义 |
|--------|------|
| `str1 = str2` | 相等 |
| `str1 != str2` | 不等 |
| `str1 \< str2` | str1 < str2（字典序） |
| `str1 \> str2` | str1 > str2 |
| `-n str` | 字符串长度非 0 |
| `-z str` | 字符串长度为 0 |

```bash
if [ "$str1" = "$str2" ]; then
    echo "相等"
fi
```

#### 4.1.3 文件条件测试（`[ ]`）
| 运算符 | 含义 |
|--------|------|
| `-e path` | 存在 |
| `-f path` | 存在且为普通文件 |
| `-d path` | 存在且为目录 |
| `-r path` | 存在且可读 |
| `-w path` | 存在且可写 |
| `-x path` | 存在且可执行 |
| `-s path` | 存在且非空 |
| `-O path` | 存在且属当前用户 |
| `-G path` | 存在且组 ID 与当前用户相同 |
| `path1 -nt path2` | path1 比 path2 新（修改时间） |
| `path1 -ot path2` | path1 比 path2 旧 |

```bash
if [ -f "/etc/passwd" ]; then
    echo "passwd 文件存在"
fi
```

### 4.2 增强型测试 `[[ ]]`（Bash 特有）
- 支持更多操作符，**无需转义** `<`、`>`、`(`、`)` 等。
- 支持**模式匹配**（通配符）和**正则匹配**（`=~`）。
- 变量一般不需要加双引号（但若字符串可能包含空格，加引号更安全）。

#### 4.2.1 字符串比较
- 支持 `=` 和 `==`，推荐使用 `==` 提高可读性。
- **注意**：右侧若**不加引号**，则视为**通配符模式**，而非字面字符串。
```bash
[[ "$str1" == "$str2" ]]   # 严格字符串相等
[[ $str == abc* ]]         # 检查是否以 abc 开头（通配符模式）
```

#### 4.2.2 正则匹配（`=~`）
- 右侧为正则表达式（不加引号）。
```bash
if [[ "$str" =~ ^[0-9]+$ ]]; then
    echo "全是数字"
fi
```

#### 4.2.3 逻辑组合
- 支持 `&&`、`||`、`!`，以及括号 `( )` 改变优先级，无需转义。

---

## 5. 逻辑运算与优先级

### 5.1 逻辑表达式形式
- 任何命令都可作为条件（退出码 0 为真）。
- 测试表达式通常用 `[ ]` 或 `[[ ]]` 包裹。

### 5.2 逻辑运算符（命令级）
- `! condition`：逻辑非（注意 `!` 前后必须有空格）。
- `condition1 && condition2`：逻辑与（短路求值）。
- `condition1 || condition2`：逻辑或（短路求值）。

### 5.3 优先级（从高到低）
```
!   >   &&   >   ||
```
- 可使用 `( )` 或 `{ }` 改变运算顺序，但 `( )` 会启动子 Shell，`{ }` 不启动（需注意语法：`{ cmd1 && cmd2; }` 末尾必须有 `;` 或换行）。

### 5.4 在 `[[ ]]` 中的使用（推荐）
```bash
if [[ ! ($num -eq 50) && ( $num -lt 100 || $num -gt 0) ]]; then
    echo "$num"
fi
```
- `!` 作用于括号内整体。
- `&&` 优先级高于 `||`，但括号明确分组。

### 5.5 在 `[ ]` 中的组合（不推荐）
- 使用 `-a`（AND）和 `-o`（OR），但容易出错，且需转义括号 `\( \)`。
- 更好的做法是使用多个 `[ ]` 通过 Shell 的 `&&`/`||` 连接：
```bash
if [ condition1 ] && [ condition2 ]; then ...
```

---

## 6. 数学计算

### 6.1 算术扩展 `$(( ))`
- 用于计算并返回结果，可赋值给变量。
```bash
result=$(( 10 + 5 * 2 ))   # 20
echo $(( 2 ** 10 ))        # 1024（幂运算）
```

### 6.2 算术复合命令 `(( ))`
- 用于条件判断（计算结果非 0 为真）或执行算术赋值。
```bash
(( num = 10 + 5 ))        # 赋值
(( num++ ))               # 自增
if (( num > 10 )); then ...; fi
```

### 6.3 常见算术运算符
| 运算符 | 含义 |
|--------|------|
| `+ - * / %` | 加、减、乘、除、取模 |
| `**` | 幂运算 |
| `++ --` | 自增/自减（前/后） |
| `!` | 逻辑非（作用于整个表达式结果） |
| `&&` `\|\|` | 逻辑与、或（同样支持短路） |
| `&` `\|` `~` `^` | 位与、或、非、异或 |
| `<<` `>>` | 位左移、右移 |
| `=` `+=` `-=` 等 | 赋值运算 |

---

## 7. 流程控制

### 7.1 `if` 语句
```bash
if command; then
    commands
elif command; then
    commands
else
    commands
fi
```
- `command` 可以是任何命令或测试表达式。
- 分号 `;` 可放在 `if` 行末以省略换行。

### 7.2 `case` 语句
- 匹配模式支持通配符和 `|` 组合。
```bash
case variable in
    pattern1 | pattern2)
        commands;;
    pattern3)
        commands;;
    *)
        default commands;;
esac
```
- 每个分支结尾用双分号 `;;`，可以加 `;&`（继续执行下一个分支）或 `;;&`（测试下一个模式）。

### 7.3 循环

#### 7.3.1 `for` 循环（遍历列表）
```bash
for var in item1 item2 ...; do
    commands
done
```
- 可配合数组、命令替换等生成列表。
```bash
for i in {1..5}; do echo $i; done
for file in *.txt; do echo "$file"; done
for user in $(cut -d: -f1 /etc/passwd); do ...
```

#### 7.3.2 `for` 循环（类 C 风格）
```bash
for (( i=0; i<10; i++ )); do
    echo $i
done
```

#### 7.3.3 `while` 循环（条件为真时执行）
```bash
while condition; do
    commands
done
```

#### 7.3.4 `until` 循环（条件为假时执行）
```bash
until condition; do
    commands
done
```

#### 7.3.5 循环控制
- `break`：退出循环。
- `continue`：跳过本次剩余部分，进入下一次迭代。

---

## 8. 函数

### 8.1 定义函数
```bash
function name {
    commands
}
# 或
name() {
    commands
}
```

### 8.2 调用函数
```bash
name              # 无参数
name arg1 arg2    # 传递参数
```

### 8.3 参数访问
- 函数内部使用 `$1`、`$2` ... 访问位置参数。
- `$#`：参数个数。
- `$@`：所有参数（作为独立单词）。
- `$*`：所有参数（作为一个单词）。

```bash
function greet {
    echo "Hello, $1!"
}
greet "Alice"
```

### 8.4 返回值

#### 8.4.1 退出状态码（`return`）
- 只能返回 0~255 的整数，用于指示函数执行是否成功（0 成功，非 0 失败）。
- 调用后可通过 `$?` 获取。
```bash
function check_file {
    if [ -f "$1" ]; then
        return 0
    else
        return 1
    fi
}
check_file "file.txt"
if [ $? -eq 0 ]; then echo "存在"; fi
```
注意：`return -1` 会被解释为 255。

#### 8.4.2 返回数据（使用 `echo` / `printf`）
- 函数打印的结果可通过命令替换捕获。
```bash
function get_name {
    echo "Alice"
}
name=$(get_name)
echo "$name"
```
- 若返回数组，可打印各元素（用空格分隔），外部再用 `()` 重建，但注意元素含空格时需特殊处理。

#### 8.4.3 返回数组（使用引用传递）
```bash
function get_array {
    local -n arr=$1
    arr=(one two three)
}
myarray=()
get_array myarray
echo "${myarray[1]}"   # 输出 "two"
```

### 8.5 局部变量
- 使用 `local` 声明，避免污染全局。
```bash
function myfunc {
    local var="inside"
    echo "$var"
}
```

### 8.6 递归函数
- Bash 支持递归，但需注意递归深度限制（默认约 1000 级）。

---

## 9. 输入输出重定向与管道

### 9.1 重定向
| 符号 | 说明 |
|------|------|
| `>` | 覆盖写入文件（若文件存在则清空） |
| `>>` | 追加写入文件 |
| `<` | 从文件读取输入 |
| `2>` | 重定向标准错误 |
| `&>` | 同时重定向标准输出和错误（覆盖） |
| `2>&1` | 将错误重定向到标准输出流 |

```bash
ls -l > listing.txt          # 写入
ls -l >> listing.txt         # 追加
grep "error" < log.txt       # 从文件读取
command 2> error.log         # 仅错误信息
command &> all.log           # 所有输出
command > out.log 2>&1       # 将错误也指向 stdout（旧式写法）
```

### 9.2 内联输入重定向（Here Document）
- 用于向命令提供多行输入，以 `<<` 加分隔符开头，以单独一行出现分隔符结束。
```bash
cat << EOF
Hello
World
EOF
```
- 分隔符加引号（如 `<<"EOF"`）可禁用变量扩展和命令替换。

### 9.3 管道 `|`
- 将前一个命令的标准输出作为后一个命令的标准输入。
```bash
ls -l | grep "txt" | wc -l
```

### 9.4 命令替换 `$( )` 和反引号 `` ` ` ``
- 将命令输出替换为文本，推荐使用 `$( )`，因为它支持嵌套且可读性更好。
```bash
now=$(date)
files=$(ls)
```

---

## 10. 引用其他脚本文件

### 10.1 `source` 或 `.`（点命令）
- 在当前 Shell 环境中执行脚本，因此其中的变量、函数会影响当前环境。
```bash
source ./config.sh
. ./utils.sh    # 简写形式
```

### 10.2 相对路径与绝对路径
- 可提供相对或绝对路径。

---

## 11. 调试与错误处理

### 11.1 常用 `set` 选项
- `set -e`：遇到任何命令返回非 0 时立即退出脚本（错误即停）。
- `set -u`：使用未定义变量时报错（并退出，若结合 `-e`）。
- `set -x`：打印每个执行的命令（调试模式）。
- `set -o pipefail`：管道中任一命令失败则整个管道返回失败（常与 `-e` 配合）。
- 可组合使用：`set -euxo pipefail`（常用推荐）。

### 11.2 临时启用调试
```bash
# 在脚本中某一段开启
set -x
# 调试部分代码
set +x   # 关闭调试
```

### 11.3 捕获信号与错误
- 使用 `trap` 命令捕获信号或错误，执行清理操作。
```bash
cleanup() {
    rm -f /tmp/tempfile
}
trap cleanup EXIT   # 脚本退出时执行
trap 'echo "Error at line $LINENO"' ERR
```

### 11.4 检查命令是否存在
```bash
if command -v mycmd &>/dev/null; then
    echo "mycmd 存在"
else
    echo "未找到 mycmd"
fi
```

---

## 附录：常用快捷键与特殊变量

### 特殊变量
| 变量 | 含义 |
|------|------|
| `$0` | 脚本名称 |
| `$1..$9` | 位置参数 |
| `${10}` | 第 10 个及以上参数需花括号 |
| `$#` | 参数个数 |
| `$*` | 所有参数（作为一个字符串） |
| `$@` | 所有参数（作为独立单词） |
| `$?` | 上一条命令的退出码 |
| `$$` | 当前 Shell 进程 ID |
| `$!` | 最后一个后台进程的 ID |
| `$-` | 当前 Shell 选项 |

### 引号规则
- **双引号**：允许变量扩展、命令替换。
- **单引号**：保留所有字符原意，无任何扩展。
- **反引号**：命令替换（不推荐，用 `$( )` 替代）。

### 花括号扩展
```bash
echo {a,b,c}.txt        # 输出 a.txt b.txt c.txt
echo {1..10}            # 1 2 3 ... 10
```

---

## 结束语

本笔记涵盖了 Bash 脚本编程的核心知识，适用于入门到中级学习者。建议结合实际练习加深理解，同时注意脚本的可移植性（若需要兼容 `sh`，则避免使用 `[[ ]]`、关联数组等 Bash 特有特性）。编写脚本时，始终牢记变量加引号、使用 `set -euxo pipefail` 提升健壮性，并善用函数组织代码。

Happy scripting! 🚀
