

# todo
# need to have a gui (wxPython / PyQt)
# will show the current running app and the time usage
# able to set/reset timer 

import win32gui
import win32con
import win32process
import psutil
import win32api
import win32ui
from PIL import Image
import ctypes
import ctypes.wintypes

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QLabel, QTableWidget, QHeaderView
from PyQt5.QtCore import QTimer
import sys

mock_software_list = [{
    "exe_name": "chrome.exe",
    "data": [{
        "name": "Google",
        "time": 1,
    },{
        "name": "Facebook",
        "time": 2,
    }],
    "total_time": 3,
}, {
    "exe_name": "firefox.exe",
    "data": [{
        "name": "Google",
        "time": 1,
    },{
        "name": "Facebook",
        "time": 2,
    }],
    "total_time": 3,
}]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App Usage Tracker")
        self.setGeometry(100,100,400,300)
        self.software_list = mock_software_list

        self.main_timer = QTimer()

        # create a sample software row
        self.table_widget = QTableWidget(1, 3, self)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch) # table resize with main window
        self.setCentralWidget(self.table_widget)

        # self.pixmap = QtGui.QPixmap.fromWinHBITMAP(self.bitmapFromHIcon(large[0]))
    

def event_foreground_window_callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    # if (hwnd):
    #     print(f"Event {event} occurred on window {hwnd}")
    exe_name, window_title = get_window_data(hwnd)
    if (exe_name != "" and window_title !=""):
        print(f"[acitve window changed] {exe_name} ===== {window_title}")

def event_window_title_changed_callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    # if (hwnd):
    #     print(f"Event {event} occurred on window {hwnd}")
    exe_name, window_title = get_window_data(hwnd)
    if (exe_name != "" and window_title !=""):
        print(f"[window title changed] {exe_name} ===== {window_title}")

WinEventProcType = ctypes.WINFUNCTYPE(
    None, 
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)
WinForegroundWindowChanged = WinEventProcType(event_foreground_window_callback)
WinWindowTitleChanged = WinEventProcType(event_window_title_changed_callback)
user32 = ctypes.windll.user32

def set_event_hook():
    user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
    hook = user32.SetWinEventHook(
        win32con.EVENT_SYSTEM_FOREGROUND,
        win32con.EVENT_SYSTEM_FOREGROUND,
        0,
        WinForegroundWindowChanged,
        0,
        0,
        win32con.WINEVENT_OUTOFCONTEXT
    )
    hook = user32.SetWinEventHook(
        win32con.EVENT_OBJECT_NAMECHANGE,
        win32con.EVENT_OBJECT_NAMECHANGE,
        0,
        WinWindowTitleChanged,
        0,
        0,
        win32con.WINEVENT_OUTOFCONTEXT
    )
    # Loop to keep the script running
    # win32gui.PumpMessages()


def get_icon(hwnd,exe_path):
    # Extract the icon from the executable file
    large, small = win32gui.ExtractIconEx(exe_path, 0)
    icon_handle = None
    if large:
        icon_handle = large[0]
    elif small:
        icon_handle = small[0]

    if icon_handle:
        icon_info = win32gui.GetIconInfo(icon_handle)
        print(icon_info)
    
    # Destroy the extracted icons to avoid resource leaks
    for hicon in large + small:
        win32gui.DestroyIcon(hicon)
    
    return icon_handle

def get_window_data(hwnd):
    window_title = ""
    window_title = win32gui.GetWindowText(hwnd)
    exe_name = ""
    icon = ""
    if window_title:
        # Get process ID
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            # Get executable name from process ID
            exe_name = psutil.Process(pid).name()
            # icon = get_icon(hwnd,psutil.Process(pid).exe())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            exe_name = "Unknown"
    # return icon, exe_name, window_title
    return exe_name, window_title

if __name__ == "__main__":
    
    set_event_hook()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()

    pass