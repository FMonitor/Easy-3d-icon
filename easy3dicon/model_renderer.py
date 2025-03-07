# import pyvista as pv
# from PIL import Image
#
#
# def render_3d_model(icon_path, thickness=0.1):
#     texture = pv.Texture(icon_path)
#     # 创建一个带厚度的挤压平面（代表立体图标）
#     # 平面大小可以随需求调整
#     plane = pv.Plane(i_size=1, j_size=1)
#     # 给平面加厚度，形成一个立方体效果
#     extruded = plane.extrude((0, 0, thickness))
#
#     # 渲染器
#     plotter = pv.Plotter()
#     plotter.add_mesh(extruded, texture=texture, show_edges=False)
#
#     # 设置交互逻辑类似 Blender
#     plotter.enable_3_lights()
#     plotter.enable_parallel_projection()
#
#     plotter.show()

import pyvista as pv
from PIL import Image
import os

icon_path = r'temp.png'

# 确认文件存在
if not os.path.exists(icon_path):
    raise FileNotFoundError(f"文件未找到: {icon_path}")

# 确认图片可以打开
try:
    img = Image.open(icon_path)
    img.show()
except Exception as e:
    raise ValueError(f"图片无法打开: {e}")

# 确认 Pyvista 纹理加载
try:
    texture = pv.Texture(icon_path)
    print(texture)
except Exception as e:
    raise ValueError(f"纹理加载失败: {e}")

# 创建平面和加厚度的模型
plane = pv.Plane(i_size=1, j_size=1)
extruded = plane.extrude((0, 0, 0.1))

# 确认模型存在
print(extruded)

# 确认模型纹理坐标
print(extruded.active_texture_coordinates)
if extruded.active_texture_coordinates is None:
    extruded.active_texture_coordinates = extruded.points[:, :2]

# 显示模型
plotter = pv.Plotter()
plotter.add_mesh(extruded, texture=texture, show_edges=True)
plotter.reset_camera()
plotter.show()
