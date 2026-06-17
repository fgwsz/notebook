# 1. 添加包含 Emacs 最新版构建 的 PPA
sudo add-apt-repository ppa:ubuntuhandbook1/emacs
# 按 Enter 确认添加

# 2. 更新软件包列表
sudo apt update

# 3. 升级/安装 Emacs(这一步可能会弹出 Postfix 配置界面)
sudo apt install emacs emacs-common

# 出现 Postfix 配置界面,请:
#   - 用数字键选择 "Local only"(对应数字 5), 然后回车
#   - 然后提示输入 System mail name, 这里输入主机名称, 然后回车

# 4. 验证版本
emacs --version
