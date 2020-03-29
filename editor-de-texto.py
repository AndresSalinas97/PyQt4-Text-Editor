#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Práctica 2 de ISSBC.

Editor de ficheros de texto que permite abrir una carpeta y mostrar los ficheros
dentro de ella en un panel lateral para poder abrirlos fácilmente con tan solo
seleccionarlos y pulsar un botón.

Author: Andrés Salinas Lima <i52salia@uco.es>
"""

import sys
import os
from PyQt4 import QtCore
from PyQt4 import QtGui


class TextEditor(QtGui.QWidget):
    """
    Clase TextEditor: QWidget con la interfaz y lógica del editor de texto.

    Atributos:
        _COLUMN_0_FIXED_WIDTH: Anchura de la primera columna del layout (lista
            de ficheros).
        _COLUMN_2_MIN_WIDTH: Anchura mínima de la tercera columna del layout 
            (editor de texto).
        _ROW_2_MIN_HEIGHT: Altura mínima de la segunda fila (lista de ficheros y 
            editor de texto)
    """

    def __init__(self):
        """
        Constructor de la clase TextEditor.
        """
        super(TextEditor, self).__init__()

        self._COLUMN_0_FIXED_WIDTH = 250
        self._COLUMN_2_MIN_WIDTH = 500
        self._ROW_2_MIN_HEIGHT = 300

        self.initUI()

        # El editor se abrirá con el directorio actual (.) cargado
        self._openThisFolder(".")

    def initUI(self):
        """
        Inicialización de la interfaz.
        """
        ##### Etiquetas #####
        # En realidad son campos de texto de una línea (QtGui.QLineEdit)
        # configurados como solo lectura ya que las etiquetas (QtGui.QLabel)
        # dan muchos problemas cuando contienen texto de longitud variable pero
        # la etiqueta dispone de un espacio limitado.
        self._openedFolderLabel = QtGui.QLineEdit()
        self._openedFolderLabel.setReadOnly(True)
        self._openedFolderLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._openedFolderLabel.setFixedWidth(self._COLUMN_0_FIXED_WIDTH)
        self._openedFolderLabel.setStatusTip("Ruta de la carpeta abierta")

        self._openedFileLabel = QtGui.QLineEdit()
        self._openedFileLabel.setReadOnly(True)
        self._openedFileLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._openedFileLabel.setMinimumWidth(self._COLUMN_2_MIN_WIDTH)
        self._openedFileLabel.setStatusTip("Ruta del fichero abierto")

        ##### Lista de ficheros #####
        self._fileList = QtGui.QListWidget()
        self._fileList.setFixedWidth(self._COLUMN_0_FIXED_WIDTH)
        self._fileList.setMinimumHeight(self._ROW_2_MIN_HEIGHT)
        # Mostramos siempre las barras de scroll para evitar bug en el que
        # dichas barras de scroll no aparecen cuando deberían
        self._fileList.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self._fileList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self._fileList.setStatusTip("Ficheros de la carpeta abierta")

        ##### Editor de texto #####
        self._textEdit = QtGui.QTextEdit()
        self._textEdit.setMinimumWidth(self._COLUMN_2_MIN_WIDTH)
        self._textEdit.setMinimumHeight(self._ROW_2_MIN_HEIGHT)
        self._textEdit.setStatusTip("Fichero abierto")

        ##### Botón #####
        arrowButton = QtGui.QPushButton(">>>", self)
        arrowButton.clicked.connect(self.openSelectedFile)
        arrowButton.setStatusTip("Abrir el fichero seleccionado")

        ##### Configuración grid layout #####
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self._openedFolderLabel, 0, 0)
        grid.addWidget(self._openedFileLabel, 0, 2)
        grid.addWidget(self._fileList, 1, 0)
        grid.addWidget(arrowButton, 1, 1)
        grid.addWidget(self._textEdit, 1, 2)

        self.setLayout(grid)

    def openFolderDialog(self):
        """
        Muestra una ventana de diálogo para elegir la carpeta que se abrirá.
        """
        # Ventana de diálogo para seleccionar la carpeta
        folderPath = QtGui.QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta")

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado una carpeta
        if(folderPath):
            self._openThisFolder(folderPath)

    def _openThisFolder(self, folderPath):
        """
        Abre la carpeta indicada en el argumento folderPath para mostrar todos
        sus ficheros en la lista de ficheros del editor.
        """
        try:
            folderPath = str(folderPath)
            folderPath = os.path.abspath(folderPath)

            # Obtenemos una lista con los ficheros de la carpeta
            listOfFiles = self._listNotHiddenFiles(folderPath)

            self._fileList.clear()  # Limpia la lista
            self._fileList.addItems(listOfFiles)  # Añade a la lista
            self._fileList.sortItems()  # Ordena alfabéticamente la lista

            # Añadimos el separador de fichero ('/' en Linux y Mac, '\' en
            # Windows) al final de la ruta que se almacena en la etiqueta
            if (folderPath[-1] != os.path.sep):
                self._openedFolderLabel.setText(folderPath + os.path.sep)
            else:
                self._openedFolderLabel.setText(folderPath)

        except:
            self._showErrorMessage("No se pudo abrir la carpeta \"" +
                                   folderPath + "\"")

    def openFileDialog(self):
        """
        Muestra una ventana de diálogo para elegir fichero que se abrirá.
        """
        # Ventana de diálogo para seleccionar el fichero
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Abrir fichero")

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado un fichero
        if(filePath):
            self._openThisFile(filePath)

    def openSelectedFile(self):
        """
        Abre el fichero seleccionado en la lista de ficheros.
        """
        selectedFiles = self._fileList.selectedItems()

        if (not selectedFiles):
            self._showErrorMessage("Primero debe seleccionar un fichero en el"
                                   "menu de la izquierda!")

        filePath = self._openedFolderLabel.text() + selectedFiles[0].text()

        self._openThisFile(filePath)

    def _openThisFile(self, filePath):
        """
        Abre el fichero indicado en el argumento filePath.
        """
        try:
            file = open(filePath, 'r')
            with file:
                data = file.read()

                self._textEdit.setText(data)
                self._openedFileLabel.setText(filePath)

                file.close()
        except:
            self._showErrorMessage("No se pudo abrir el fichero \"" +
                                   filePath + "\"")

    def saveOpenedFile(self):
        """
        Guarda el archivo abierto.

        Si no hay ningún archivo abierto, es decir, la etiqueta que indica el
        fichero abierto _openedFileLabel está vacía, se abrirá la ventana de
        diálogo de Guardar Como...
        """
        if (not self._openedFileLabel.text()):
            self.saveAsDialog()
        else:
            self._saveInThisFile(self._openedFileLabel.text())

    def saveAsDialog(self):
        """
        Muestra una ventana de diálogo para elegir dónde se guardará el fichero.
        """
        # Ventana de diálogo para seleccionar dónde se guardará el fichero
        filePath = QtGui.QFileDialog.getSaveFileName(self, 'Guardar Como...')

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado un fichero
        if(filePath):
            self._saveInThisFile(filePath)

    def _saveInThisFile(self, filePath):
        """
        Guarda el archivo abierto en la ruta indicada en el argumento filePath.
        """
        try:
            file = open(filePath, "w")

            data = self._textEdit.toPlainText()

            file.write(data)

            file.close()

            self._openedFileLabel.setText(filePath)

            self._showInfoMessage("Fichero guardado con exito!")
        except:
            self._showErrorMessage("No se pudo guardar en el fichero \"" +
                                   filePath + "\"")

    def _showErrorMessage(self, errorText):
        """
        Muestra una ventana emergente de error con el mensaje indicado en
        el argumento errorText.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QtGui.QMessageBox.Critical)
        msg.setText(errorText)
        msg.exec_()

    def _showInfoMessage(self, infoText):
        """
        Muestra una ventana emergente de información con el mensaje indicado en
        el argumento infoText.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle("Informacion")
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(infoText)
        msg.exec_()

    def _listNotHiddenFiles(self, folderPath):
        """
        Devuelve una lista con los nombres de los ficheros no ocultos dentro de
        la carpeta indicada en el argumento folderPath.
        """
        list = []

        for f in os.listdir(folderPath):
            if (os.path.isfile(os.path.join(folderPath, f))):  # Si es fichero...
                if (not f.startswith('.')):  # ... y no está oculto...
                    list.append(f)  # ... lo añadimos a la lista

        return list


class MainWindow(QtGui.QMainWindow):
    """
    Ventana principal del programa.

    Contiene la barra de menús, la barra de herramientas, la barra de estado, y,
    por supuesto, el widget con el editor de texto.

    Atributos:
        textEditor: Widget con el editor de texto (objeto textEditor de la clase
            TextEditor)
    """

    def __init__(self, textEditor):
        """
        Constructor de la clase MainWindow.

        Argumentos:
            textEditor: Widget con el editor de texto (objeto textEditor de la
                clase TextEditor)
        """
        super(MainWindow, self).__init__()

        self.textEditor = textEditor

        self.initUI()

    def initUI(self):
        """
        Inicialización de la interfaz.
        """

        ##### Acciones #####
        exitAction = QtGui.QAction("Salir", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip("Salir del programa")
        exitAction.triggered.connect(QtGui.qApp.closeAllWindows)

        openFileAction = QtGui.QAction("Abrir Fichero", self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.setStatusTip("Abrir fichero")
        openFileAction.triggered.connect(self.textEditor.openFileDialog)

        openFolderAction = QtGui.QAction("Abrir Carpeta", self)
        openFolderAction.setShortcut('Ctrl+Shift+O')
        openFolderAction.setStatusTip("Abrir carpeta")
        openFolderAction.triggered.connect(self.textEditor.openFolderDialog)

        saveFileAction = QtGui.QAction("Guardar", self)
        saveFileAction.setShortcut('Ctrl+S')
        saveFileAction.setStatusTip("Guardar cambios del fichero abierto")
        saveFileAction.triggered.connect(self.textEditor.saveOpenedFile)

        saveAsAction = QtGui.QAction("Guardar Como...", self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.setStatusTip("Guardar cambios del fichero abierto en un"
                                  " nuevo fichero")
        saveAsAction.triggered.connect(self.textEditor.saveAsDialog)

        ##### Barra de menús #####
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&Archivo')
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(openFolderAction)
        fileMenu.addSeparator()
        fileMenu.addAction(saveFileAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        ##### Barra de herramientas #####
        toolBar = self.addToolBar("Barra de Herramientas")
        toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolBar.addAction(openFileAction)
        toolBar.addAction(openFolderAction)
        toolBar.addAction(saveFileAction)
        toolBar.addAction(saveAsAction)

        ##### Barra de estado #####
        self.statusBar()  # Activa la barra de estado

        ##### Widget contador #####
        # Añade a la ventana principal el contador
        self.setCentralWidget(self.textEditor)

        ##### Propiedades ventana #####
        self.setWindowTitle("Editor de Texto")


def main():
    """
    Main: Inicia el programa.
    """

    app = QtGui.QApplication(sys.argv)

    textEditor = TextEditor()

    mainWindow = MainWindow(textEditor)
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()  # Si ejecutamos este módulo se llamará a main()
