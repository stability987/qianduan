# 替换图片绿色背景（本地脚本）

脚本位置：scripts/replace_bg.py

依赖：
```
pip install -r requirements.txt
```

用法示例：
```
python scripts/replace_bg.py <前景图路径> <背景图路径> <输出路径>

# 示例（假设把附件截图保存为 image/hero.png）：
python scripts/replace_bg.py image/hero.png image/cta-bg.jpg output/hero_composite.png
```

可调参数：
- `--lower H,S,V` 和 `--upper H,S,V` 用来微调绿色范围（HSV 空间）。默认值为 `35,40,40` 到 `90,255,255`。

注意事项：
- 请在本地先把要处理的截图保存到项目中（例如 `image/hero.png`）。
- 若合成边缘出现问题，可微调 HSV 阈值或手动在图像编辑器中修整。
