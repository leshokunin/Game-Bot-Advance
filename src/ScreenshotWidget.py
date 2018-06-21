from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
import configparser
import discord
from discord.ext import commands
from DiscordScreenshotEvents import DiscordScreenshotEvents


class ScreenshotWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.4)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Select capture area...')
        self.show()

    def start_discord_bot(self, screen_x1, screen_y1, screen_x2, screen_y2):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        description = config.get('DISCORD', 'description')
        bot = commands.Bot(command_prefix='?', description=description)
        discord_events = DiscordScreenshotEvents(bot, config, screen_x1, screen_y1, screen_x2, screen_y2)
        bot.add_cog(discord_events)

        try:
            bot.run(config.get('DISCORD', 'bot_token'))

        finally:
            discord_events.write_chat_log()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 5))
        qp.setBrush(QtGui.QColor(0, 0, 0, 255))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()
        screen_x1 = min(self.begin.x(), self.end.x())
        screen_y1 = min(self.begin.y(), self.end.y())
        screen_x2 = max(self.begin.x(), self.end.x())
        screen_y2 = max(self.begin.y(), self.end.y())
        self.start_discord_bot(screen_x1, screen_y1, screen_x2, screen_y2)