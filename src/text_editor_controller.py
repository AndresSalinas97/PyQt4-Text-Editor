#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con el controlador del editor de texto.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
from text_editor_view import TextEditorDialogs
import sys
from PyQt4 import QtGui


class TextEditorController():
    """
    Clase TextEditorController: Controlador del editor de texto.

    Argumentos:
        model: objeto de la clase TextEditorModel.
        view: objeto de la clase TextEditorView.

    Atributos:
        model: objeto de la clase TextEditorModel.
        view: objeto de la clase TextEditorView.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._initModel()
        self._initView()
        self._initController()

    def _initModel(self):
        """
        Inicializa el modelo.
        """
        # El editor se abrirá con el directorio actual (.) cargado.
        self.model.openFolder(".")

    def _initView(self):
        """
        Inicializa la vista.
        """
        self._updateView()
        self.view.show()

    def _initController(self):
        """
        Inicializa el controlador.

        Conecta los botones y acciones de la vista con métodos del controlador.
        """
        self.view.widget.refreshButton.clicked.connect(self.reloadFolder)

        self.view.widget.fileList.itemClicked.connect(self._openSelectedFile)

        self.view.mainWindow.exitAction.triggered.connect(
            QtGui.qApp.closeAllWindows)
        self.view.mainWindow.openFileAction.triggered.connect(
            self._openFileDialog)
        self.view.mainWindow.openFolderAction.triggered.connect(
            self._openFolderDialog)
        self.view.mainWindow.saveFileAction.triggered.connect(
            self._saveOpenedFile)
        self.view.mainWindow.saveAsAction.triggered.connect(
            self._saveAsDialog)

    def _updateView(self):
        """
        Actualiza la vista.
        """
        # Actualizamos las etiquetas.
        self.view.widget.openedFileLabel.setText(self.model.openedFilePath)
        self.view.widget.openedFolderLabel.setText(self.model.openedFolderPath)

        # Actualizamos la lista de ficheros.
        self.view.widget.fileList.clear()
        self.view.widget.fileList.addItems(self.model.openedFolderFiles)
        self.view.widget.fileList.sortItems()  # Ordena alfabéticamente.

        # Actualizamos el editor
        self.view.widget.textEdit.setText(self.model.openedFileData)

    def _openFolderDialog(self):
        """
        Muestra una ventana de diálogo para elegir la carpeta que se abrirá.
        """
        # Ventana de diálogo para seleccionar la carpeta.
        folderPath = TextEditorDialogs.openFolderDialog(self.view.mainWindow)

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado una carpeta.
        if(folderPath):
            self._openFolder(folderPath)

    def _openFolder(self, folderPath):
        """
        Indica al modelo la carpeta a abrir (folderPath) y actualiza la vista.
        """
        self.model.openFolder(folderPath)
        self._updateView()

    def _openFileDialog(self):
        """
        Muestra una ventana de diálogo para elegir fichero que se abrirá.
        """
        # Ventana de diálogo para seleccionar el fichero.
        filePath = TextEditorDialogs.openFileDialog(self.view.mainWindow)

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado un fichero.
        if(filePath):
            self._openFile(filePath)

    def _openSelectedFile(self):
        """
        Abre el fichero seleccionado en la lista de ficheros.
        """
        selectedFiles = self.view.widget.fileList.selectedItems()

        if (not selectedFiles):
            TextEditorDialogs.showErrorMessage(
                "Primero debe seleccionar un fichero en el panel de la izquierda!")
            return

        filePath = self.model.openedFolderPath + selectedFiles[0].text()

        self._openFile(filePath)

    def _openFile(self, filePath):
        """
        Indica al modelo el fichero a abrir (filePath) y actualiza la vista.

        Antes de abrir el nuevo fichero se comprobará si el usuario ha hecho
        cambios en el fichero abierto y, en caso afirmativo, se le avisará de
        que perderá dichos cambios y se le permitirá cancelar la operación.
        """
        # Comprobamos si el usuario ha hecho cambios en el fichero abierto.
        if (self.view.widget.textEdit.toPlainText() != self.model.openedFileData):
            # Avisamos al usuario y le pedimos confirmación.
            confirmed = TextEditorDialogs.confirmOperationMessage(
                "Al abrir otro fichero perdera los cambios sin guardar!")

            # Si el usuario decide cancelar...
            if (not confirmed):
                # ... eliminamos la selección y...
                self._clearFileListSelection()
                # ... salimos sin abrir el nuevo fichero.
                return

        self.model.openFile(filePath)
        self._updateView()

    def _clearFileListSelection(self):
        """
        Anula la selección de todos los items de la lista de ficheros.

        Sirve para que el fichero que se ha intentado abrir no se quede marcado
        como seleccionado en el panel lateral si este finalmente no ha sido
        abierto.
        """
        for item in self.view.widget.fileList.selectedItems():
            self.view.widget.fileList.setItemSelected(item, False)

    def _saveAsDialog(self):
        """
        Muestra una ventana de diálogo para elegir dónde se guardará el fichero.
        """
        # Ventana de diálogo para seleccionar dónde se guardará el fichero.
        filePath = TextEditorDialogs.saveFileDialog(self.view.mainWindow)

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado un fichero.
        if(filePath):
            self._saveFile(filePath)

    def _saveOpenedFile(self):
        """
        Guarda el archivo abierto.

        Si no hay ningún archivo abierto, es decir, la etiqueta que indica el
        fichero abierto openedFilePath está vacía, se abrirá la ventana de
        diálogo de Guardar Como...
        """
        if (not self.model.openedFilePath):
            self._saveAsDialog()
        else:
            self._saveFile(self.model.openedFilePath)

    def _saveFile(self, filePath):
        """
        Actualiza el modelo con los cambios en el editor de la vista, le indica
        dónde guardar los cambios (filePath) y actualiza la vista.
        """
        self.model.openedFileData = self.view.widget.textEdit.toPlainText()
        self.model.saveFile(filePath)
        self._updateView()

    def reloadFolder(self):
        """
        Ordena al modelo actualizar la lista de ficheros y actualiza la vista.
        """
        self.model.reloadFolder()
        self._updateView()


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print("Este módulo no puede ser ejecutado", file=sys.stderr)
