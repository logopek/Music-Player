from PyQt5 import QtWidgets, QtSvg
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
import setproctitle
import ui
import os
import database_rq

"""Changelog: Switching from QMediaContent to QMediaPlaylist, Added repeat mode"""

class MainApp(ui.Ui_MainWindow):
    version = "1.1"

    def __init__(self, MainWindow):
        super().__init__()
        self.setupUi(MainWindow)
        self.player = QMediaPlayer()
        setproctitle.setproctitle("Music Player")
        self.selected = False
        self.paused = True
        self.now_pos = 0
        self.setupButtons()
        self.statusbar.showMessage(f"Version {self.version}")
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)


    def setupButtons(self):
        self.addMusic.clicked.connect(self.addMusicToList)
        self.buttonPlay.clicked.connect(self.playNow)
        self.nextTrack.clicked.connect(self.toNextTrack)
        self.previousTrack.clicked.connect(self.toPreviousTrack)
        self.timeMusic.sliderReleased.connect(self.changeTime)
        self.player.durationChanged.connect(self.setDuration)
        self.player.positionChanged.connect(self.updateSlider)
        self.repeat_btn.clicked.connect(self.repeatMusic)

        self.listMusic.itemSelectionChanged.connect(self.drop_all)
        self.volume.sliderMoved.connect(self.change_volume)
        self.addMusic.setShortcut("Ctrl+O")
        self.buttonPlay.setShortcut("Space")
        self.nextTrack.setShortcut("D")
        self.previousTrack.setShortcut("A")



    def repeatMusic(self):
        print(self.repeat_btn.isChecked())
        if self.repeat_btn.isChecked():
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)

    def addMusicToList(self):
        items = []
        for i in range(self.listMusic.count()):
            items.append(self.listMusic.item(i).text())
        dialog = QtWidgets.QFileDialog().getOpenFileNames(directory=os.environ["USERPROFILE"] + "/Music", filter="mp3 (*.mp3);; ogg (*.ogg);; wav (*.wav)")
        self.listMusic.addItems([dialog[0][i] for i in range(len(dialog[0])) if dialog[0][i] not in items])
        [self.playlist.addMedia(QMediaContent(QUrl(dialog[0][i]))) for i in range(len(dialog[0])) if dialog[0][i] not in items]

    def changeTime(self):
        self.player.setPosition(self.timeMusic.value())

    def change_volume(self):
        if self.volume.value() <= 0:
            self.volume_icon.load("src/volume-mute-fill.svg")
        elif self.volume.value() <= 50:
            self.volume_icon.load("src/volume-down-fill.svg")
        elif self.volume.value() > 50:
            self.volume_icon.load("src/volume-up-fill.svg")
        self.player.setVolume(self.volume.value())

    def drop_all(self):
        self.now_pos = 0
        self.player.pause()
        self.buttonPlay.setIcon(QIcon("src/play-circle-fill.svg"))
        self.paused = True


    def setMusic(self):
        if self.listMusic.selectedItems():
            self.playlist.setCurrentIndex(self.listMusic.row(self.listMusic.selectedItems()[0]))
            return True
        else:
            return False



    def toNextTrack(self):
        if self.listMusic.count():
            x = self.listMusic.selectedItems()
            if self.listMusic.count() == self.listMusic.row(x[0]) + 1:
                self.listMusic.setCurrentRow(0)
            else:
                self.listMusic.setCurrentRow(self.listMusic.row(x[0]) + 1)
            del x
        self.now_pos = 0
        self.drop_all()
        self.playNow()

    def toPreviousTrack(self):
        if self.listMusic.count():
            x = self.listMusic.selectedItems()
            if self.listMusic.row(x[0]) == 0:
                self.listMusic.setCurrentRow(self.listMusic.count() - 1)
            else:
                self.listMusic.setCurrentRow(self.listMusic.row(x[0]) - 1)
        self.now_pos = 0
        self.drop_all()
        self.playNow()

    def setDuration(self):
        self.timeMusic.setMaximum(self.player.duration())
        seconds = int((self.player.duration() / 1000) % 60)
        minutes = int((self.player.duration() / (1000 * 60)) % 60)
        self.all_time_music.setText(f"{0 if minutes < 10 else ''}{minutes}:{0 if seconds < 10 else ''}{seconds}")
        del seconds, minutes

    def updateSlider(self):
        self.timeMusic.setValue(self.player.position())
        seconds = int((self.player.position() / 1000) % 60)
        minutes = int((self.player.position() / (1000 * 60)) % 60)
        self.now_time_music.setText(f"{0 if minutes < 10 else ''}{minutes}:{0 if seconds < 10 else ''}{seconds}")
        del seconds, minutes



    # self.buttonPlay.setIcon(QIcon("src/pause-circle-fill.svg"))

    def playNow(self):
        if self.paused:
            self.setMusic()
            self.player.play()
            self.player.setPosition(self.now_pos)
            if self.player.mediaStatus() != 1 and self.player.mediaStatus() != 8:
                self.buttonPlay.setIcon(QIcon("src/pause-circle-fill.svg"))
                self.paused = False

        else:
            self.now_pos = self.player.position()
            self.player.pause()
            self.buttonPlay.setIcon(QIcon("src/play-circle-fill.svg"))
            self.paused = True

        """if self.player.isMetaDataAvailable():
            self.setWindowTitle("Playing" + self.player.metaData("Title"))
            self.statusbar.showMessage("Playing" + self.player.metaData("Title"))
        else:
            self.setWindowTitle("Music Player")
"""




def _except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    exe = MainApp(MainWindow)
    MainWindow.show()
    sys.excepthook = _except_hook
    sys.exit(app.exec_())
