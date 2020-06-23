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
        opened_file_path: String con la ruta al fichero abierto.
        opened_file_data: String con el contenido del fichero abierto.
        opened_folder_path: String con la ruta a la carpeta abierta.
        opened_folder_files: Lista con los ficheros de la carpeta abierta.
    """

    def __init__(self):
        self.opened_file_path = u""
        self.opened_file_data = u""
        self.opened_folder_path = u""
        self.opened_folder_files = []

    def open_folder(self, folder_path):
        """
        Abre la carpeta indicada en el argumento folder_path para cargar todos
        sus ficheros en la lista de ficheros self.opened_folder_files.
        """
        try:
            folder_path = folder_path
            folder_path = unicode(os.path.abspath(folder_path))

            # Obtenemos la lista con los ficheros de la carpeta.
            self.opened_folder_files = self._list_not_hidden_files(folder_path)

            # Añadimos el separador de fichero ('/' en Linux y Mac, '\' en
            # Windows) al final de la ruta que se almacena en la etiqueta.
            if (folder_path[-1] != os.path.sep):
                self.opened_folder_path = folder_path + os.path.sep
            else:
                self.opened_folder_path = folder_path
        except:
            TextEditorDialogs.show_error_message(
                u"No se pudo abrir la carpeta \"" + folder_path + u"\"")

    def open_file(self, file_path):
        """
        Abre el fichero indicado en el argumento file_path.
        """
        try:
            with codecs.open(file_path, 'r', encoding='utf-8') as file:
                self.opened_file_data = unicode(file.read())
                self.opened_file_path = file_path

                file.close()
        except:
            TextEditorDialogs.show_error_message(
                u"No se pudo abrir el fichero \"" + file_path + u"\"")

    def save_file(self, file_path):
        """
        Guarda el archivo abierto en la ruta indicada en el argumento file_path.
        """
        try:
            with codecs.open(file_path, 'w', encoding='utf-8') as file:
                file.write(unicode(self.opened_file_data))

                file.close()

            self.opened_file_path = file_path

            # Actualizamos los ficheros de la carpeta para que el nuevo fichero
            # aparezca en el menú lateral.
            self.reload_folder()

            TextEditorDialogs.show_info_message(u"Fichero guardado con éxito!")
        except:
            TextEditorDialogs.show_error_message(
                u"No se pudo guardar en el fichero \"" + file_path + u"\"")

    def reload_folder(self):
        """
        Vuelve a cargar los ficheros de la carpeta abierta (para actualizar
        la lista y mostrar nuevos ficheros que puedan haber sido creados).
        """
        self.open_folder(self.opened_folder_path)

    def _list_not_hidden_files(self, folder_path):
        """
        Devuelve una lista con los nombres de los ficheros no ocultos dentro de
        la carpeta indicada en el argumento folder_path.
        """
        list = []

        for f in os.listdir(folder_path):
            if (os.path.isfile(os.path.join(folder_path, f))):  # Si es fichero...
                if (not f.startswith('.')):  # ... y no está oculto...
                    list.append(f)  # ... lo añadimos a la lista.

        return list


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print(u"Este módulo no puede ser ejecutado", file=sys.stderr)
