import tkinter as tk
from tkinter import messagebox
from controllers.grupos import insert_grupo


def form_grupo(parent, on_close_callback):
    # --- Ventana principal ---
    ventana = tk.Toplevel(parent)
    ventana.title("Agregar Grupo")
    ventana.configure(bg="#f8f8f8")
    ventana.resizable(False, False)

    # --- Función para centrar ventana ---
    def centrar_ventana(ventana, ancho, alto):
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    centrar_ventana(ventana, 380, 260)

    # --- Contenedor principal tipo tarjeta ---
    frame_main = tk.Frame(ventana, bg="white", bd=2, relief="groove", padx=20, pady=20)
    frame_main.pack(padx=20, pady=20, fill="both", expand=True)

    # --- Título ---
    tk.Label(
        frame_main,
        text="🧩 Agregar Nuevo Grupo",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#333"
    ).pack(pady=(0, 15))

    # --- Campo de texto ---
    tk.Label(
        frame_main,
        text="Nombre del grupo:",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        fg="#444"
    ).pack(anchor="w", pady=(5, 2))

    entry_nombre = tk.Entry(
        frame_main,
        font=("Segoe UI", 11),
        width=30,
        relief="solid",
        bd=1
    )
    entry_nombre.pack(pady=(0, 10))

    # --- Función de guardado ---
    def guardar():
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("⚠️ Error", "El nombre no puede estar vacío.")
            return

        insert_grupo(nombre)
        messagebox.showinfo("✅ Éxito", f"Grupo '{nombre}' agregado correctamente.")
        on_close_callback()  # Actualiza la vista en el menú
        ventana.destroy()

    # --- Frame de botones ---
    frame_botones = tk.Frame(frame_main, bg="white")
    frame_botones.pack(pady=(10, 0))

    # --- Botón Guardar ---
    tk.Button(
        frame_botones,
        text="Guardar",
        font=("Segoe UI", 11, "bold"),
        bg="#68ab98",
        fg="white",
        activebackground="#5b9c8a",
        activeforeground="white",
        width=12,
        command=guardar
    ).grid(row=0, column=0, padx=10)

    # --- Botón Cancelar ---
    tk.Button(
        frame_botones,
        text="Cancelar",
        font=("Segoe UI", 11, "bold"),
        bg="#e57373",
        fg="white",
        activebackground="#d16060",
        activeforeground="white",
        width=12,
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)

    # --- Mantener ventana modal ---
    ventana.transient(parent)
    ventana.grab_set()
    parent.wait_window(ventana)
