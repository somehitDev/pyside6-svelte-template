# -*- coding: utf-8 -*-
"""
Template of PySide6.QWebEngineView and Svelte
"""
import pathlib
from datetime import datetime
from PySide6.QtCore import QObject, Slot, Signal, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from . import __path__


root_dir = pathlib.Path(__path__[0]).resolve()
class Bridge(QObject):
    show_timestamp = Signal(str)

    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.send_timestamp)
        self.timer.start(1000)

    @Slot(int)
    def show_count(self, count:int):
        print(f"current count: {count}")

    @Slot()
    def send_timestamp(self):
        self.show_timestamp.emit(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Webview Template")
        self.resize(600, 400)

        self.webview = QWebEngineView()
        self.channel = QWebChannel()

        self.bridge = Bridge()
        self.channel.registerObject("bridge", self.bridge)

        self.webview.page().setWebChannel(self.channel)

        self.webview.setUrl(QUrl("qrc:/index.html"))

        self.setCentralWidget(self.webview)

def main():
    import sys
    from PySide6.QtCore import qInstallMessageHandler, QtMsgType
    from .dist import svelte_dist

    def empty_message_handler(msg_type, msg_log_context, msg_string):
        if msg_type == QtMsgType.QtCriticalMsg:
            print(msg_string)

    app = QApplication(sys.argv + [ "--remote-debugging-port=9999" ])

    qInstallMessageHandler(empty_message_handler)

    win = MainWindow()
    win.showNormal()

    sys.exit(app.exec())