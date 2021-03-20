# --------------------------------------------------------------- #
#       Copyright 2021, Abanob Ashraf, All rights reserved.       #
# --------------------------------------------------------------- #

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from powerPad_ui import Ui_MainWindow as userInterface
import os
import time


class Ui_MainWindow(QMainWindow, userInterface):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.sideBanal.setVisible(False)
        self.loadingFrame.setVisible(False)
        self.textBar.setVisible(False)
        self.setWindowTitle('PowerPad IDE - Abanob Ashraf')

        self.msg = QMessageBox()
        self.file = QFileDialog()

        self.actionNewFile.triggered.connect(self.new)
        self.actionSave.triggered.connect(self.prompt)
        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenFolder.triggered.connect(self.selectFolder)
        self.actionPrint.triggered.connect(self.printTool)
        self.actionExport.triggered.connect(self.exportPDF)
        self.actionExit.triggered.connect(lambda: self.close())

        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionSelectAll.triggered.connect(self.textEdit.selectAll)
        self.actionInsertImage.triggered.connect(self.insertImage)

        self.actionTextBar.triggered.connect(self.toggleTextBar)
        self.actionSideBar.triggered.connect(self.toggleSideBar)
        self.actionToolBar.triggered.connect(self.toggleToolBar)
        self.actionMenuBar.triggered.connect(self.toggleMenuBar)

        self.actionStyle.triggered.connect(self.fontStyle)
        self.actionColor.triggered.connect(self.fontColor)
        self.actionBold.triggered.connect(self.fontBold)
        self.actionItalic.triggered.connect(self.fontItalic)
        self.actionUnderline.triggered.connect(self.fontUnderline)
        self.actionhighlighter.triggered.connect(self.fontHighlight)

        self.actionLeft.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignLeft))
        self.actionCenter.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignCenter))
        self.actionRight.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignRight))
        self.actionJustify.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignJustify))
        self.actionAbout.triggered.connect(self.about)

        self.actionZoomIn.triggered.connect(self.fontSizeIN)
        self.actionZoomOut.triggered.connect(self.fontSizeOUT)

    def about(self):
        box = QMessageBox()
        box.about(self, 'PowerPad v1', 'Registered and Created by : Abanob Ashraf Shoukry\nCode : 619082')

    def prompt(self):
        # we will show popup message box when save was triggered
        self.msg.setText("Do you want to save the file?")
        self.msg.setIcon(self.msg.Information)
        self.msg.setWindowTitle("Super Notepad")
        self.msg.setStandardButtons(self.msg.Yes | self.msg.No)
        retrieved = self.msg.exec_()
        if retrieved == 16384:
            self.saveAs()
        elif retrieved == 65536:
            pass

    def writer(self, filename):
        data = self.textEdit.toHtml()
        with open(filename, 'w') as file:
            file.write(data)

    def saveAs(self):
        filename, _ = self.file.getSaveFileName()
        if filename != '':
            if '.Pp' not in filename:
                filename = filename+'.Pp'
            self.writer(filename)
            filename = os.path.basename(filename)
            filename, _ = os.path.splitext(filename)
            filetype = filename + ' - Mini Python Ide'
            self.setWindowTitle(os.path.basename(filetype))

    def openFile(self):
        fileSelect = QFileDialog.getOpenFileName(self, 'Open File')
        if os.path.exists(fileSelect[0]):
            self.loadingMethod()
            with open(fileSelect[0], "r") as file:
                ext = fileSelect[0].split('.')[1]
                if ext == 'Pp':
                    text = file.read()
                    self.textEdit.setHtml(text)
                else:
                    text = file.read()
                    self.textEdit.setPlainText(text)
        else:
            print("SELECT FILE !")

    def selectFolder(self):
        path = QFileDialog.getExistingDirectory(self, "select folder", "./")
        if os.path.isdir(path):
            model = QFileSystemModel()
            model.setRootPath((QtCore.QDir.rootPath()))
            self.loadingMethod()
            self.sideBanal.setVisible(True)
            self.treeView.setModel(model)
            self.treeView.setRootIndex(model.index(path))
            self.treeView.clicked.connect(lambda: self.treeModel(model))
            self.treeView.hideColumn(1)
            self.treeView.hideColumn(2)
            self.treeView.hideColumn(3)
        else:
            pass

    def treeModel(self, m):
        try:
            index = self.treeView.currentIndex()
            file_path = m.filePath(index)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    txt = file.read()
                    self.textEdit.setPlainText(str(txt))
        except Exception as a:
            print(a)

    def loadingMethod(self):
        try:
            self.loadingFrame.setVisible(True)
            count = 0
            while count < 100:
                count += 1
                time.sleep(0.0000000000000001)
                self.progressBar.setValue(count)
            time.sleep(0.005)
            self.loadingFrame.setVisible(False)
            QApplication.processEvents()
        except Exception as a:
            print(a)

    def printTool(self):
        printer = QPrinter(QPrinter.HighResolution)
        # dialog = QPrintDialog(printer, self)
        dialog = QPrintPreviewDialog(printer, self)
        dialog.paintRequested.connect(lambda: self.textEdit.print_(printer))
        dialog.exec_()
        # if dialog.exec_() == QPrintDialog.Accepted:
        #     self.textEdit.print_(printer)

    def exportPDF(self):
        dialog, _ = QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF Files (*.pdf) ;; All Files (*.*)')
        if dialog != '':
            if QFileInfo(dialog).suffix() == '':
                dialog += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(dialog)
            self.loadingMethod()
            self.textEdit.document().print_(printer)

    def insertImage(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image', ".", "Images(*.png *.xpm *.jpg *.bmp *.gif)")[0]
        if filename:
            photo = QtGui.QImage(filename)
            # Error
            if photo.isNull():
                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                              "Image load error",
                                              "Could not load image file!",
                                              QtWidgets.QMessageBox.Ok,
                                              self)
                popup.show()
            else:
                cursor = self.textEdit.textCursor()
                cursor.insertImage(photo, filename)

    def new(self):
        self.loadingMethod()
        new = Ui_MainWindow()
        new.show()

    def fontSizeIN(self):
        num = self.textEdit.fontPointSize()
        self.textEdit.setFontPointSize(num + 10)

    def fontSizeOUT(self):
        num = self.textEdit.fontPointSize()
        self.textEdit.setFontPointSize(num - 10)

    def fontStyle(self):
        style, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(style)

    def fontColor(self):
        color = QtWidgets.QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def fontBold(self):
        if self.textEdit.fontWeight() == QtGui.QFont.Bold:
            self.textEdit.setFontWeight(QtGui.QFont.Normal)
        else:
            self.textEdit.setFontWeight(QtGui.QFont.Bold)

    def fontItalic(self):
        state = self.textEdit.fontItalic()
        self.textEdit.setFontItalic(not state)

    def fontUnderline(self):
        state = self.textEdit.fontUnderline()
        self.textEdit.setFontUnderline(not state)

    def fontHighlight(self):
        color = QtWidgets.QColorDialog.getColor()
        self.textEdit.setTextBackgroundColor(color)

    def strike(self):
        txt = self.textEdit.currentCharFormat()
        txt.setFontStrikeOut(not txt.fontStrikeOut())
        self.textEdit.setCurrentCharFormat(txt)

    def toggleToolBar(self):
        state = self.toolBar.isVisible()
        self.toolBar.setVisible(not state)

    def toggleSideBar(self):
        state = self.sideBanal.isVisible()
        self.sideBanal.setVisible(not state)

    def toggleTextBar(self):
        state = self.textBar.isVisible()
        self.textBar.setVisible(not state)

    def toggleMenuBar(self):
        state = self.menuBar.isVisible()
        self.menuBar.setVisible(not state)
        if state:
            self.actionMenuBar.setIcon(QtGui.QIcon(":/new/light/icons/white/icons8_chevron_down_30px.png"))
        else:
            self.actionMenuBar.setIcon(QtGui.QIcon(":/new/light/icons/white/icons8_chevron_up_30px.png"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
