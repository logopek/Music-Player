from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAbstractItemView, QMainWindow


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(320, 463)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.all_time_music = QtWidgets.QLabel(self.centralwidget)
        self.all_time_music.setText("")
        self.all_time_music.setGeometry(QtCore.QRect(285, 190, 75, 23))
        self.all_time_music.setObjectName("all_time_music")

        self.now_time_music = QtWidgets.QLabel(self.centralwidget)
        self.now_time_music.setText("")
        self.now_time_music.setGeometry(QtCore.QRect(10, 190, 75, 23))
        self.now_time_music.setObjectName("now_time_music")

        self.volume = QtWidgets.QSlider(self.centralwidget)
        self.volume.setGeometry(QtCore.QRect(241, 220, 70, 22))
        self.volume.setOrientation(QtCore.Qt.Horizontal)
        self.volume.setMinimum(-2)
        self.volume.setMaximum(102)
        self.volume.setValue(100)
        self.volume_icon = QtSvg.QSvgWidget("src/volume-up-fill.svg", parent=self.centralwidget)
        self.volume_icon.setGeometry(210, 215, 30, 30)

        self.addMusic = QtWidgets.QPushButton(self.centralwidget)
        self.addMusic.setGeometry(QtCore.QRect(0, 220, 75, 23))
        self.addMusic.setObjectName("addMusic")

        self.repeat_btn = QtWidgets.QCheckBox(self.centralwidget)
        self.repeat_btn.setIcon(QIcon("src/repeat-1.svg"))
        self.repeat_btn.setGeometry(QtCore.QRect(170, 220, 40, 20))

        self.listMusic = QtWidgets.QListWidget(self.centralwidget)
        self.listMusic.setGeometry(QtCore.QRect(0, 250, 321, 192))
        self.listMusic.setObjectName("listMusic")
        self.listMusic.setSelectionMode(QAbstractItemView.SingleSelection)
        self.buttonPlay = QtWidgets.QPushButton(self.centralwidget)
        self.buttonPlay.setGeometry(QtCore.QRect(130, 60, 71, 71))
        self.buttonPlay.setObjectName("buttonPlay")

        self.nextTrack = QtWidgets.QPushButton(self.centralwidget)
        self.nextTrack.setGeometry(QtCore.QRect(240, 70, 51, 51))
        self.nextTrack.setObjectName("nextTrack")

        self.previousTrack = QtWidgets.QPushButton(self.centralwidget)
        self.previousTrack.setGeometry(QtCore.QRect(40, 70, 51, 51))
        self.previousTrack.setObjectName("previousTrack")

        self.timeMusic = QtWidgets.QSlider(self.centralwidget)
        self.timeMusic.setGeometry(QtCore.QRect(10, 170, 301, 22))
        self.timeMusic.setOrientation(QtCore.Qt.Horizontal)
        self.timeMusic.setObjectName("timeMusic")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Music Player", "Music Player"))
        MainWindow.setWindowIcon(QIcon("src/music-note-beamed.svg"))
        self.addMusic.setText(_translate("MainWindow", "Add Music"))

        __sortingEnabled = self.listMusic.isSortingEnabled()
        self.listMusic.setSortingEnabled(False)
        self.listMusic.setSortingEnabled(__sortingEnabled)

        self.buttonPlay.setText(_translate("", ""))
        self.buttonPlay.setIcon(QIcon("src/play-circle-fill.svg"))
        self.buttonPlay.setIconSize(QtCore.QSize(71, 71))

        self.nextTrack.setText(_translate("MainWindow", ""))
        self.nextTrack.setIcon(QIcon("src/skip-forward-fill.svg"))
        self.nextTrack.setIconSize(QtCore.QSize(40, 40))

        self.previousTrack.setText(_translate("MainWindow", ""))
        self.previousTrack.setIcon(QIcon("src/skip-backward-fill.svg"))
        self.previousTrack.setIconSize(QtCore.QSize(40, 40))

        self.addMusic.setIcon(QIcon("src/music-note-list.svg"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("src/music-note-beamed.svg"))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
