import tkinter as tk
import keyboard
import win32gui
import win32api

import time
import os
import subprocess
import ctypes
import psutil
import tkinter.messagebox

class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("小工具")
        self.root.geometry("400x380")  # 调整窗口大小

        self.button = tk.Button(self.root, text="说明", command=self.show_info)
        self.button.pack(side=tk.RIGHT)

        self.opacity = tk.Scale(self.root, from_=10, to=100, orient=tk.HORIZONTAL, command=self.update_opacity)
        self.opacity.set(100)
        self.opacity.pack()

        self.entry = tk.Text(self.root, wrap=tk.WORD)  # 使用 Text 小部件以支持多行输入
        self.entry.pack()

        self.new_entry = tk.Text(self.root, wrap=tk.WORD)  # 新增：新的输入框
        self.new_entry.pack()

        self.root.withdraw()  # 隐藏窗口

        keyboard.add_hotkey("ctrl+alt+v", self.simulate_input)
        keyboard.add_hotkey("ctrl+alt+x", self.simulate_line_input)  # 新增：用于一行一行的模拟输入
        keyboard.add_hotkey("ctrl+1", self.toggle_window_visibility)

        try:
            self.clipboard_content = self.root.clipboard_get()
        except tk.TclError:
            self.clipboard_content = ""  # 提供一个默认值

        self.root.after(1000, self.update_clipboard)  # 每隔1000毫秒检查一次剪贴板

        self.topmost_block = tk.Toplevel(self.root)
        self.topmost_block.overrideredirect(True)
        self.topmost_block.geometry("30x30+0+0")  # 将白色色块放在屏幕的左上角
        self.topmost_block.configure(background='white')
        self.topmost_block.attributes('-topmost', True, '-alpha', 0.3)  # 设置透明度为30%
        self.topmost_block.bind("<Double-Button-1>", self.toggle_network)

        self.network_adapters = list(psutil.net_if_addrs().keys())
        print(f"网络适配器的名称：{self.network_adapters}")  # 打印网络适配器的名称

        self.network_enabled = True

    def update_opacity(self, value):  # 新增：用于更新窗口的透明度
        self.root.attributes('-alpha', int(value) / 100)

    def update_clipboard(self):
        try:
            new_clipboard_content = self.root.clipboard_get()
            if new_clipboard_content != self.clipboard_content:
                self.clipboard_content = new_clipboard_content
                self.entry.delete("1.0", tk.END)
                self.entry.insert(tk.END, self.clipboard_content)
                self.new_entry.delete("1.0", tk.END)
                self.new_entry.insert(tk.END, self.clipboard_content)
        except tk.TclError:
            pass
        finally:
            self.root.after(1000, self.update_clipboard)

    def simulate_input(self):
        text = self.entry.get("1.0", "end-1c")  # 获取旧输入框的全部内容
        keyboard.write(text)

    def simulate_line_input(self):  # 新增：用于一行一行的模拟输入
        line = self.new_entry.get("1.0", "2.0")  # 获取新输入框的第一行
        print(f"旧输入框的内容：\n{self.entry.get('1.0', 'end-1c')}")  # 输出旧输入框的内容
        print(f"新输入框的内容：\n{self.new_entry.get('1.0', 'end-1c')}")  # 输出新输入框的内容
        print(f"当前模拟输出的内容：\n{line}")  # 输出当前模拟输出的内容
        keyboard.write(line)
        keyboard.press_and_release("enter")
        self.new_entry.delete("1.0", "2.0")  # 删除新输入框的第一行

    def stop_simulation(self):
        keyboard.unhook_all_hotkeys()

    def toggle_window_visibility(self):
        if self.root.state() == "withdrawn":
            self.root.deiconify()
        else:
            self.root.withdraw()

    def toggle_network(self, event):  # 新增：用于开启/禁用所有网卡
        for adapter in self.network_adapters:
            if self.network_enabled:
                command = f'netsh interface set interface "{adapter}" admin=disable'
            else:
                command = f'netsh interface set interface "{adapter}" admin=enable'
            print(f"正在执行命令：{command}")  # 打印正在执行的命令
            subprocess.call(command, shell=True)
        self.network_enabled = not self.network_enabled  # 更新网络适配器的状态

    def show_info(self):
        info = "小工具箱(By GTP-4&Mike)\n\n1.ctrl+alt+x单行模式，一次输出文本框中的一行\n\n2.ctrl+alt+v直接粘贴整个文本框的内容\n\n3.ctrl+1隐藏窗口，并且后台改成chrome.exe以防被发现\n\n4.双击屏幕左上角可以禁用/开启网卡，相当于一键解控"
        tkinter.messagebox.showinfo("说明", info)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MyApp()
    app.run()
