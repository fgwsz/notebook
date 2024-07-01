# Ubuntu学习笔记
## 下载
进入官网下载页:<https://cn.ubuntu.com/download>  
点击`下载Ubuntu桌面版`按钮  
![](data/20240516094331.png 
进入后向下翻,找到`Ubuntu xx.yy.z LTS`  
点击`其他下载`  
![](data/20240516094453.png)  
进入后向下翻,找到`BitTorrent`  
点击`Ubuntu xx.yy.z LTS`栏下的`Ubuntu 桌面版(64位)`按钮  
此时会下载`ubuntu-xx.yy.z-desktop-amd64.iso.torrent`  
![](data/20240516095053.png)
下载完成之后，使用BT下载工具打开这个`torrent`文件下载即可  
### 选择其他下载的原因
如果点击`下载xx.yy.z`按钮会开始下载  
但Chinese国情原因,下载速度会很慢(`kb/s`级别 
而且如果下载过程中一旦出现了中断,会造成此次下载失败
## 安装
启动`Ubuntu`系统  
选中第一项`Try or Install Ubuntu`并回车  
![](data/20240516152406.png)  
### 语言
进入`install`界面后  
在左侧的语言栏选择系统语言,这里我选择的是`English`  
然后点击右侧的`Install Ubuntu`按钮  
![](data/20240516152557.png)  
### 键盘布局
进入`Keyboard layout`界面  
选择键盘布局  
我的选择都是`English(US)`  
然后点击`Continue`按钮  
![](data/20240516152928.png)  
### 安装模式
进入`Updates and other software`界面选择安装模式  
有两个选项:`Normal installation`/`Minimal installation`  
在`Normal installation`中，将安装所有 GUI 相关的应用程序  
在`Minimal installation`中只会安装基本的应用程序  
我的选择是`Normal installation`  
注意到`Other options`选项中还有2个选项  
当需要安装所有更新和第三方图形软件和`wifi`驱动程序和额外的媒体格式时  
可以勾选这两个选项,否则保持它们为未勾选状态  
最后,点击右下角的`Continue`按钮  
![](data/20240516153417.png)  
### 安装类型
进入`Installation type`界面选择安装类型  
勾选`Something else`  
点击右下角的`Continue`按钮  
![](data/20240516154146.png)  
### 磁盘分区
#### 新建一个磁盘分区并设置
进入`Installation type`磁盘分区窗口  
右下角的`New Partition Table`按钮用于创建一个新的磁盘分区  
![](data/20240516160631.png)  
点击`Continue`按钮,创建一个新的磁盘分区`free space`  
![](data/20240516160929.png)  
选中刚刚创建的磁盘分区`free space`  
然后点击`+`按钮即可对此分区进行设置  
![](data/20240516161230.png)  
#### 磁盘分区配置
给出一个案例来进行参考  
首先明确一下我的系统可用磁盘空间大概是`200GB`  
`/boot`  2GB  
`/home`  98GB  
`/`      98GB  
`/swap`  2GB  
1. `/boot`  
![](data/20240516162202.png)  
2. `/home`  
![](data/20240516162510.png)  
3. `/`  
![](data/20240516162644.png)  
4. `/swap`  
![](data/20240516162853.png)  
配置完成后,点击`Install Now`按钮开始安装  
![](data/20240516163107.png)  
弹出如下提示  
![](data/20240516163420.png)  
于是重新增加一个`EFI`分区(`(100,250MB]`MB,设置为500MB有备无患)  
![](data/20240516163648.png)  
配置完成后,点击`Install Now`按钮开始安装  
弹出如下提示  
![](data/20240516164101.png)  
于是重新增加一个`BIOS Boot`分区(`>=1MB`)  
![](data/20240516164309.png)  
配置完成后,点击`Install Now`按钮开始安装  
![](data/20240516164530.png)  
点击`Continue`按钮开始安装  
![](data/20240516164600.png)  
### 选择时区
进入`Where are you?`界面  
选择东8区的`Shanghai`  
点击`Continue`按钮  
![](data/20240516164743.png)  
### 账号密码
进入`Who are you?`界面  
输入如下信息  
`Your name`:名字  
`Your computer's name`:电脑名称  
`Pick a username`:普通用户名称(必须全部使用小写字母)  
`password`:密码  
勾选`Require my password to log in`按钮  
点击`Continue`按钮开始安装  
![](data/20240516165121.png)  
至此等待系统安装完成即可  
![](data/20240516170558.png)  
点击`Restart Now`按钮重启系统  
## 使用
### 打开终端
桌面右键单击  
点击`Open in Terminal`按钮  
![](data/20240516220107.png)  
此时终端已打开  
![](data/20240516220157.png)  
### 重启
点击右上角菜单栏  
点击`Power Off/Log Out`按钮  
点击`Restart`按钮  
![](data/20240516221541.png)  
### 安装中文输入法
点击右上角的`Settings`选项  
![](data/20240516214126.png)  
向下翻找到`Region & Language`选项卡  
点击右侧的`Manage Installed Languages`按钮  
![](data/20240516214333.png)  
点击`Install/Remove Languages`按钮  
![](data/20240516214628.png)  
勾选`Chinese(simplified)`选项  
点击`Apply`按钮  
![](data/20240516214726.png)  
`Language for menus and windows:`栏下出现`汉语(中国)`字样  
设置`Keyboard input method system:`栏为`IBus`  
点击`Close`按钮  
![](data/20240516214929.png)  
点击`Keyboard`选项卡  
点击`Input Sources`栏下`+`按钮  
![](data/20240516215256.png)  
点击`Chinese`按钮  
![](data/20240516215445.png)  
点击`Chinese(intelligent pinyin)`按钮  
点击`Add`按钮  
![](data/20240516215554.png)  
此时`Input Sources`栏下出现`Chinese(intellient pinyin)`  
点击右侧的按钮  
点击`Move up`按钮将中文输入法置顶  
![](data/20240516215758.png)  
打开终端,输入如下命令  
```bash
ibus-setup
```
此命令的作用:打开`ibus`管理页面  
点击`Input Method`选项卡下的`Add`按钮  
![](data/20240516220504.png)  
点击`Chinese`按钮  
![](data/20240516220615.png)  
点击`Intelligent Pinyin`按钮  
点击`Add`按钮  
![](data/20240516220712.png)  
切换到`General`选项卡下  
点击`Next input method:`右侧的`...`按钮  
![](data/20240516220957.png)  
#### 设置切换中英文输入法的快捷键为`Ctrl+Space`
> 注意:这是切换中文/英文2个输入法的快捷键  
> 不是中文输入法切换中/英输入的快捷键  
> 中文输入法切换中/英输入的快捷键是`shift`键  

取消勾选`Super`  
勾选`Control`  
点击`Apply`按钮  
点击`Close`按钮  
![](data/20240516221154.png)  
点击`Close`按钮  
![](data/20240516221343.png)  
重启系统  
开机后发现右上角菜单栏出现`中`字样按钮  
至此中文输入法安装成功  
![](data/20240516221810.png)  
安装另一个超好用的ibus输入法:Rime
```bash
sudo apt install ibus-rime
```
上述指令执行完之后输入
```bash
ibus-setup
```
点击`Input Method`标签栏下的`Add`按钮,  
添加`Chinese`下的`Rime`  
其他的设置和上述一开始的`Intelligent Pinyin`输入法一样  
可以在系统设置的`Keyboard`标签栏下添加新的中文输入法  
然后管理输入法的优先级顺序  
`Rime`默认的中文输出方式是中文繁体,在打字弹出输入框的情况下  
按`F4`可以切换到`明月拼音 简化字`即可输出中文简体  
### 安装/配置`Git`
#### 安装`Git`
```bash
sudo apt-get install git
git --version
```
#### 配置`Github`账号信息
```bash
git config --global user.name "your name"
git config --global user.email youremail@example.com
git config --list
```
#### 生成`ssh`密钥
```bash
ssh-keygen -t rsa -C "youremail@example.com"
gedit ~/.ssh/id_rsa.pub
```
把`~/.ssh/id_rsa.pub`里的全部内容复制到剪切板  
#### 连接到`github`
登录`github`账号  
点击`Settings`按钮  
![](data/20240516225837.png)  
切换到`SSH and GPG keys`栏  
点击`New SSH key`按钮  
![](data/20240516225951.png)  
`Title`输入标题  
`Key type`选择`Authentication Key`  
`Key`栏粘贴`~/.ssh/id_rsa.pub`里的全部内容  
![](data/20240516230339.png)  
至此添加`ssh`到`github`成功  
![](data/20240516230459.png)  
测试一下是否可以`ssh`到`github`  
```bash
ssh -T git@github.com
```
如下图所示,证明配置成功  
![](data/20240516231223.png)  
### 安装`Vim 9`
```bash
sudo add-apt-repository ppa:jonathonf/vim
sudo apt update
sudo apt install vim
vim --version
```
### 安装`Vim`
1.方式一
打开`Ubuntu Software`  
![](data/20240517112556.png)  
搜索`GVim`然后点进去点击`install`按钮即可  
![](data/20240517112741.png)  
2.方式二
```bash
sudo apt install vim
sudo apt install vim-gtk3
```
### 删除无用的应用图标
系统图标:`/usr/share/applications`  
用户应用:`~/.local/share/applications`  
进入上述文件夹之后使用`grep`/`vim`的高亮查找功能锁定对应的文件,删除即可.  
### AppImage包如何使用
AppImage包本身是一个可执行文件  
但是需要先安装FUSE  
然后赋予可执行权限  
最后执行即可  
```bash
sudo apt-get install fuse
chmod +x ./xxx.AppImage
./xxx.AppImage
```
### 修改gnome显示样式
```bash
sudo apt install gnome-tweaks
gnome-tweaks
```
### 配置ibus-rime输入法
#### 设置横排显示候选项
```bash
gvim ~/.config/ibus/rime/build/ibus_rime.yaml
```
修改该文件的如下内容(#标注的)  
```yaml
style:
  cursor_type: insert
  horizontal: true #横排显示候选项
  inline_preedit: true
  preedit_style: composition
```
#### 使用shift切换的时候清除已输入字符
```bash
gvim ~/.config/ibus/rime/build/default.yaml
```
修改该文件的如下内容(#标注的)  
```yaml
ascii_composer:
  good_old_caps_lock: true
  switch_key:
    Caps_Lock: clear
    Control_L: noop
    Control_R: noop
    Eisu_toggle: clear
    Shift_L: clear #inline_ascii
    Shift_R: clear #commit_text
```
#### 重新配置ibus-rime
鼠标左键单击右上角的语言栏`ibus`图标  
鼠标左键单击选中`Chinese(Rime)`  
鼠标左键单击选中`部署`  
等待一会儿会显示提示`Rime is ready`  
至此重新配置ibus-rime成功  
### 使用ripgrep替换grep
安装  
```bash
sudo apt install ripgrep
rg --version
```
替换:在`~/.bashrc`中输入如下内容  
```bash
alias grep='rg'
```
### 更换DNS服务器
```bash
sudo gvim /etc/systemd/resolved.conf
```
添加如下内容并保存:  
```txt
DNS=8.8.8.8 114.114.114.114
FallbackDNS=8.8.8.8
```
然后依次执行如下命令:  
```bash
sudo systemctl restart systemd-resolved
sudo systemctl enable systemd-resolved
sudo mv /etc/resolv.conf /etc/resolv.conf.bak
sudo ln -s /run/systemd/resolve/resolv.conf /etc/
```
再查看/etc/resolv.conf文件就可以看到新的dns信息已经写入其中了。  
```bash
sudo gvim /etc/resolv.conf
```
`etc/resolv.conf`文件发现如下内容:  
```txt
nameserver 8.8.8.8
nameserver 114.114.114.114
```
此时更换DNS服务器完成  
### 修复Grub Windows11引导项
```bash
sudo gvim /etc/default/grub
```
设置默认启动项为第一个  
设置显示菜单  
设置停留时间为10秒  
```txt
GRUB_DEFAULT=0
GRUB_TIMEOUT_STYLE=menu
GRUB_TIMEOUT=10
```
保存上述更改，执行如下指令  
```bash
sudo update-grub
```
重启计算机即可解决
### 修复Ubuntu启动显示`SGX disable by BIOS`问题
```bash
sudo gvim /etc/default/grub
```
设置不使用`SGX`  
```txt
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nosgx"
```
保存上述更改，执行如下指令  
```bash
sudo update-grub
```
重启计算机即可解决
