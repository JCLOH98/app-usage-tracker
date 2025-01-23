

# todo
# need to have a gui (wxPython / PyQt)
# will show the current running app and the time usage
# able to set/reset timer 
# only triggers the function when the foreground windows changes / window resized

import win32gui
import win32con
import win32process
import psutil
import win32api
import win32ui
from PIL import Image

def get_icon(hwnd,exe_path):
    
    # Extract the icon from the executable file
    large, small = win32gui.ExtractIconEx(exe_path, 0)
    icon_handle = None
    if large:
        icon_handle = large[0]
    elif small:
        icon_handle = small[0]

    # Save the icon to a file
    icoX = win32api.GetSystemMetrics(win32con.SM_CXICON)
    icoY = win32api.GetSystemMetrics(win32con.SM_CXICON)
    if icon_handle:
        icon_info = win32gui.GetIconInfo(icon_handle)
        print(icon_info)
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, icoX, icoX)
        hdc = hdc.CreateCompatibleDC()

        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0,0), icon_handle)
        
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (icoX,icoY),
            bmpstr, 'raw', 'BGRA', 0, 1
        )

        img.save('icon.png')
    
    # Destroy the extracted icons to avoid resource leaks
    for hicon in large + small:
        win32gui.DestroyIcon(hicon)
    
    
    return icon_handle

    # hlib = win32api.LoadLibrary(exe_path)
    # icon_names = win32api.EnumResourceNames(hlib, win32con.RT_ICON)
    # for icon_name in icon_names:
    #     rec = win32api.LoadResource(hlib, win32con.RT_ICON, icon_name)
    #     with open(f"icon_{icon_name}.png","wb") as file:
    #         file.write(rec)

def get_active_window():
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd)
    exe_name = ""
    icon = ""
    if window_title:
        # Get process ID
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            # Get executable name from process ID
            exe_name = psutil.Process(pid).name()
            icon = get_icon(hwnd,psutil.Process(pid).exe())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            exe_name = "Unknown"
    print(f"{icon} - {exe_name} - {window_title}")


if __name__ == "__main__":
    get_active_window()
    # while(1):
        # get_active_window()
    pass