import tkinter as tk
from tkinter import messagebox
from controllers.grupos import insert_grupo

def form_grupo(parent, on_close_callback):
    ventana = tk.Toplevel(parent)
    ventana.title("Agregar Grupo")

    tk.Label(ventana, text="Nombre del grupo:").pack(pady=5)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack(pady=5)

    def guardar():
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "El nombre no puede estar vacío.")
            return
        
        insert_grupo(nombre)
        messagebox.showinfo("Éxito", f"Grupo '{nombre}' agregado correctamente.")
        on_close_callback()  # Actualiza en el menú
        ventana.destroy()

    tk.Button(ventana, text="Guardar", command=guardar, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()

    ventana.transient(parent)
    ventana.grab_set()
    parent.wait_window(ventana)
