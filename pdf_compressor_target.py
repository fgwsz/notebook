#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 压缩工具（支持目标压缩率）

用法示例：
    # 压到原体积的 50%
    python pdf_compressor_target.py input.pdf --target-ratio 0.5

    # 指定输出文件，并允许 ±5% 误差
    python pdf_compressor_target.py input.pdf output.pdf --target-ratio 0.5 --tolerance 0.05

    # 只做无损压缩（不追求精确比例）
    python pdf_compressor_target.py input.pdf --method pymupdf

依赖：
    pip install pymupdf     # 可选，用于无损压缩和兜底
    Ghostscript             # 推荐安装，用于有损压缩
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


# ----------------------------
# 工具函数
# ----------------------------
def human_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def find_ghostscript():
    for cmd in ("gs", "gswin64c", "gswin32c"):
        path = shutil.which(cmd)
        if path:
            return path
    return None


def file_size(path) -> int:
    p = Path(path)
    return p.stat().st_size if p.exists() else 0


# ----------------------------
# PyMuPDF 无损压缩
# ----------------------------
def compress_with_pymupdf(input_path: str, output_path: str):
    if fitz is None:
        raise RuntimeError("未安装 PyMuPDF，请执行：pip install pymupdf")

    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()


# ----------------------------
# Ghostscript 有损压缩（可调分辨率）
# ----------------------------
def run_ghostscript(
    gs: str,
    input_path: str,
    output_path: str,
    color_dpi: int,
    gray_dpi: int,
    mono_dpi: int,
    jpeg_quality: int,
):
    """
    调用 Ghostscript 做压缩。
    dpi 越低、jpeg_quality 越低，体积越小。
    """
    cmd = [
        gs,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        "-dAutoRotatePages=/None",
        # 图片降采样
        "-dDownsampleColorImages=true",
        "-dDownsampleGrayImages=true",
        "-dDownsampleMonoImages=true",
        f"-dColorImageResolution={color_dpi}",
        f"-dGrayImageResolution={gray_dpi}",
        f"-dMonoImageResolution={mono_dpi}",
        # JPEG 质量
        "-dColorImageDownsampleType=/Bicubic",
        "-dGrayImageDownsampleType=/Bicubic",
        "-dMonoImageDownsampleType=/Subsample",
        f"-dJPEGQ={jpeg_quality}",
        f"-sOutputFile={output_path}",
        input_path,
    ]
    subprocess.run(cmd, check=True)


# ----------------------------
# 迭代达到目标压缩率
# ----------------------------
def compress_to_target_ratio(
    gs: str,
    input_path: str,
    output_path: str,
    target_ratio: float = 0.5,
    tolerance: float = 0.05,
    max_iter: int = 12,
):
    """
    通过调节 (color_dpi, gray_dpi, mono_dpi, jpeg_quality) 逐步逼近目标压缩率。

    target_ratio: 目标体积 / 原始体积。0.5 表示压缩到原来的一半。
    tolerance:    允许的误差，例如 0.05 表示结果在目标的 ±5% 之内即可。
    """
    original_size = file_size(input_path)
    target_size = original_size * target_ratio

    # 参数空间：从“高质量”到“极低质量”排列
    presets = [
        # (color_dpi, gray_dpi, mono_dpi, jpeg_quality)
        (300, 300, 600, 90),
        (200, 200, 400, 85),
        (150, 150, 300, 80),
        (120, 120, 300, 75),
        (100, 100, 200, 70),
        (96, 96, 200, 65),
        (72, 72, 150, 60),
        (72, 72, 150, 50),
        (60, 60, 120, 45),
        (50, 50, 100, 40),
        (40, 40, 80, 35),
        (30, 30, 80, 30),
    ]

    # 先整体扫描一遍，找到第一个 <= target_size 的档位
    best = None  # (abs_diff, path, params, size)

    tmpdir = Path(tempfile.mkdtemp(prefix="pdfcmp_"))
    try:
        for idx, (cdpi, gdpi, mdpi, q) in enumerate(presets[:max_iter]):
            tmp_out = tmpdir / f"try_{idx}.pdf"
            try:
                run_ghostscript(
                    gs, input_path, str(tmp_out), cdpi, gdpi, mdpi, q
                )
            except subprocess.CalledProcessError:
                continue

            size = file_size(tmp_out)
            diff = abs(size - target_size)
            print(
                f"  尝试 #{idx+1}: dpi={cdpi}/{gdpi}/{mdpi}, q={q} "
                f"→ {human_size(size)}（目标 {human_size(int(target_size))}）"
            )

            if best is None or diff < best[0]:
                best = (diff, tmp_out, (cdpi, gdpi, mdpi, q), size)

            # 命中容差范围即可停止
            if abs(size - target_size) / target_size <= tolerance:
                break

            # 已经压得比目标更小，再往下只会更小，提前结束
            if size <= target_size:
                break

        if best is None:
            raise RuntimeError("Ghostscript 所有档位均失败。")

        # 把最佳结果复制到输出路径
        shutil.copyfile(best[1], output_path)
        return best[3], best[2]

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ----------------------------
# 主程序
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="PDF 压缩工具（支持目标压缩率）")
    parser.add_argument("input", help="输入 PDF 文件")
    parser.add_argument("output", nargs="?", help="输出 PDF 文件")
    parser.add_argument(
        "--method",
        choices=["auto", "pymupdf", "ghostscript"],
        default="auto",
        help="压缩方法，默认 auto",
    )
    parser.add_argument(
        "--target-ratio",
        type=float,
        default=None,
        help="目标压缩率，例如 0.5 表示压到原体积的 50%%",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.05,
        help="允许误差，默认 0.05（±5%%）",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：输入文件不存在：{input_path}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        suffix = ""
        if args.target_ratio:
            suffix = f"_x{args.target_ratio}"
        output_path = input_path.with_name(
            input_path.stem + suffix + "_compressed" + input_path.suffix
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    original_size = file_size(input_path)
    print(f"原始大小：{human_size(original_size)}")

    gs = find_ghostscript()
    method = args.method
    if method == "auto":
        method = "ghostscript" if gs else "pymupdf"

    # 需要精确控制压缩率 → 走 Ghostscript 迭代
    if args.target_ratio is not None:
        if not gs:
            print(
                "错误：达到指定压缩率需要 Ghostscript，请先安装并加入 PATH。",
                file=sys.stderr,
            )
            sys.exit(1)
        print(
            f"目标压缩率：{args.target_ratio:.0%} "
            f"（目标大小约 {human_size(int(original_size * args.target_ratio))}）"
        )
        try:
            final_size, params = compress_to_target_ratio(
                gs,
                str(input_path),
                str(output_path),
                target_ratio=args.target_ratio,
                tolerance=args.tolerance,
            )
        except Exception as e:
            print(f"压缩失败：{e}", file=sys.stderr)
            sys.exit(1)
        print(f"采用参数：dpi={params[0]}/{params[1]}/{params[2]}, JPEGQ={params[3]}")
    else:
        # 没有指定压缩率，按原来的逻辑
        if method == "ghostscript":
            if not gs:
                print("错误：未找到 Ghostscript。", file=sys.stderr)
                sys.exit(1)
            print("使用 Ghostscript（ebook 档）压缩 ...")
            try:
                run_ghostscript(gs, str(input_path), str(output_path), 150, 150, 300, 80)
            except subprocess.CalledProcessError as e:
                print(f"压缩失败：{e}", file=sys.stderr)
                sys.exit(1)
        else:
            print("使用 PyMuPDF 无损压缩 ...")
            try:
                compress_with_pymupdf(str(input_path), str(output_path))
            except Exception as e:
                print(f"压缩失败：{e}", file=sys.stderr)
                sys.exit(1)
        final_size = file_size(output_path)

    ratio = 1 - final_size / original_size if original_size else 0
    actual_ratio = final_size / original_size if original_size else 0

    print(f"压缩后大小：{human_size(final_size)}")
    print(f"实际压缩率：{actual_ratio:.1%}（即缩小了 {ratio:.1%}）")
    print(f"输出文件：{output_path}")


if __name__ == "__main__":
    main()
