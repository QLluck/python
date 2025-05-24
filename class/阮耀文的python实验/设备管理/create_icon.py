from PIL import Image, ImageDraw

# 创建一个 32x32 像素的图像，使用 RGBA 模式（支持透明度）
icon_size = (32, 32)
image = Image.new('RGBA', icon_size, (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# 绘制一个简单的图标
# 外圈
draw.ellipse([2, 2, 29, 29], outline=(0, 120, 215), width=2)
# 内圈
draw.ellipse([8, 8, 23, 23], fill=(0, 120, 215))

# 保存为 ICO 文件
image.save('icon.ico', format='ICO') 