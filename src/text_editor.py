#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Práctica 2 de ISSBC: Programa editor de ficheros de texto desarrollado con PyQt4
siguiendo la arquitectura Modelo-Vista-Controlador.

Módulo principal.

Editor de ficheros de texto que permite abrir una carpeta y mostrar los ficheros
dentro de ella en un panel lateral para poder abrirlos fácilmente con tan solo
seleccionarlos y pulsar un botón.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from text_editor_model import TextEditorModel
from text_editor_view import TextEditorView
from text_editor_controller import TextEditorController
import sys
from PyQt4 import QtGui


class TextEditor():
    """
    Clase TextEditor: Monta todas las piezas del MVC e inicia el programa.
    """

    def __init__(self):
        app = QtGui.QApplication(sys.argv)

        controller = TextEditorController(TextEditorModel(), TextEditorView())

        sys.exit(app.exec_())


if __name__ == "__main__":
    """
    Función principal: Inicia el programa.
    """
    textEditorProgram = TextEditor()
