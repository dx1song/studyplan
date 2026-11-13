"""一键启动入口：启动后端服务并自动打开浏览器。

双击项目根目录的「启动学习计划系统.bat」会调用本脚本：
1. 若 8000 端口已有服务在运行，直接打开浏览器，不重复启动；
2. 否则后台线程轮询 /api/health，等服务真正就绪后再打开浏览器（避免连接被拒绝）；
3. 主线程运行 uvicorn（前端页面由后端直接托管）。
"""

import socket
import threading
import time
import urllib.request
import webbrowser

import uvicorn

from main import app

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://127.0.0.1:{PORT}"


def _port_in_use() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((HOST, PORT)) == 0


def _open_when_ready() -> None:
    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            urllib.request.urlopen(URL + "/api/health", timeout=1)
            webbrowser.open(URL)
            return
        except Exception:
            time.sleep(0.3)
    # 超时兜底：仍尝试打开一次
    webbrowser.open(URL)


if __name__ == "__main__":
    if _port_in_use():
        print(f"服务已在运行，直接打开浏览器：{URL}")
        webbrowser.open(URL)
    else:
        print("正在启动服务，请稍候……")
        print(f"服务就绪后将自动打开浏览器；若未自动打开，请手动访问 {URL}")
        print("按 Ctrl+C 停止服务。")
        threading.Thread(target=_open_when_ready, daemon=True).start()
        uvicorn.run(app, host=HOST, port=PORT)
