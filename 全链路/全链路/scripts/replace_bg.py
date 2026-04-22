#!/usr/bin/env python3
"""
replace_bg.py

用法：
  python scripts/replace_bg.py <foreground_path> <background_path> [output_path] [--lower H,S,V] [--upper H,S,V]

示例：
  python scripts/replace_bg.py image/hero.png image/cta-bg.jpg output/result.png

说明：对输入图片做简单的 chroma-key（绿色）抠图并用背景图替换抠掉的区域。
可通过 --lower 和 --upper 调整 HSV 阈值以适配不同绿色。
"""
import sys
import os
import argparse
import cv2
import numpy as np


def parse_hsv(s):
    parts = [int(x) for x in s.split(',')]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("HSV 必须是 H,S,V 三个用逗号分隔的整数")
    return np.array(parts, dtype=np.uint8)


def replace_green(foreground_path, background_path, output_path, lower_hsv, upper_hsv):
    fg = cv2.imread(foreground_path, cv2.IMREAD_COLOR)
    if fg is None:
        raise FileNotFoundError(f"无法打开前景图: {foreground_path}")

    bg = cv2.imread(background_path, cv2.IMREAD_COLOR)
    if bg is None:
        raise FileNotFoundError(f"无法打开背景图: {background_path}")

    h, w = fg.shape[:2]
    bg_resized = cv2.resize(bg, (w, h), interpolation=cv2.INTER_AREA)

    hsv = cv2.cvtColor(fg, cv2.COLOR_BGR2HSV)

    # 生成绿色掩码（掩盖为需要替换的区域）
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # 使用形态学处理去噪
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

    # 软化边缘，避免太生硬
    mask_blur = cv2.GaussianBlur(mask, (7, 7), 0)

    # 归一化 alpha
    alpha = mask_blur.astype(float) / 255.0
    alpha = np.expand_dims(alpha, axis=2)

    fg_float = fg.astype(float)
    bg_float = bg_resized.astype(float)

    # 对应像素混合：当 mask=255（完全绿色）时显示背景，当 mask=0 时显示前景
    comp = (1 - alpha) * fg_float + alpha * bg_float
    comp = np.clip(comp, 0, 255).astype(np.uint8)

    # 保存结果
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    cv2.imwrite(output_path, comp)


def main():
    parser = argparse.ArgumentParser(description='用背景图替换图片中的绿色 (chroma key)')
    parser.add_argument('foreground', help='前景图片路径（含绿色背景的图片）')
    parser.add_argument('background', help='用作替换的背景图片路径')
    parser.add_argument('output', nargs='?', default='output/result.png', help='输出合成图片路径（默认 output/result.png）')
    parser.add_argument('--lower', type=parse_hsv, default=np.array([35, 40, 40], dtype=np.uint8), help='HSV 下界，格式 H,S,V 例如 35,40,40')
    parser.add_argument('--upper', type=parse_hsv, default=np.array([90, 255, 255], dtype=np.uint8), help='HSV 上界，格式 H,S,V 例如 90,255,255')

    args = parser.parse_args()

    try:
        replace_green(args.foreground, args.background, args.output, args.lower, args.upper)
        print(f"合成完成：{args.output}")
    except Exception as e:
        print("处理失败:", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
