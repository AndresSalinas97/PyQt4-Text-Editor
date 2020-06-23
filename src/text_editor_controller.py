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

        self._init_model()
        self._init_view()
        self._init_controller()

    def _init_model(self):
        """
        Inicializa el modelo.
        """
        # El editor se abrirá con el directorio actual (.) cargado.
        self.model.open_folder(".")

    def _init_view(self):
        """
        Inicializa la vista.
        """
        self._update_view()
        self.view.show()

    def _init_controller(self):
        """
        Inicializa el controlador.

        Conecta los botones y acciones de la vista con métodos del controlador.
        """
        self.view.main_widget.refresh_button.clicked.connect(
            self._reload_folder)

        self.view.main_widget.file_list.itemClicked.connect(
            self._open_selected_file)

        self.view.main_window.exit_action.triggered.connect(
            QtGui.qApp.closeAllWindows)
        self.view.main_window.open_file_action.triggered.connect(
            self._open_file_dialog)
        self.view.main_window.open_folder_action.triggered.connect(
            self._open_folder_dialog)
        self.view.main_window.save_file_action.triggered.connect(
            self._save_opened_file)
        self.view.main_window.save_as_action.triggered.connect(
            self._save_as_dialog)

    def _update_view(self):
        """
        Actualiza la vista.
        """
        # Actualizamos las etiquetas.
        self.view.main_widget.opened_file_label.setText(
            self.model.opened_file_path)
        self.view.main_widget.opened_folder_label.setText(
            self.model.opened_folder_path)

        # Actualizamos la lista de ficheros.
        self.view.main_widget.file_list.clear()
        self.view.main_widget.file_list.addItems(
            self.model.opened_folder_files)
        self.view.main_widget.file_list.sortItems()  # Ordena alfabéticamente.

        # Actualizamos el editor
        self.view.main_widget.text_edit.setText(
            unicode(self.model.opened_file_data))

    def _open_folder_dialog(self):
        """
        Muestra una ventana de diálogo para elegir la carpeta que se abrirá.
        """
        # Ventana de diálogo para seleccionar la carpeta.
        folder_path = TextEditorDialogs.open_folder_dialog(
            self.view.main_window)

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado una carpeta.
        if(folder_path):
            self._open_folder(folder_path)

    def _open_folder(self, folder_path):
        """
        Indica al modelo la carpeta a abrir (folder_path) y actualiza la vista.
        """
        self.model.open_folder(folder_path)
        self._update_view()

    def _open_file_dialog(self):
        """
        Muestra una ventana de diálogo para elegir fichero que se abrirá.
        """
        # Ventana de diálogo para seleccionar el fichero.
        file_path = TextEditorDialogs.open_file_dialog(self.view.main_window)

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado un fichero.
        if(file_path):
            self._open_file(file_path)

    def _open_selected_file(self):
        """
        Abre el fichero seleccionado en la lista de ficheros.
        """
        selected_files = self.view.main_widget.file_list.selectedItems()

        if (not selected_files):
            TextEditorDialogs.show_error_message(
                u"Primero debe seleccionar un fichero en el panel de la izquierda!")
            return

        file_path = unicode(self.model.opened_folder_path +
                            selected_files[0].text())

        self._open_file(file_path)

    def _open_file(self, file_path):
        """
        Indica al modelo el fichero a abrir (file_path) y actualiza la vista.

        Antes de abrir el nuevo fichero se comprobará si el usuario ha hecho
        cambios en el fichero abierto y, en caso afirmativo, se le avisará de
        que perderá dichos cambios y se le permitirá cancelar la operación.
        """
        # Comprobamos si el usuario ha hecho cambios en el fichero abierto.
        if (self.view.main_widget.text_edit.toPlainText() != self.model.opened_file_data):
            # Avisamos al usuario y le pedimos confirmación.
            confirmed = TextEditorDialogs.confirm_operation_message(
                u"Al abrir otro fichero perderá los cambios sin guardar!")

            # Si el usuario decide cancelar...
            if (not confirmed):
                # ... eliminamos la selección y...
                self._clear_file_list_selection()
                # ... salimos sin abrir el nuevo fichero.
                return

        self.model.open_file(file_path)
        self._update_view()

    def _clear_file_list_selection(self):
        """
        Anula la selección de todos los items de la lista de ficheros.

        Sirve para que el fichero que se ha intentado abrir no se quede marcado
        como seleccionado en el panel lateral si este finalmente no ha sido
        abierto.
        """
        for item in self.view.main_widget.file_list.selectedItems():
            self.view.main_widget.file_list.setItemSelected(item, False)

    def _save_as_dialog(self):
        """
        Muestra una ventana de diálogo para elegir dónde se guardará el fichero.
        """
        # Ventana de diálogo para seleccionar dónde se guardará el fichero.
        file_path = TextEditorDialogs.save_file_dialog(self.view.main_window)

        # Antes de continuar comprobamos que el usuario realmente ha
        # seleccionado un fichero.
        if(file_path):
            self._save_file(file_path)

    def _save_opened_file(self):
        """
        Guarda el archivo abierto.

        Si no hay ningún archivo abierto, es decir, la etiqueta que indica el
        fichero abierto opened_file_path está vacía, se abrirá la ventana de
        diálogo de Guardar Como...
        """
        if (not self.model.opened_file_path):
            self._save_as_dialog()
        else:
            self._save_file(self.model.opened_file_path)

    def _save_file(self, file_path):
        """
        Actualiza el modelo con los cambios en el editor de la vista, le indica
        dónde guardar los cambios (file_path) y actualiza la vista.
        """
        self.model.opened_file_data = unicode(
            self.view.main_widget.text_edit.toPlainText())
        self.model.save_file(file_path)
        self._update_view()

    def _reload_folder(self):
        """
        Ordena al modelo actualizar la lista de ficheros y actualiza la vista.
        """
        self.model.reload_folder()
        self._update_view()


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print(u"Este módulo no puede ser ejecutado", file=sys.stderr)
