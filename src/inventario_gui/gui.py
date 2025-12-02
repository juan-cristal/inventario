import tkinter as tk
from tkinter import ttk, messagebox

from inventario_gui import app   # Our backend module


# ----------------------------------------------------
# Main GUI Class
# ----------------------------------------------------

class InventarioGUI:

    def __init__(self, root):
        self.root = root
        root.title("Inventario GUI - Tkinter + SQLite (by J.S. Cristal)")
        root.geometry("950x500")

        self._crear_widgets()
        self._cargar_tabla()

    # ------------------------------------------------
    # Create all UI widgets
    # ------------------------------------------------
    def _crear_widgets(self):

        # LEFT PANEL – FORM
        form_frame = tk.Frame(self.root, padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Labels and entries
        self._add_label_entry(form_frame, "Nombre:", "nombre")
        self._add_label_entry(form_frame, "Descripción:", "descripcion")
        self._add_label_entry(form_frame, "Cantidad:", "cantidad")
        self._add_label_entry(form_frame, "Precio:", "precio")
        self._add_label_entry(form_frame, "Categoría:", "categoria")

        # Buttons
        tk.Button(form_frame, text="Agregar", width=20,
                  command=self._agregar).pack(pady=3)
        tk.Button(form_frame, text="Actualizar", width=20,
                  command=self._actualizar).pack(pady=3)
        tk.Button(form_frame, text="Eliminar", width=20,
                  command=self._eliminar).pack(pady=3)
        tk.Button(form_frame, text="Bajo Stock", width=20,
                  command=self._filtrar_bajo_stock).pack(pady=3)
        tk.Button(form_frame, text="Mostrar Todo", width=20,
                  command=self._cargar_tabla).pack(pady=3)
        tk.Button(form_frame, text="Limpiar", width=20,
                  command=self._limpiar_formulario).pack(pady=3)

        # RIGHT PANEL – TABLE
        columnas = ("id", "nombre", "descripcion", "cantidad", "precio", "categoria")
        self.tabla = ttk.Treeview(self.root, columns=columnas, show="headings", height=20)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120)

        self.tabla.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._on_select)

    # Helper to create labeled Entry fields
    def _add_label_entry(self, frame, text, attribute):
        tk.Label(frame, text=text).pack()
        entry = tk.Entry(frame)
        entry.pack(fill=tk.X)
        setattr(self, f"entry_{attribute}", entry)

    # ------------------------------------------------
    # CRUD Operations via the backend (app.py)
    # ------------------------------------------------

    def _agregar(self):
        try:
            app.agregar_producto(
                self.entry_nombre.get().strip(),
                self.entry_descripcion.get().strip(),
                int(self.entry_cantidad.get()),
                float(self.entry_precio.get()),
                self.entry_categoria.get().strip()
            )
            messagebox.showinfo("OK", "Producto agregado.")
            self._cargar_tabla()
            self._limpiar_formulario()

        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser numéricos.")

    def _actualizar(self):
        selected = self._get_selected_id()
        if not selected:
            return

        try:
            app.actualizar_producto(
                selected,
                self.entry_nombre.get().strip(),
                self.entry_descripcion.get().strip(),
                int(self.entry_cantidad.get()),
                float(self.entry_precio.get()),
                self.entry_categoria.get().strip()
            )
            messagebox.showinfo("OK", "Producto actualizado.")
            self._cargar_tabla()

        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser numéricos.")

    def _eliminar(self):
        selected = self._get_selected_id()
        if not selected:
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar producto?"):
            app.eliminar_producto(selected)
            self._cargar_tabla()
            self._limpiar_formulario()

    # ------------------------------------------------
    # Table handling
    # ------------------------------------------------

    def _cargar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        productos = app.obtener_todos()

        for p in productos:
            self.tabla.insert("", tk.END, values=p)

    def _filtrar_bajo_stock(self):
        try:
            limite = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número en Cantidad.")
            return

        productos = app.obtener_bajo_stock(limite)

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for p in productos:
            self.tabla.insert("", tk.END, values=p)

    def _on_select(self, event):
        """When the user selects an item in the table."""
        try:
            item = self.tabla.focus()
            datos = self.tabla.item(item)["values"]

            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, datos[1])

            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, datos[2])

            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, datos[3])

            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, datos[4])

            self.entry_categoria.delete(0, tk.END)
            self.entry_categoria.insert(0, datos[5])

        except Exception:
            pass

    # ------------------------------------------------
    # Helpers
    # ------------------------------------------------

    def _get_selected_id(self):
        item = self.tabla.focus()
        if not item:
            messagebox.showerror("Error", "Seleccione un producto.")
            return None
        return self.tabla.item(item)["values"][0]

    def _limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)


# ----------------------------------------------------
# Entry Point (this runs the GUI)
# ----------------------------------------------------

def start_gui():
    root = tk.Tk()
    InventarioGUI(root)
    root.mainloop()


if __name__ == "__main__":
    start_gui()
