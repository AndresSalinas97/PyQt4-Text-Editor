#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con el modelo del editor de texto.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
from text_editor_view import TextEditorDialogs
import codecs
import sys
import os


class TextEditorModel():
    """
    Clase TextEditorModel: Modelo del editor de texto.

    Atributos:
        openedFilePath: String con la ruta al fichero abierto.
        openedFileData: String con el contenido del fichero abierto.
        openedFolderPath: String con la ruta a la carpeta abierta.
        openedFolderFiles: Lista con los ficheros de la carpeta abierta.
    """

    def __init__(self):
        self.openedFilePath = u""
        self.openedFileData = u""
        self.openedFolderPath = u""
        self.openedFolderFiles = []

    def openFolder(self, folderPath):
        """
        Abre la carpeta indicada en el argumento folderPath para cargar todos
        sus ficheros en la lista de ficheros self.openedFolderFiles.
        """
        try:
            folderPath = unicode(folderPath)
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
            TextEditorDialogs.showErrorMessage(
                u"No se pudo abrir la carpeta \"" + folderPath + u"\"")

    def openFile(self, filePath):
        """
        Abre el fichero indicado en el argumento filePath.
        """
        try:
            with codecs.open(filePath, 'r', encoding='utf-8') as file:
                self.openedFileData = unicode(file.read())
                self.openedFilePath = filePath

                file.close()
        except:
            TextEditorDialogs.showErrorMessage(
                u"No se pudo abrir el fichero \"" + filePath + u"\"")

    def saveFile(self, filePath):
        """
        Guarda el archivo abierto en la ruta indicada en el argumento filePath.
        """
        try:
            with codecs.open(filePath, 'w', encoding='utf-8') as file:
                file.write(unicode(self.openedFileData))

                file.close()

            self.openedFilePath = filePath

            # Actualizamos los ficheros de la carpeta para que el nuevo fichero
            # aparezca en el menú lateral.
            self.reloadFolder()

            TextEditorDialogs.showInfoMessage(u"Fichero guardado con éxito!")
        except:
            TextEditorDialogs.showErrorMessage(
                u"No se pudo guardar en el fichero \"" + filePath + u"\"")

    def reloadFolder(self):
        """
        Vuelve a cargar los ficheros de la carpeta abierta (para actualizar
        la lista y mostrar nuevos ficheros que puedan haber sido creados).
        """
        self.openFolder(self.openedFolderPath)

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
    print(u"Este módulo no puede ser ejecutado", file=sys.stderr)
