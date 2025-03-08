from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def generate_texture(image_path, output_path="filled_temp.png"):
    """
    将透明部分填充为图像的主要颜色
    :param image_path: 输入图像路径（带透明通道）
    :param output_path: 输出图像路径
    """
    # 打开图像并确保是RGBA格式（带透明通道）
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    # 将图像数据转换为NumPy数组
    image_array = np.array(image)

    # 提取不透明像素的RGB值
    opaque_pixels = image_array[image_array[:, :, 3] > 0][:, :3]  # 只取RGB通道，忽略Alpha通道

    # 使用K-Means聚类找到主要颜色（颜色数量为1）
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(opaque_pixels)

    # 获取主要颜色
    dominant_color = kmeans.cluster_centers_[0].astype(int)

    # 创建一个新的图像数组，用于填充透明部分
    filled_image_array = image_array.copy()

    # 将透明部分（Alpha通道为0）填充为主要颜色
    transparent_mask = filled_image_array[:, :, 3] == 0  # 找到透明区域
    filled_image_array[transparent_mask, :3] = dominant_color  # 填充RGB通道
    filled_image_array[transparent_mask, 3] = 255  # 将Alpha通道设置为不透明

    # 将NumPy数组转换回图像
    filled_image = Image.fromarray(filled_image_array, "RGBA")

    # 保存结果
    filled_image.save(output_path)
