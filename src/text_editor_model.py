#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con el modelo del editor de texto.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
import sys
import os
from PyQt4 import QtGui


class TextEditorModel():
    """
    Clase TextEditorModel: 

    Atributos:
        openedFilePath
        openedFileData
        openedFolderPath
        openedFolderFiles
    """

    def __init__(self):
        # TODO: Valorar si esto es necesario.
        self.openedFilePath = ""
        self.openedFileData = ""
        self.openedFolderPath = ""
        self.openedFolderFiles = []

    def openThisFolder(self, folderPath):
        """
        Abre la carpeta indicada en el argumento folderPath para cargar todos
        sus ficheros en la lista de ficheros self.openedFolderFiles.
        """
        try:
            folderPath = str(folderPath)
            folderPath = os.path.abspath(folderPath)

            # Obtenemos la lista con los ficheros de la carpeta.
            self.openedFolderFiles = self._listNotHiddenFiles(folderPath)

            # Añadimos el separador de fichero ('/' en Linux y Mac, '\' en
            # Windows) al final de la ruta que se almacena en la etiqueta.
            if (folderPath[-1] != os.path.sep):
                self.openedFolderPath = folderPath + os.path.sep
            else:
                self.openedFolderPath = folderPath
        except:
            self._showErrorMessage("No se pudo abrir la carpeta \"" +
                                   folderPath + "\"")

    def openThisFile(self, filePath):
        """
        Abre el fichero indicado en el argumento filePath.
        """
        try:
            file = open(filePath, 'r')
            with file:
                self.openedFileData = file.read()
                self.openedFilePath = filePath

                file.close()
        except:
            self._showErrorMessage("No se pudo abrir el fichero \"" +
                                   filePath + "\"")

    def saveInThisFile(self, filePath):
        """
        Guarda el archivo abierto en la ruta indicada en el argumento filePath.
        """
        try:
            file = open(filePath, "w")

            file.write(self.openedFileData)

            file.close()

            self.openedFilePath = filePath

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
                    list.append(f)  # ... lo añadimos a la lista.

        return list


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print("Este módulo no puede ser ejecutado", file=sys.stderr)
