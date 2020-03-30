#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con la vista del editor de texto.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui


class TextEditorView():
    """
    Clase TextEditorView: Vista del editor de texto.

    Atributos:
        widget: QWidget con la interfaz del editor de texto (objeto de la clase
            TextEditorWidget).
        mainWindow: Ventana principal (objeto de la clase TextEditorMainWindow).
    """

    def __init__(self):
        self.widget = TextEditorWidget()
        self.mainWindow = TextEditorMainWindow(self.widget)

    def show(self):
        """
        Hace visible la ventana principal.
        """
        self.mainWindow.show()


class TextEditorWidget(QtGui.QWidget):
    """
    Clase TextEditorWidget: QWidget con la interfaz del editor de texto.

    Atributos:
        openedFolderLabel: QLineEdit que muestra la ruta de la carpeta abierta.
        openedFileLabel: QLineEdit que muestra la ruta del fichero abierto.
        fileList: QListWidget que muestra la lista de ficheros de la carpeta.
        textEdit: QTextEdit para mostrar/editar el fichero.
        arrowButton: QPushButton para abrir el fichero seleccionado.
    """

    def __init__(self):
        super(TextEditorWidget, self).__init__()

        # Anchura de la primera columna del layout (lista de ficheros).
        self._COLUMN_0_FIXED_WIDTH = 250
        # Anchura mínima de la tercera columna del layout (editor de texto).
        self._COLUMN_2_MIN_WIDTH = 500
        # Altura mínima de la segunda fila (lista de ficheros y editor de texto).
        self._ROW_2_MIN_HEIGHT = 300

        self._initUI()

    def _initUI(self):
        """
        Inicialización de la interfaz.
        """
        ##### Etiquetas #####
        # En realidad son campos de texto de una línea (QtGui.QLineEdit)
        # configurados como solo lectura ya que las etiquetas (QtGui.QLabel)
        # dan muchos problemas cuando contienen texto de longitud variable pero
        # la etiqueta dispone de un espacio limitado.
        self.openedFolderLabel = QtGui.QLineEdit()
        self.openedFolderLabel.setReadOnly(True)
        self.openedFolderLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.openedFolderLabel.setFixedWidth(self._COLUMN_0_FIXED_WIDTH)
        self.openedFolderLabel.setStatusTip("Ruta de la carpeta abierta")

        self.openedFileLabel = QtGui.QLineEdit()
        self.openedFileLabel.setReadOnly(True)
        self.openedFileLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.openedFileLabel.setMinimumWidth(self._COLUMN_2_MIN_WIDTH)
        self.openedFileLabel.setStatusTip("Ruta del fichero abierto")

        ##### Lista de ficheros #####
        self.fileList = QtGui.QListWidget()
        self.fileList.setFixedWidth(self._COLUMN_0_FIXED_WIDTH)
        self.fileList.setMinimumHeight(self._ROW_2_MIN_HEIGHT)
        # Mostramos siempre las barras de scroll para evitar bug en el que
        # dichas barras de scroll no aparecen cuando deberían.
        self.fileList.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.fileList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.fileList.setStatusTip("Ficheros de la carpeta abierta")

        ##### Editor de texto #####
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setMinimumWidth(self._COLUMN_2_MIN_WIDTH)
        self.textEdit.setMinimumHeight(self._ROW_2_MIN_HEIGHT)
        self.textEdit.setStatusTip("Fichero abierto")

        ##### Botón #####
        self.arrowButton = QtGui.QPushButton(">>>", self)
        self.arrowButton.setStatusTip("Abrir el fichero seleccionado")

        ##### Configuración grid layout #####
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.openedFolderLabel, 0, 0)
        grid.addWidget(self.openedFileLabel, 0, 2)
        grid.addWidget(self.fileList, 1, 0)
        grid.addWidget(self.arrowButton, 1, 1)
        grid.addWidget(self.textEdit, 1, 2)

        self.setLayout(grid)


class TextEditorMainWindow(QtGui.QMainWindow):
    """
    Ventana principal del programa.

    Contiene la barra de menús, la barra de herramientas, la barra de estado, y,
    por supuesto, el widget con el editor de texto.

    Argumentos:
        textEditorWidget: Widget con el editor de texto (objeto de la clase
            textEditorWidget)

    Atributos:
        textEditorWidget: Widget con el editor de texto (objeto de la clase
            textEditorWidget)
        exitAction: QAction para salir del programa.
        openFileAction: QAction para abrir fichero.
        openFolderAction: QAction para abrir carpeta.
        saveFileAction: QAction para guardar fichero.
        saveAsAction: QAction para guardar fichero como.
    """

    def __init__(self, textEditorWidget):
        super(TextEditorMainWindow, self).__init__()

        self.textEditorWidget = textEditorWidget

        self._initUI()

    def _initUI(self):
        """
        Inicialización de la interfaz.
        """

        ##### Acciones #####
        self.exitAction = QtGui.QAction("Salir", self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip("Salir del programa")

        self.openFileAction = QtGui.QAction("Abrir Fichero", self)
        self.openFileAction.setShortcut('Ctrl+O')
        self.openFileAction.setStatusTip("Abrir fichero")

        self.openFolderAction = QtGui.QAction("Abrir Carpeta", self)
        self.openFolderAction.setShortcut('Ctrl+Shift+O')
        self.openFolderAction.setStatusTip("Abrir carpeta")

        self.saveFileAction = QtGui.QAction("Guardar", self)
        self.saveFileAction.setShortcut('Ctrl+S')
        self.saveFileAction.setStatusTip("Guardar cambios del fichero abierto")

        self.saveAsAction = QtGui.QAction("Guardar Como...", self)
        self.saveAsAction.setShortcut('Ctrl+Shift+S')
        self.saveAsAction.setStatusTip("Guardar cambios del fichero abierto en un"
                                       " nuevo fichero")

        ##### Barra de menús #####
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&Archivo')
        fileMenu.addAction(self.openFileAction)
        fileMenu.addAction(self.openFolderAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveFileAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        ##### Barra de herramientas #####
        toolBar = self.addToolBar("Barra de Herramientas")
        toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolBar.addAction(self.openFileAction)
        toolBar.addAction(self.openFolderAction)
        toolBar.addAction(self.saveFileAction)
        toolBar.addAction(self.saveAsAction)

        ##### Barra de estado #####
        self.statusBar()  # Activa la barra de estado.

        ##### Widget contador #####
        # Añade a la ventana principal el contador.
        self.setCentralWidget(self.textEditorWidget)

        ##### Propiedades ventana #####
        self.setWindowTitle("Editor de Texto")


class TextEditorDialogs():
    """
    Clase TextEditorDialogs: Contiene métodos para mostrar mensajes emergentes y
    ventanas de diálogo para abrir/guardar ficheros/directorios.
    """

    @staticmethod
    def showErrorMessage(errorText):
        """
        Muestra una ventana emergente de error con el mensaje indicado en
        el argumento errorText.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QtGui.QMessageBox.Critical)
        msg.setText(errorText)
        msg.exec_()

    @staticmethod
    def showInfoMessage(infoText):
        """
        Muestra una ventana emergente de información con el mensaje indicado en
        el argumento infoText.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle("Informacion")
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(infoText)
        msg.exec_()

    @staticmethod
    def openFileDialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar el fichero a abrir.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta del fichero seleccionado.
        """
        return QtGui.QFileDialog.getOpenFileName(parent, "Abrir fichero")

    @staticmethod
    def openFolderDialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar la carpeta a abrir.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta de la carpeta seleccionada.
        """
        return QtGui.QFileDialog.getExistingDirectory(
            parent, "Seleccionar carpeta")

    @staticmethod
    def saveFileDialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar dónde se guardará el
        fichero.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta del fichero seleccionado.
        """
        return QtGui.QFileDialog.getSaveFileName(parent, 'Guardar Como...')


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print("Este módulo no puede ser ejecutado", file=sys.stderr)
