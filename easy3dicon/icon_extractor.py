# 文件: icon_extractor.py
import win32com.client
from easy3dicon.get_exe_icon import get_icon
def extract_icon(file_path):
    if file_path.endswith('.png'):
        return file_path

    if file_path.endswith('.lnk'):
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(file_path)
        icon_path = shortcut.IconLocation.split(',')[0]
        file_path = icon_path  # 如果是 exe，继续往下执行
    print(file_path)

    if file_path.endswith('.ico'):
        from PIL import Image
        img = Image.open(file_path)
        # output = os.path.join(os.environ['TEMP'], 'temp.png')
        output = f'temp.png'  # 测试用
        img.save(output, format='PNG')
        return output

    if file_path.endswith('.exe'):
        # 临时输出在系统临时文件夹
        # output = os.path.join(os.environ['TEMP'], 'temp.png')
        output = f'temp.png' # 测试用
        try:
            return get_icon(file_path,output)
        except Exception as e:
            print("图标提取失败: ", e)
            return None

    return None
