#!/usr/bin/env python

from PyQt5.QtCore import QDate, QSize, Qt, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QListView, QListWidget, QListWidgetItem, QPushButton, QSpinBox,
                             QStackedWidget, QVBoxLayout, QWidget, QFileDialog, QFrame, QSpacerItem, QSizePolicy)

from bcfg.gui import configdialog_rc
import sys
from subprocess import run
from pathlib import Path
from bcfg.settings import (
    DOWNLOAD_PATH,
    CHROME_BINARY,
    CHROMIUM_BINARY,
    ALBUM_LINKS_TXT,
    TIMEOUT_TIME,
    BROWSER,
    FORMAT
)

CONFIG = {}


class ConfigurationPage(QWidget):
    def __init__(self, parent=None):
        super(ConfigurationPage, self).__init__(parent)

        pathGroup = QGroupBox("Paths")
        configGroup = QGroupBox("Scraper")
        saveGroup = QGroupBox("")

        self.saveBtn = QPushButton("Save")
        self.saveBtn.resize(25, 25)
        saveLayout = QHBoxLayout()
        saveLayout.addWidget(self.saveBtn)
        saveGroup.setLayout(saveLayout)

        self.browserPathLabel = QLabel("Browser Binary Path")
        likely_chrome_binary = Path(
            "C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
        self.browserPathSelect = QLabel(
            str(CHROME_BINARY if BROWSER == "chrome" else CHROMIUM_BINARY if BROWSER == "chromium" else likely_chrome_binary)
        )
        self.browserPathSelect.setFrameStyle(
            QFrame.Sunken | QFrame.Panel
        )
        self.browserPathSelect.setFixedHeight(20)
        self.browserPathButton = QPushButton("Select")
        browserPathLayout = QHBoxLayout()
        browserPathLayout2 = QHBoxLayout()
        browserPathLayout.addWidget(self.browserPathLabel)
        browserPathLayout.addWidget(self.browserPathButton)
        browserPathLayout2.addWidget(self.browserPathSelect)

        self.downloadPathLabel = QLabel("Download Path:")
        self.downloadPathSelect = QLabel(
            Path.home().joinpath("Downloads").__str__()
        )
        self.downloadPathSelect.setFrameStyle(
            QFrame.Sunken | QFrame.Panel
        )
        self.downloadPathSelect.setFixedHeight(20)
        self.downloadPathButton = QPushButton("Select")
        downloadPathLayout = QHBoxLayout()
        downloadPathLayout2 = QHBoxLayout()
        downloadPathLayout.addWidget(self.downloadPathLabel)
        downloadPathLayout.addWidget(self.downloadPathButton)
        downloadPathLayout2.addWidget(self.downloadPathSelect)

        # ################################
        formatLabel = QLabel("File Type to Get:")
        self.formatCombo = QComboBox()
        self.formatCombo.addItem("flac")
        self.formatCombo.addItem("mp3")
        self.formatCombo.addItem("mp3-vo")
        self.formatCombo.addItem("mp3-320")
        self.formatCombo.addItem("vorbis")
        formatLayout = QHBoxLayout()
        formatLayout.addWidget(formatLabel)
        formatLayout.addWidget(self.formatCombo)

        timeoutLabel = QLabel("Timeout (Seconds):")
        self.timeoutEdit = QSpinBox()  # Make this an Integer
        self.timeoutEdit.setMaximum(1000000)
        self.timeoutEdit.setValue(int(TIMEOUT_TIME))
        self.timeoutEdit.setMinimum(1)
        timeoutLayout = QHBoxLayout()
        timeoutLayout.addWidget(timeoutLabel)
        timeoutLayout.addWidget(self.timeoutEdit)

        browserLabel = QLabel("Browser Flavor?")
        self.browserCombo = QComboBox()
        self.browserCombo.addItem("chrome")
        self.browserCombo.addItem("chromium")
        browserLayout = QHBoxLayout()
        browserLayout.addWidget(browserLabel)
        browserLayout.addWidget(self.browserCombo)
        # ##################################

        self.downloadPathButton.clicked.connect(
            self.setDownloadDirectory
        )

        self.browserPathButton.clicked.connect(
            self.setBrowserBinary
        )

        self.saveBtn.clicked.connect(
            self.saveConfig
        )

        pathLayout = QVBoxLayout()
        pathLayout.addLayout(browserPathLayout)
        pathLayout.addLayout(browserPathLayout2)
        pathLayout.addSpacing(20)
        pathLayout.addLayout(downloadPathLayout)
        pathLayout.addLayout(downloadPathLayout2)

        pathGroup.setLayout(pathLayout)

        configLayout = QVBoxLayout()
        configLayout.addLayout(formatLayout)
        configLayout.addLayout(timeoutLayout)
        configLayout.addLayout(browserLayout)

        configGroup.setLayout(configLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(configGroup)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(pathGroup)
        mainLayout.addSpacing(25)
        mainLayout.addWidget(saveGroup)
        mainLayout.addSpacing(10)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    def setDownloadDirectory(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select a directory to download albums to...",
            directory=self.downloadPathButton.text(),
            options=options
        )
        if directory:
            self.downloadPathSelect.setText(directory)

    def setBrowserBinary(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="QFileDialog.getOpenFileName()",
            directory=self.browserPathButton.text(),
            options=options
        )
        if fileName:
            self.browserPathSelect.setText(fileName)

    def saveConfig(self):
        global CONFIG
        CONFIG = {
            'format': self.formatCombo.currentText(),
            'browser': self.browserCombo.currentText(),
            'timeout': int(self.timeoutEdit.value()),
            'download': self.downloadPathSelect.text(),
            'binary': self.browserPathSelect.text()
        }


class DownloadPage(QWidget):
    def __init__(self, parent=None):
        super(DownloadPage, self).__init__(parent)

        pathGroup = QGroupBox("Album URLs")
        urlGroup = QGroupBox("Loaded Album URLs")

        self.browserPathLabel = QLabel("Links Text File")

        self.browserPathSelect = QLabel(
            str(ALBUM_LINKS_TXT)
        )
        self.browserPathSelect.setFrameStyle(
            QFrame.Sunken | QFrame.Panel
        )
        self.browserPathSelect.setFixedHeight(20)
        self.browserPathButton = QPushButton("Select")
        browserPathLayout = QHBoxLayout()
        browserPathLayout2 = QHBoxLayout()
        browserPathLayout.addWidget(self.browserPathLabel)
        browserPathLayout.addWidget(self.browserPathButton)
        browserPathLayout2.addWidget(self.browserPathSelect)

        self.browserPathButton.clicked.connect(
            self.setAlbumsTxt
        )

        pathLayout = QVBoxLayout()
        pathLayout.addLayout(browserPathLayout)
        pathLayout.addLayout(browserPathLayout2)
        pathGroup.setLayout(pathLayout)

        urlList = QListWidget()
        urlList.setObjectName("urlList")
        with open(self.browserPathSelect.text(), 'r') as lines:
            for line in lines:
                urlList.addItem(line)

        self.startDownloadButton = QPushButton("Start Downloading")

        self.startDownloadButton.clicked.connect(
            self.executeConfig
        )

        downloadGroup = QGroupBox("Download")
        downloadLayout = QVBoxLayout()
        downloadLayout.addWidget(self.startDownloadButton)
        downloadGroup.setLayout(downloadLayout)

        urlLayout = QVBoxLayout()
        urlLayout.addWidget(urlList)
        urlGroup.setLayout(urlLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(pathGroup)
        mainLayout.addWidget(urlGroup)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(downloadGroup)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

    def setAlbumsTxt(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()",
            self.browserPathButton.text(),
            "Text Files (*.txt)",
            options=options
        )
        if fileName:
            self.browserPathSelect.setText(fileName)

    def executeConfig(self):
        cmd = rf"python  .\bandcamp_flac_get.py  -i  {self.browserPathSelect.text()}" \
              + f"  -o  {CONFIG['download']}  --{CONFIG['browser']}  {CONFIG['binary']}" \
              + f"  -f  {CONFIG['format']}  -t  {CONFIG['timeout']}"
        list_cmd = cmd.split("  ")
        print(list_cmd)
        run(list_cmd, shell=True, timeout=None)
        sys.exit(0)


class HelpPage(QWidget):
    def __init__(self, parent=None):
        super(HelpPage, self).__init__(parent)

        aboutGroup = QGroupBox("About BCFG")

        aboutLabel = QLabel("""
        dsf
        dsf
        ds
        fds
        fds
        fdas
        fds
        """)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(aboutGroup)
        mainLayout.addWidget(aboutLabel)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)

        self.contentsWidget = QListWidget()
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setIconSize(QSize(96, 84))
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setMaximumWidth(128)
        self.contentsWidget.setSpacing(12)

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(ConfigurationPage())
        self.pagesWidget.addWidget(DownloadPage())
        self.pagesWidget.addWidget(HelpPage())

        closeButton = QPushButton("Close")

        self.createIcons()
        self.contentsWidget.setCurrentRow(0)

        closeButton.clicked.connect(self.close)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.contentsWidget)
        horizontalLayout.addWidget(self.pagesWidget, 1)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(closeButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)

        self.setWindowTitle("bandcamp-flac-get.py")

    def changePage(self, current, previous):
        if not current:
            current = previous

        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))

    def createIcons(self):
        configButton = QListWidgetItem(self.contentsWidget)
        configButton.setIcon(QIcon(':/images/config.png'))
        configButton.setText("Configuration")
        configButton.setTextAlignment(Qt.AlignHCenter)
        configButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        updateButton = QListWidgetItem(self.contentsWidget)
        updateButton.setIcon(QIcon(':/images/update.png'))
        updateButton.setText("Download")
        updateButton.setTextAlignment(Qt.AlignHCenter)
        updateButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        queryButton = QListWidgetItem(self.contentsWidget)
        queryButton.setIcon(QIcon(':/images/query.png'))
        queryButton.setText("Help")
        queryButton.setTextAlignment(Qt.AlignHCenter)
        queryButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.contentsWidget.currentItemChanged.connect(self.changePage)


def GUI():
    import sys

    app = QApplication(sys.argv)
    conf = ConfigDialog()
    sys.exit(conf.exec_())


if __name__ == '__main__':
    GUI()
