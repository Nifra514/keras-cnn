import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
import sys
from PyQt5.uic import loadUi
import os
 
class VideoWindow(QtWidgets.QMainWindow):
 
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player") 
        
        self.mediaPlayer = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
 
        videoWidget = QtMultimediaWidgets.QVideoWidget()
 
        self.playButton = QtWidgets.QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
 
        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
 
        self.errorLabel = QtWidgets.QLabel()
        self.errorLabel.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Maximum)
 
        # Create new action
        # openAction = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open', self)        
        # openAction.setShortcut('Ctrl+O')
        # openAction.setStatusTip('Open movie')
        # openAction.triggered.connect(self.openFile)

        # Create new action
        setAction = QtWidgets.QAction(QtGui.QIcon('st.png'), '&Set Video', self)        
        setAction.setShortcut('Ctrl+E')
        setAction.setStatusTip('Set video')
        setAction.triggered.connect(self.setVid)

        # Create new action
        exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)  
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)
 
        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(setAction)
        fileMenu.addAction(exitAction)
 
        # Create a widget for window contents
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
 
        # Create layouts to place inside widget
        controlLayout = QtWidgets.QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
 
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
 
        # Set widget to contain window contents
        wid.setLayout(layout)
 
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
 
    def setVid(self):
        bpath = os.getcwd()
        fpath = 'Video'
        path = os.path.join(bpath,fpath,'1_9 and A_Z.mp4')
        # print (path)
        selFile = QtWidgets.QFileDialog.selectFile = path
        if selFile != '':
            self.mediaPlayer.setMedia(
                    QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(selFile)))
            self.playButton.setEnabled(True)
 
    def exitCall(self):
        self.close()
        
    def play(self):

        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
 
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
 
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
 
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
 
    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

# class main(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(main,self).__init__()
#         loadUi('UI/main.ui',self)
 
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
 


