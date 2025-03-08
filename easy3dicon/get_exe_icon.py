import os
import ctypes
from ctypes.wintypes import HICON, UINT, DWORD, LONG, WORD
from PIL import Image

# Define constants and functions
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
ExIcon = user32.PrivateExtractIconsA
DesIcon = user32.DestroyIcon

# Define structures
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", DWORD), ("biWidth", LONG), ("biHeight", LONG),
        ("biPlanes", WORD), ("biBitCount", WORD), ("biCompression", DWORD),
        ("biSizeImage", DWORD), ("biXPelsPerMeter", LONG), ("biYPelsPerMeter", LONG),
        ("biClrUsed", DWORD), ("biClrImportant", DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", DWORD * 3)]

# Convert raw data to RGBA format
def rgba(raw, width=256, height=256):
    rgba = bytearray(height * width * 4)
    rgba[0::4], rgba[1::4], rgba[2::4], rgba[3::4] = raw[2::4], raw[1::4], raw[0::4], [255] * (height * width)
    for i in range(0, len(rgba), 4):
        if rgba[i:i+3] == b'\x00\x00\x00':
            rgba[i+3] = 0  # Set alpha to 0 for black pixels
    return bytes(rgba)

# Extract raw icon data
def get_raw_data(path, index=0, size=256):
    path = os.path.abspath(path)
    width = height = size

    icon_total_count = ExIcon(path.encode(), 0, 0, 0, None, None, 0, 0)
    hicons = (HICON * icon_total_count)()
    ids = (UINT * icon_total_count)()

    ExIcon(path.encode(), 0, size, size, ctypes.pointer(hicons), ctypes.pointer(ids), icon_total_count, 0)

    srcdc = user32.GetWindowDC(0)
    memdc = gdi32.CreateCompatibleDC(srcdc)
    bmp = gdi32.CreateCompatibleBitmap(srcdc, width, height)
    gdi32.SelectObject(memdc, bmp)
    user32.DrawIconEx(memdc, 0, 0, hicons[index], width, height, 0, None, 0x0003)  # Use DrawIconEx to scale the icon

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height

    data = ctypes.create_string_buffer(width * height * 4)
    if gdi32.GetDIBits(memdc, bmp, 0, height, data, ctypes.byref(bmi), 0) != height:
        raise Exception("gdi32.GetDIBits() failed.")

    gdi32.DeleteObject(bmp)
    return bytearray(data)

# Get RGBA data from icon
def get_rgba_data(path):
    return rgba(get_raw_data(path))

def get_icon(path,output):
    data = get_rgba_data(path)
    img = Image.frombytes('RGBA', (256, 256), data)
    try:
        img.save(output, format='PNG')
        return output
    except Exception as e:
        print("图标保存失败: ", e)
