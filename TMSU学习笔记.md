# TMSU 学习笔记

## 一、概述

TMSU（Tag My Stuff Unix）是一款文件标签管理工具。它的核心思想是：**用标签来组织文件，而非仅依赖传统的文件夹层级**。

TMSU 提供两个主要功能：

1. **命令行工具**：用于给文件打标签、查询文件
2. **虚拟文件系统（VFS）** ：基于 FUSE 实现，可将标签视图挂载为一个目录，让你在任何应用程序（包括文件管理器）中通过标签浏览文件

**最重要的原则：TMSU 不会以任何方式修改你的原始文件**。标签信息全部存储在一个独立的 SQLite 数据库中，文件本身在磁盘上保持不变。

## 二、安装

### 2.1 通过包管理器安装（推荐）

**Ubuntu/Debian**（使用官方 PPA）：

```bash
sudo add-apt-repository ppa:tmsu/ppa
sudo apt update
sudo apt install tmsu
```

**Arch Linux**（AUR）：

```bash
yay -S tmsu
# 或
paru -S tmsu
```

**Nix/NixOS**：

```bash
nix-env -iA nixos.tmsu
```

**macOS**（Homebrew）：

```bash
brew install tmsu
```

### 2.2 安装预编译二进制

从 [GitHub Releases](https://github.com/oniony/TMSU/releases) 下载对应平台的二进制文件：

```bash
# 下载后复制到系统路径
sudo cp tmsu /usr/bin/
```

> **依赖要求**：TMSU 需要 **FUSE** 和 **SQLite3**。通过包管理器安装会自动处理这些依赖。

### 2.3 从源码编译

```bash
git clone https://github.com/oniony/TMSU.git
cd TMSU
make
sudo make install
```

## 三、初始化数据库

在使用 TMSU 之前，需要在你想管理文件的目录下初始化一个数据库：

```bash
cd /path/to/your/files
tmsu init
```

执行后会在当前目录下创建一个 `.tmsu/` 隐藏目录，其中的 `db` 文件就是 SQLite 数据库。

> **注意**：TMSU 会自动使用当前目录（或其父目录）下的数据库。这意味着你可以在项目的根目录初始化一次，然后在任何子目录中使用 TMSU 命令。

## 四、打标签

### 4.1 给单个文件打标签

```bash
tmsu tag <文件名> <标签1> [标签2] ...
```

示例：

```bash
tmsu tag summer.mp3 music big-jazz mp3
```

执行后会看到类似输出：
```
tmsu: New tag 'music'
tmsu: New tag 'big-jazz'
tmsu: New tag 'mp3'
```

### 4.2 给多个文件批量打标签

使用 `--tags` 选项，将标签列表放在前面，文件列表放在后面：

```bash
tmsu tag --tags "music mp3" *.mp3
```

### 4.3 带值的标签

标签可以附带值（字符串或数字），便于后续按范围筛选：

```bash
tmsu tag spring.mp3 year=2003
tmsu tag summer.mp3 year=2008
tmsu tag winter.mp3 year=2010
```

### 4.4 移除标签

使用 `untag` 命令移除文件上的指定标签：

```bash
tmsu untag summer.mp3 big-jazz
```

## 五、查询标签

### 5.1 列出所有标签

```bash
tmsu tags
```

### 5.2 查看某个文件的标签

```bash
tmsu tags summer.mp3
```

输出示例：
```
big-jazz mp3 music year=2008
```

### 5.3 查看多个文件的标签

```bash
tmsu tags *.mp3
```

输出示例：
```
spring.mp3: folk mp3 music year=2003
summer.mp3: big-jazz mp3 music year=2008
winter.mp3: mp3 music year=2010
```

## 六、查找文件

### 6.1 基础查询

使用 `files` 命令通过标签查找文件。多个标签之间默认是 **AND**（且）关系：

```bash
tmsu files mp3
tmsu files mp3 big-jazz        # 同时包含 mp3 和 big-jazz
tmsu files "mp3 and big-jazz"  # 同上，更明确的写法
```

### 6.2 逻辑运算查询

TMSU 支持 `and`、`or`、`not` 运算符及括号：

```bash
tmsu files "(mp3 or flac) and not big-jazz"
```

### 6.3 按标签值筛选

```bash
tmsu files "year = 2010"
tmsu files "year >= 2000 and year < 2010"
```

## 七、虚拟文件系统（VFS）

这是 TMSU 最强大的功能。通过 FUSE 将一个目录挂载为标签视图，让你可以在任何图形化应用程序（如文件管理器、视频播放器）中通过标签浏览文件。

### 7.1 挂载虚拟文件系统

首先创建一个空的挂载点目录：

```bash
mkdir ~/tmsu-mount
```

然后挂载：

```bash
tmsu mount ~/tmsu-mount
```

### 7.2 浏览标签视图

挂载后，进入挂载点目录，你会看到两个子目录：`tags/` 和 `queries/`。

**`tags/` 目录**：所有标签都显示为文件夹。

```bash
ls ~/tmsu-mount/tags
big-jazz  mp3  music
```

进入某个标签文件夹，就能看到所有被打上该标签的文件：

```bash
ls ~/tmsu-mount/tags/music
```

**组合标签浏览**：在标签目录下还可以继续进入子标签，实现“且”筛选：

```bash
ls ~/tmsu-mount/tags/music/big-jazz/
```

这里显示的是同时拥有 `music` 和 `big-jazz` 两个标签的文件。

**`queries/` 目录**：可以在这里直接使用查询表达式作为路径，TMSU 会自动生成对应的文件列表。例如：

```bash
ls ~/tmsu-mount/queries/"mp3 and not folk"/
```

> 不需要手动创建这个目录，访问时 TMSU 会自动生成。

### 7.3 使用虚拟文件系统中的文件

虚拟文件系统中的文件**不是真实的副本或符号链接**，而是由 FUSE 动态生成的虚拟视图。但你可以像操作普通文件一样：

- 在文件管理器中双击打开
- 拖拽到应用程序中
- 用播放器播放视频
- 用编辑器打开文档

**原始文件本身不会被修改**。

### 7.4 卸载虚拟文件系统

使用完毕后卸载：

```bash
tmsu unmount ~/tmsu-mount
```

或使用系统命令：

```bash
fusermount -u ~/tmsu-mount
```

## 八、标签管理命令

| 命令 | 用途 | 示例 |
| :--- | :--- | :--- |
| `tag` | 添加标签 | `tmsu tag file.mp3 music` |
| `untag` | 移除标签 | `tmsu untag file.mp3 music` |
| `tags` | 查看标签 | `tmsu tags file.mp3` |
| `files` | 按标签查找文件 | `tmsu files music and not jazz` |
| `rename` | 重命名标签 | `tmsu rename old_tag new_tag` |
| `merge` | 合并标签 | `tmsu merge old_tag new_tag` |
| `delete` | 删除标签 | `tmsu delete tag_name` |
| `status` | 查看文件标签状态 | `tmsu status` |
| `repair` | 修复数据库中失效的路径 | `tmsu repair` |

### 8.1 合并标签示例

如果你有两个相似的标签想合并：

```bash
tmsu merge old-tag new-tag
```

这会将所有带有 `old-tag` 标签的文件改为带有 `new-tag`，然后删除 `old-tag`。

### 8.2 标签暗示（Imply）

可以设置当添加某个标签时自动添加另一个标签：

```bash
tmsu imply work project
```

此后给任何文件添加 `work` 标签时，会自动同时添加 `project` 标签。

## 九、注意事项

1. **虚拟文件系统需要 FUSE 支持**：Linux 和 macOS 可用，Windows 上虚拟文件系统功能不可用。

2. **数据库是目录级别的**：每个目录（及其子目录）使用该目录下的 `.tmsu/db` 数据库。在不同目录间切换时，TMSU 会自动使用对应的数据库。

3. **文件移动/重命名后路径会失效**：如果文件被移动或重命名，数据库中的路径记录会失效，需要使用 `tmsu repair` 命令修复。

4. **备份建议**：标签数据存储在 `.tmsu/` 目录中，请定期备份该目录。

5. **挂载点要求为空目录**：挂载虚拟文件系统前，请确保目标目录为空。

## 十、快速参考

```bash
# 初始化
tmsu init

# 打标签
tmsu tag file.mp3 tag1 tag2
tmsu tag --tags "tag1 tag2" *.mp3
tmsu tag file.mp3 year=2024

# 查标签
tmsu tags
tmsu tags file.mp3

# 查文件
tmsu files tag1
tmsu files "tag1 and tag2"
tmsu files "(tag1 or tag2) and not tag3"
tmsu files "year >= 2020"

# 挂载虚拟文件系统
mkdir ~/tmsu-mount
tmsu mount ~/tmsu-mount

# 卸载
tmsu unmount ~/tmsu-mount

# 帮助
tmsu help
tmsu help tag
```

## 十一、总结

TMSU 是一款**不修改原始文件**的文件标签管理工具，通过命令行打标签 + FUSE 虚拟文件系统浏览，打破了传统文件夹层级对文件组织的限制。

- 适合需要**多维度、跨目录**管理文件的场景
- 特别适合**视频剪辑师**等需要保持原始文件路径不变的用户
- 学习成本略高，但一旦掌握，文件管理效率将大幅提升

更多信息请参考 [TMSU 官方 Wiki](https://github.com/oniony/TMSU/wiki)。
