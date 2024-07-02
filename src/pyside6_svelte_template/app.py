# -*- coding: utf-8 -*-
"""
Template of PySide6.QWebEngineView and Svelte
"""
import os, pathlib
from datetime import datetime

# qt.qpa.plugin: Could not find the Qt platform plugin "windows" in ""
# This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem
from PySide6 import __path__ as pyside6_path
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pyside6_path[0], "Qt", "plugins", "platforms")

from PySide6.QtCore import QObject, Slot, Signal, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from . import __path__


root_dir = pathlib.Path(__path__[0]).resolve()
class MainWindow(QMainWindow):
    show_timestamp = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Webview Template")
        self.resize(600, 400)

        self.webview = QWebEngineView()
        self.channel = QWebChannel()

        self.channel.registerObject("bridge", self)

        self.webview.page().setWebChannel(self.channel)

        self.setCentralWidget(self.webview)

    def showEvent(self, ev):
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_timestamp)
        self.timer.start(1000)

        self.webview.setUrl(QUrl("qrc:/index.html"))

        super().showEvent(ev)

    @Slot(int)
    def show_count(self, count:int):
        print(f"current count: {count}")

    @Slot()
    def send_timestamp(self):
        self.show_timestamp.emit(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))


def main():
    import sys
    from PySide6.QtCore import qInstallMessageHandler, QtMsgType
    from .dist import svelte_dist

    def empty_message_handler(msg_type, msg_log_context, msg_string):
        if msg_type == QtMsgType.QtCriticalMsg:
            print(msg_string)

    app = QApplication(sys.argv + [ "--webEngineArgs", "--remote-debugging-port=9999" ])

    qInstallMessageHandler(empty_message_handler)

    win = MainWindow()
    win.showNormal()

    sys.exit(app.exec())