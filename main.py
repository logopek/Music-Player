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

    def __init__(self, MainWindow) -> None:

        super().__init__()
        self.setupUi(MainWindow)
        self.player = QMediaPlayer()
        setproctitle.setproctitle("L Player")
        self.items = []
        self.selected = False
        self.paused = True
        self.now_pos = 0
        self.setupButtons()
        self.statusbar.showMessage(f"Version {self.version}")
        self.statusbar.setStyleSheet("background-color: #96aab7")
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.database = database_rq.Database()
        self.addMusicFromDatabase()


    def setupButtons(self) -> None:
        """Setup buttons"""
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




    def repeatMusic(self) -> None:
        """Change playlist state to repeat current music or not"""
        #print(self.repeat_btn.isChecked())
        if self.repeat_btn.isChecked():
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)

    def addMusicFromDatabase(self):
        """Read and add music from database"""
        x = self.database.read_music()
        for i in range(len(x)):
            if x[i][0]:
                if os.path.exists(x[i][0]):
                    self.listMusic.addItem(x[i][0])
                    self.playlist.addMedia(QMediaContent(QUrl(x[i][0])))
        for i in range(self.listMusic.count()):
            self.items.append(self.listMusic.item(i).text())

        """self.listMusic.addItems([self.database.read_music()[i][0] for i in range(len(self.database.read_music()))])
        [self.playlist.addMedia(QMediaContent(QUrl(self.database.read_music()[i][0]))) for i in range(len(self.database.read_music()))]
        for i in range(self.listMusic.count()):
            self.items.append(self.listMusic.item(i).text())"""

    def addMusicToList(self) -> None:
        """Add user selected music to list and playlist"""

        dialog = QtWidgets.QFileDialog().getOpenFileNames(directory=os.environ["USERPROFILE"] + "/Music", filter="mp3 (*.mp3);; ogg (*.ogg);; wav (*.wav)")

        self.listMusic.addItems([dialog[0][i] for i in range(len(dialog[0])) if dialog[0][i] not in self.items])
        [self.playlist.addMedia(QMediaContent(QUrl(dialog[0][i]))) for i in range(len(dialog[0])) if dialog[0][i] not in self.items]

        for i in range(self.listMusic.count()):
            if not self.database.request_select(
                    "SELECT * FROM music WHERE path='{}'".format(self.listMusic.item(i).text())):
                self.database.add_music(path=self.listMusic.item(i).text())
        del dialog

    def changeTime(self) -> None:
        """Change music position in accordance with slider"""
        self.player.setPosition(self.timeMusic.value())

    def change_volume(self) -> None:
        """Change volume"""
        if self.volume.value() <= 0:
            self.volume_icon.load("src/volume-mute-fill.svg")
        elif self.volume.value() <= 50:
            self.volume_icon.load("src/volume-down-fill.svg")
        elif self.volume.value() > 50:
            self.volume_icon.load("src/volume-up-fill.svg")
        self.player.setVolume(self.volume.value())

    def drop_all(self) -> None:
        """Setting all parameters to default"""
        self.now_pos = 0
        self.player.pause()
        self.buttonPlay.setIcon(QIcon("src/play-circle-fill.svg"))
        self.paused = True


    def setMusic(self) -> bool:
        """Set user selected music"""
        if self.listMusic.selectedItems():
            self.timeMusic.setEnabled(True)
            self.playlist.setCurrentIndex(self.listMusic.row(self.listMusic.selectedItems()[0]))
            return True
        else:
            self.timeMusic.setEnabled(False)
            return False



    def toNextTrack(self) -> None:
        """Change current music to next track"""
        if self.listMusic.count():
            x = self.listMusic.selectedItems()
            if self.listMusic.count() == self.listMusic.row(x[0]) + 1:
                self.listMusic.setCurrentRow(0)
            else:
                self.listMusic.setCurrentRow(self.listMusic.row(x[0]) + 1)
            del x
        self.drop_all()
        self.playNow()

    def toPreviousTrack(self) -> None:
        """Change current music to previous track"""
        if self.listMusic.count():
            x = self.listMusic.selectedItems()
            if self.listMusic.row(x[0]) == 0:
                self.listMusic.setCurrentRow(self.listMusic.count() - 1)
            else:
                self.listMusic.setCurrentRow(self.listMusic.row(x[0]) - 1)
        self.drop_all()
        self.playNow()

    def setDuration(self) -> None:
        """Music duration in minutes and seconds"""
        self.timeMusic.setMaximum(self.player.duration())
        seconds = int((self.player.duration() / 1000) % 60)
        minutes = int((self.player.duration() / (1000 * 60)) % 60)
        self.all_time_music.setText(f"{0 if minutes < 10 else ''}{minutes}:{0 if seconds < 10 else ''}{seconds}")
        del seconds, minutes

    def updateSlider(self) -> None:
        """Change slider position in accordance with music position"""
        self.timeMusic.setValue(self.player.position())
        seconds = int((self.player.position() / 1000) % 60)
        minutes = int((self.player.position() / (1000 * 60)) % 60)
        self.now_time_music.setText(f"{0 if minutes < 10 else ''}{minutes}:{0 if seconds < 10 else ''}{seconds}")
        del seconds, minutes


    def playNow(self) -> None:
        """Playing selected music"""
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


