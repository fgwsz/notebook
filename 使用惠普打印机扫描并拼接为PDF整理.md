# 使用惠普打印机扫描并拼接为 PDF 整理

## 1. 安装惠普扫描工具

```bash
sudo apt install hplip hplip-gui
```

可用工具：

```bash
hp-toolbox   # 惠普打印机图形工具箱
hp-scan      # 惠普扫描仪驱动程序
```

## 2. 扫描图片

默认黑白扫描，输出 `hpscanxxx.png`：

```bash
hp-scan
```

彩色扫描，300dpi：

```bash
hp-scan -m color -r 300
```

执行后会列出扫描设备，例如：

```text
Enter number 0...3 for device (q=quit) ?
```

选择对应的惠普设备编号。示例中选择 `3`：

```text
? 3
```

> 如果提示参数错误，可继续使用上述命令重新选择 `3`，通常即可正常扫描。  
> 扫描完成后，图片会保存到 `~/hpscanxxx.jpg` 或 `~/hpscanxxx.png`，以终端实际输出文件名为准。

## 3. 安装 ImageMagick 并拼接 PDF

```bash
sudo apt install imagemagick
```

将多张扫描图片拼接为 PDF：

```bash
convert hpscan001.jpg hpscan002.jpg hpscan003.jpg output.pdf
```

## 4. 解决 ImageMagick 报错

### 4.1 PDF 安全策略报错

报错：

```text
convert-im6.q16: attempt to perform an operation not allowed by the security policy `PDF' @ error/constitute.c/IsCoderAuthorized/426.
```

编辑策略文件：

```bash
sudo gvim /etc/ImageMagick-6/policy.xml
```

找到类似内容：

```xml
<policy domain="coder" rights="none" pattern="PDF" />
```

修改为：

```xml
<policy domain="coder" rights="read|write" pattern="PDF" />
```

保存后重新执行 `convert`。

### 4.2 缓存资源不足报错

报错：

```text
convert-im6.q16: cache resources exhausted `66-5.jpg' @ error/cache.c/OpenPixelCache/4095.
```

继续编辑：

```bash
sudo gvim /etc/ImageMagick-6/policy.xml
```

调整资源限制，例如：

```xml
<policy domain="resource" name="memory" value="2GiB"/>
<policy domain="resource" name="map" value="512MiB"/>
<policy domain="resource" name="width" value="16KP"/>
<policy domain="resource" name="height" value="16KP"/>
<!-- <policy domain="resource" name="list-length" value="128"/> -->
<policy domain="resource" name="area" value="128MP"/>
<policy domain="resource" name="disk" value="4GiB"/>
```

保存后重新执行：

```bash
convert hpscan001.jpg hpscan002.jpg hpscan003.jpg output.pdf
```

即可生成 `output.pdf`。

## 5. `convert` 的常见用法

`convert` 支持通配符、格式转换、多文件拼接。最后一个文件路径为输出文件。

示例：

```bash
convert hpscan*.jpg 0.pdf
convert 1.png 1.jpg
convert hpscan*.jpg 1.jpg 1.pdf
convert 0.pdf 1.pdf 2.png 2.pdf
```

说明：

- 可以将多张 `jpg/png` 拼接为 PDF。
- 可以转换图片格式，例如 PNG 转 JPG、JPG 转 PDF。
- 也可以拼接已有 PDF 和图片。

## 6. 替换 PDF 中某一页为新的图片

思路：

1. 将原 PDF 拆分为单页图片；
2. 用新图片替换其中某一页；
3. 再将这些图片重新拼接为 PDF。

### 6.1 安装 poppler-utils

```bash
sudo apt-get install poppler-utils
```

### 6.2 将 PDF 拆分为图片

```bash
pdftoppm -jpeg "old.pdf" output
```

执行后会生成类似：

```text
output-01.jpg
output-02.jpg
output-03.jpg
...
```

其中数字对应原 PDF 页码。

### 6.3 替换指定页

用新图片替换对应页码的图片。例如替换第 2 页，就用新图片替换 `output-02.jpg`。

### 6.4 重新拼接为 PDF

```bash
convert output-*.jpg new.pdf
```

最终得到替换过指定页面的 `new.pdf`。

## 7. 关键命令汇总

```bash
# 安装扫描工具
sudo apt install hplip hplip-gui

# 彩色扫描 300dpi
hp-scan -m color -r 300

# 安装 ImageMagick
sudo apt install imagemagick

# 图片拼接为 PDF
convert hpscan001.jpg hpscan002.jpg hpscan003.jpg output.pdf

# 修改 ImageMagick 策略文件
sudo gvim /etc/ImageMagick-6/policy.xml

# 安装 PDF 拆页工具
sudo apt-get install poppler-utils

# PDF 拆分为 JPG
pdftoppm -jpeg "old.pdf" output

# 替换页面后重新拼接
convert output-*.jpg new.pdf
```

## 8. 旋转图片

使用 ImageMagick 的 `convert` 命令旋转图片，核心语法非常简单，主要是通过 `-rotate` 参数指定旋转角度。

### 基本语法

```bash
convert 输入图片 -rotate 角度 输出图片
```

角度为**正数**时，图片会**顺时针**旋转；为**负数**时，则**逆时针**旋转。

### 常用旋转操作

**1. 旋转固定角度（90°、180°、270°）**
这是最常用的场景，适合快速校正照片方向。

```bash
# 顺时针旋转90度
convert input.jpg -rotate 90 output.jpg

# 逆时针旋转90度
convert input.jpg -rotate -90 output.jpg

# 旋转180度（上下颠倒）
convert input.jpg -rotate 180 output.jpg
```
以上操作均会生成新文件 `output.jpg`，原始文件不受影响。

**2. 按任意角度旋转（如45°、30°）**
适合创意微调或校正倾斜的扫描件。

```bash
convert input.jpg -rotate 45 output.jpg
```
**需要注意**：非90倍数的旋转，图片的边角会超出原画布范围，产生空白区域，默认这些区域会以黑色填充。

**3. 自定义空白区域的背景色**
如果旋转后产生的黑色背景不符合需求，可以先用 `-background` 选项指定颜色（如白色或透明），再进行旋转。

```bash
# 将旋转后的背景设为白色
convert input.jpg -background white -rotate 45 output.jpg

# 将背景设为透明（仅对PNG等支持透明的格式有效）
convert input.png -background transparent -rotate 45 output.png
```
**顺序很重要**：`-background` 选项必须放在 `-rotate` 选项**之前**才能生效。

### 批量旋转图片

如果需要处理一个目录下的多张图片，可以配合 `find` 命令来实现。

**使用 `find` 配合 `convert`（推荐，可控性强）**
此命令会查找当前目录（`-maxdepth 1`）下所有 `.jpg` 文件，并逐一进行顺时针90度旋转，**直接覆盖原文件**。
```bash
find . -maxdepth 1 -type f -name "*.jpg" -exec convert {} -rotate 90 {} \;
```
**注意**：此操作会直接修改原始文件，建议操作前先做好备份。
