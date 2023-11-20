from lib.bg3lt_core import Initializer as Core
import sys
from PyQt5 import QtGui as Layout
from PyQt5 import QtWidgets as Widgets


class WindowInstance(Widgets.QWidget):
    def __init__(self):
        super().__init__()
        self.fileName = None
        self.messageBox = None
        self.fileExport = None
        self.localisationApplication = None
        self.coreInstance = None
        self.window = None
        self.subWindow = None
        self.filePath = None
        self.fileSelect = None
        self.leftEditor = None
        self.rightEditor = None
        self.lineHeight = None
        self.genWindowInstance()

    def genWindowInstance(self):
        # 创建窗口实例
        self.window = Widgets.QVBoxLayout(self)

        # 初始化功能核心
        self.coreInstance = Core()
        config = self.coreInstance.configs

        # 定义窗口信息
        self.localisationApplication = self.coreInstance.localisation['application']
        self.setWindowTitle(self.localisationApplication['title'])
        self.setGeometry(100, 100, config['resolutionX'], config['resolutionY'])

        # 添加元件 - 选择文件
        self.filePath = Widgets.QPlainTextEdit(parent=self)
        self.filePath.setGeometry(0, 0, 100, 30)
        self.fileSelect = Widgets.QPushButton(self.localisationApplication['fileSelect'], self)
        self.fileSelect.clicked.connect(self.openFileDialog)

        # 获取文字高度 设置为1.5倍行高
        fontMetrics = Layout.QFontMetrics(self.filePath.font())
        self.lineHeight = fontMetrics.height()
        self.filePath.setFixedHeight(round(self.lineHeight / 2 * 3))

        # 创建编辑栏
        self.subWindow = Widgets.QHBoxLayout()
        self.rightEditor = Widgets.QPlainTextEdit(parent=self)
        self.leftEditor = Widgets.QPlainTextEdit(parent=self)
        self.leftEditor.setReadOnly(True)
        self.subWindow.addWidget(self.leftEditor)
        self.subWindow.addWidget(self.rightEditor)

        # 创建输出按钮
        self.fileExport = Widgets.QPushButton(self.localisationApplication['fileExport'], self)
        self.fileExport.clicked.connect(self.exportTranslatedFile)

        # 添加控件进入窗口
        self.window.addWidget(self.filePath)
        self.window.addWidget(self.fileSelect)
        self.window.addLayout(self.subWindow)
        self.window.addWidget(self.fileExport)
        self.setLayout(self.window)

        # 显示窗口
        self.show()

    def exportTranslatedFile(self):
        self.coreInstance.doneText = self.rightEditor.toPlainText()
        if self.coreInstance.checkLengthPassed():
            self.coreInstance.prepareExportFile(self.fileName)
            self.messageBox = Widgets.QMessageBox(parent=self)
            self.messageBox.about(self, self.localisationApplication['exportAction'],
                                  self.localisationApplication['exportSuccessfully'])
        else:
            self.messageBox = Widgets.QMessageBox(parent=self)
            self.messageBox.warning(self, self.localisationApplication['exportAction'],
                                    self.localisationApplication['lengthNotMatch'])

    def openFileDialog(self):
        filename, _ = Widgets.QFileDialog.getOpenFileName(filter='')
        if filename:
            self.coreInstance.processOriginalFile(filename)
            self.filePath.insertPlainText(filename)
            self.fileName = filename
            self.leftEditor.insertPlainText(self.coreInstance.rawText)
            self.rightEditor.insertPlainText(self.coreInstance.rawText)
        else:
            return False


if __name__ == '__main__':
    application = Widgets.QApplication(sys.argv)
    window = WindowInstance()
    sys.exit(application.exec_())
