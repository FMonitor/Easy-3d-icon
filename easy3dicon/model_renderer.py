import cv2
import numpy as np
import pyvista as pv


def extract_and_extrude(icon_path, thickness=0.1):
    # 读取图像（带 Alpha 通道）
    image = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise FileNotFoundError(f"无法找到文件: {icon_path}")

    # 分离 Alpha 通道（透明度）
    alpha_channel = image[:, :, 3]

    # 二值化处理，将透明部分变为黑色，非透明部分为白色
    _, binary = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

    # 使用 OpenCV 找轮廓，确保闭合和完整性
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    meshes = []

    for contour in contours:
        # 转换轮廓为浮点数
        contour = contour.astype(float)

        # 构造 2D 多边形点集
        points = np.column_stack((contour[:, 0, 0], contour[:, 0, 1], np.zeros(contour.shape[0])))

        # 创建 PyVista PolyData 对象
        base = pv.PolyData(points)
        base = base.delaunay_2d()

        # 拉伸成 3D 模型
        extruded = base.extrude((0, 0, thickness))

        # 创建顶部和底部封盖
        bottom = base
        top = pv.PolyData(points + [0, 0, thickness])
        top = top.delaunay_2d()

        # 合并底面、拉伸部分和顶面
        meshes.append(pv.MultiBlock([extruded, bottom, top]).combine())

    # 合并所有轮廓生成的模型
    combined = pv.MultiBlock(meshes).combine()

    # 归一化模型尺寸，确保纹理贴合
    bounds = combined.bounds
    x_min, x_max, y_min, y_max, _, _ = bounds
    combined.points[:, 0] = (combined.points[:, 0] - x_min) / (x_max - x_min)
    combined.points[:, 1] = (combined.points[:, 1] - y_min) / (y_max - y_min)

    # 加载图标作为纹理
    texture = pv.Texture(icon_path)

    # 确保 combined 有统一的纹理坐标
    combined.active_texture_coordinates = combined.points[:, :2]

    # 渲染模型，应用纹理
    plotter = pv.Plotter()
    plotter.add_mesh(combined, texture=texture, show_edges=True)
    plotter.add_axes()
    plotter.show_bounds()
    plotter.set_background('white')
    plotter.show()


# 调用函数测试
extract_and_extrude('temp.png', 0.3)
