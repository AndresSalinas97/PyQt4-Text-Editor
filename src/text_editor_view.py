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

    Monta la interfaz del editor a partir de las clases text_editor_widget y
    TextEditorMainWindow y permite acceder a ellas a partir de sus atributos.

    Atributos:
        main_widget: QWidget con la interfaz del editor de texto (objeto de la
                     clase text_editor_widget).
        main_window: Ventana principal (objeto de la clase TextEditorMainWindow).
    """

    def __init__(self):
        self.main_widget = text_editor_widget()
        self.main_window = TextEditorMainWindow(self.main_widget)

    def show(self):
        """
        Hace visible la ventana principal.
        """
        self.main_window.show()


class text_editor_widget(QtGui.QWidget):
    """
    Clase text_editor_widget: QWidget con la interfaz del editor de texto.

    Atributos:
        opened_folder_label: QLineEdit que muestra la ruta de la carpeta abierta.
        opened_file_label: QLineEdit que muestra la ruta del fichero abierto.
        file_list: QListWidget que muestra la lista de ficheros de la carpeta.
        text_edit: QTextEdit para mostrar/editar el fichero.
        refresh_button: QPushButton para recargar la lista de ficheros.
    """

    # Anchura de la primera columna del layout (lista de ficheros).
    _COLUMN_0_FIXED_WIDTH = 300

    # Anchura mínima de la tercera columna del layout (editor de texto).
    _COLUMN_1_MIN_WIDTH = 600

    # Altura mínima de la segunda fila (lista de ficheros y editor de texto).
    _ROW_2_MIN_HEIGHT = 350

    def __init__(self):
        super(text_editor_widget, self).__init__()
        self._init_UI()

    def _init_UI(self):
        """
        Inicialización de la interfaz.
        """
        ##### Etiquetas #####
        # En realidad son campos de texto de una línea (QtGui.QLineEdit)
        # configurados como solo lectura ya que las etiquetas (QtGui.QLabel)
        # dan muchos problemas cuando contienen texto de longitud variable pero
        # la etiqueta dispone de un espacio limitado.
        self.opened_folder_label = QtGui.QLineEdit()
        self.opened_folder_label.setReadOnly(True)
        self.opened_folder_label.setAlignment(QtCore.Qt.AlignCenter)
        self.opened_folder_label.setFixedWidth(self._COLUMN_0_FIXED_WIDTH)
        self.opened_folder_label.setStatusTip(u"Ruta de la carpeta abierta")

        self.opened_file_label = QtGui.QLineEdit()
        self.opened_file_label.setReadOnly(True)
        self.opened_file_label.setAlignment(QtCore.Qt.AlignCenter)
        self.opened_file_label.setMinimumWidth(self._COLUMN_1_MIN_WIDTH)
        self.opened_file_label.setStatusTip(u"Ruta del fichero abierto")

        ##### Lista de ficheros #####
        self.file_list = QtGui.QListWidget()
        self.file_list.setFixedWidth(self._COLUMN_0_FIXED_WIDTH)
        self.file_list.setMinimumHeight(self._ROW_2_MIN_HEIGHT)
        # Mostramos siempre las barras de scroll para evitar bug en el que
        # dichas barras de scroll no aparecen cuando deberían.
        self.file_list.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.file_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.file_list.setStatusTip(
            u"Ficheros de la carpeta abierta (seleccione uno para abrirlo)")

        ##### Editor de texto #####
        self.text_edit = QtGui.QTextEdit()
        self.text_edit.setMinimumWidth(self._COLUMN_1_MIN_WIDTH)
        self.text_edit.setMinimumHeight(self._ROW_2_MIN_HEIGHT)
        self.text_edit.setStatusTip(u"Fichero abierto")

        ##### Botones #####
        self.refresh_button = QtGui.QPushButton(u"Refrescar", self)
        self.refresh_button.setStatusTip(
            u"Actualizar la lista de ficheros para reflejar los últimos cambios"
            u" en la carpeta abierta")

        ##### Configuración grid layout #####
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.opened_folder_label, 0, 0)
        grid.addWidget(self.opened_file_label, 0, 1)
        grid.addWidget(self.file_list, 1, 0)
        grid.addWidget(self.text_edit, 1, 1, 2, 1)
        grid.addWidget(self.refresh_button, 2, 0)

        self.setLayout(grid)


class TextEditorMainWindow(QtGui.QMainWindow):
    """
    Clase TextEditorMainWindow: Ventana principal del programa.

    Contiene la barra de menús, la barra de herramientas, la barra de estado, y,
    por supuesto, el widget con el editor de texto.

    Argumentos:
        text_editor_widget: Widget con el editor de texto (objeto de la clase
            text_editor_widget)

    Atributos:
        text_editor_widget: Widget con el editor de texto (objeto de la clase
            text_editor_widget)
        exit_action: QAction para salir del programa.
        open_file_action: QAction para abrir fichero.
        open_folder_action: QAction para abrir carpeta.
        save_file_action: QAction para guardar fichero.
        save_as_action: QAction para guardar fichero como.
    """

    def __init__(self, text_editor_widget):
        super(TextEditorMainWindow, self).__init__()

        self.text_editor_widget = text_editor_widget

        self._init_UI()

    def _init_UI(self):
        """
        Inicialización de la interfaz.
        """

        ##### Acciones #####
        self.exit_action = QtGui.QAction(u"Salir", self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip(u"Salir del programa")

        self.open_file_action = QtGui.QAction(u"Abrir Fichero", self)
        self.open_file_action.setShortcut('Ctrl+O')
        self.open_file_action.setStatusTip(u"Abrir fichero")

        self.open_folder_action = QtGui.QAction(u"Abrir Carpeta", self)
        self.open_folder_action.setShortcut('Ctrl+Shift+O')
        self.open_folder_action.setStatusTip(u"Abrir carpeta")

        self.save_file_action = QtGui.QAction(u"Guardar", self)
        self.save_file_action.setShortcut('Ctrl+S')
        self.save_file_action.setStatusTip(
            u"Guardar cambios del fichero abierto")

        self.save_as_action = QtGui.QAction(u"Guardar Como...", self)
        self.save_as_action.setShortcut('Ctrl+Shift+S')
        self.save_as_action.setStatusTip(
            u"Guardar cambios del fichero abierto en un nuevo fichero")

        ##### Barra de menús #####
        menuBar = self.menuBar()
        file_menu = menuBar.addMenu(u"Archivo")
        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.open_folder_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_file_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        ##### Barra de herramientas #####
        toolBar = self.addToolBar(u"Barra de Herramientas")
        toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolBar.addAction(self.open_file_action)
        toolBar.addAction(self.open_folder_action)
        toolBar.addAction(self.save_file_action)
        toolBar.addAction(self.save_as_action)

        ##### Barra de estado #####
        self.statusBar()  # Activa la barra de estado.

        ##### Widget contador #####
        # Añade a la ventana principal el contador.
        self.setCentralWidget(self.text_editor_widget)

        ##### Propiedades ventana #####
        self.setWindowTitle(u"Editor de Texto")


class TextEditorDialogs():
    """
    Clase TextEditorDialogs: Contiene métodos para mostrar mensajes emergentes y
    ventanas de diálogo para abrir/guardar ficheros/directorios.
    """

    @staticmethod
    def show_error_message(error_text):
        """
        Muestra una ventana emergente de error con el mensaje indicado en
        el argumento error_text.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(u"Error")
        msg.setIcon(QtGui.QMessageBox.Critical)
        msg.setText(error_text)
        msg.exec_()

    @staticmethod
    def show_info_message(info_text):
        """
        Muestra una ventana emergente de información con el mensaje indicado en
        el argumento info_text.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(u"Información")
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(info_text)
        msg.exec_()

    @staticmethod
    def confirm_operation_message(info_text):
        """
        Muestra una ventana emergente de advertencia para confirmar que el
        usuario desea continuar con la operación.

        Devuelve:
            True si el usuario hace click en Ok; False en caso contrario.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(u"Advertencia")
        msg.setIcon(QtGui.QMessageBox.Warning)
        msg.setText(info_text)
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        retval = msg.exec_()

        if (retval == QtGui.QMessageBox.Ok):
            return True
        else:
            return False

    @staticmethod
    def open_file_dialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar el fichero a abrir.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta del fichero seleccionado.
        """
        return unicode(QtGui.QFileDialog.getOpenFileName(parent, u"Abrir fichero"))

    @staticmethod
    def open_folder_dialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar la carpeta a abrir.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta de la carpeta seleccionada.
        """
        return unicode(QtGui.QFileDialog.getExistingDirectory(
            parent, u"Seleccionar carpeta"))

    @staticmethod
    def save_file_dialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar dónde se guardará el
        fichero.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta del fichero seleccionado.
        """
        return unicode(QtGui.QFileDialog.getSaveFileName(parent,
                                                         u"Guardar Como..."))


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print(u"Este módulo no puede ser ejecutado", file=sys.stderr)
