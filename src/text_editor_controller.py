#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con el controlador del editor de texto.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
import sys
from PyQt4 import QtGui


class TextEditorController():
    """
    Clase TextEditorController: Controlador del editor de texto.
    """

    def __init__(self, model, view):
        """
        Constructor de la clase TextEditorController.

        Atributos:
            model: objeto de la clase TextEditorModel.
            view: objeto de la clase TextEditorView.
        """

        self.model = model
        self.view = view

        self.initModel()
        self.initView()
        self.initController()

    def initModel(self):
        pass

    def initView(self):
        self.view.show()
        self.updateView()

    def initController(self):
        pass

    def updateView(self):
        pass


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print("Este módulo no puede ser ejecutado", file=sys.stderr)
