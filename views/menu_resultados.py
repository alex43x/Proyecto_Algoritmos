import tkinter as tk
from tkinter import ttk, messagebox
from controllers.partido import get_partidos
from models.partido import Partido


def pantalla_resultados(ventana, volver_menu):
    # limpiar la ventana principal
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.configure(bg="#f8f8f8")

    # título principal
    tk.Label(
        ventana,
        text="⚽ Registro de resultados de los partidos",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#f8f8f8"
    ).pack(pady=20)

    # marco principal
    frame_tabla = tk.Frame(ventana, bg="#f8f8f8")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    # columnas de la tabla
    columnas = (
        "idPartido", "equipo1", "equipo2", "jornada",
        "fecha", "hora",
        "goles1", "goles2",
        "amarillas1", "amarillas2",
        "rojas1", "rojas2",
        "puntos1", "puntos2"
    )

    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=20)
    tabla.pack(fill="both", expand=True)

    encabezados = {
        "idPartido": "ID",
        "equipo1": "Equipo 1",
        "equipo2": "Equipo 2",
        "jornada": "Jornada",
        "fecha": "Fecha",
        "hora": "Hora",
        "goles1": "Goles E1",
        "goles2": "Goles E2",
        "amarillas1": "TA E1",
        "amarillas2": "TA E2",
        "rojas1": "TR E1",
        "rojas2": "TR E2",
        "puntos1": "Puntos E1",
        "puntos2": "Puntos E2",
    }

    for col in columnas:
        tabla.heading(col, text=encabezados[col])
        tabla.column(col, anchor="center", width=80)

    # cargar datos de los partidos
    partidos = get_partidos()
    for p in partidos:
        valores = (
            p[0], p[1], p[2], p[3],
            p[4], p[5],
            "", "", "", "", "", "", "", ""
        )
        tabla.insert("", "end", values=valores)

    # función para editar celdas numéricas
    def editar_celda(event):
        item = tabla.identify_row(event.y)
        col = tabla.identify_column(event.x)
        if not item or col in ("#1", "#2", "#3", "#4", "#5", "#6"):  # no editables
            return

        col_index = int(col[1:]) - 1
        old_value = tabla.item(item, "values")[col_index]
        entry = tk.Entry(frame_tabla, font=("Segoe UI", 11))
        entry.insert(0, old_value)
        entry.focus()

        bbox = tabla.bbox(item, col)
        if not bbox:
            return
        entry.place(
            x=bbox[0] + 2, y=bbox[1] + 2,
            width=bbox[2] - 4, height=bbox[3] - 4
        )

        def guardar_editado(_):
            nuevo_valor = entry.get().strip()
            valores = list(tabla.item(item, "values"))
            valores[col_index] = nuevo_valor
            tabla.item(item, values=valores)
            entry.destroy()

        def destruir_entry(_):
            entry.destroy()

        entry.bind("<Return>", guardar_editado)
        entry.bind("<FocusOut>", destruir_entry)

    tabla.bind("<Double-1>", editar_celda)

    # función para guardar los resultados editados
    def guardar_resultados():
        filas = tabla.get_children()
        actualizados = 0

        for f in filas:
            valores = tabla.item(f, "values")
            (
                idPartido, _, _, _,
                _, _,
                g1, g2, a1, a2, r1, r2, p1, p2
            ) = valores

            # si no hay goles cargados, se ignora
            if not g1.strip() or not g2.strip():
                continue

            try:
                datos = list(map(int, [
                    g1, g2, a1 or 0, a2 or 0, r1 or 0, r2 or 0, p1 or 0, p2 or 0
                ]))
            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"Valores inválidos en el partido ID {idPartido}. Usa solo números."
                )
                return

            Partido.actualizar_resultados(
                idPartido,
                goles1=datos[0], goles2=datos[1],
                amarillas1=datos[2], amarillas2=datos[3],
                rojas1=datos[4], rojas2=datos[5],
                puntos1=datos[6], puntos2=datos[7]
            )
            actualizados += 1

        if actualizados > 0:
            messagebox.showinfo(
                "Éxito",
                f"Se actualizaron {actualizados} partidos correctamente ✅"
            )
        else:
            messagebox.showinfo("Sin cambios", "No se ingresaron resultados.")

    # función para volver al menú principal
    def volver():
        volver_menu(ventana)

    # marco de botones inferiores
    frame_botones = tk.Frame(ventana, bg="#f8f8f8")
    frame_botones.pack(pady=20)

    btn_guardar = tk.Button(
        frame_botones,
        text="💾 Guardar Resultados",
        font=("Segoe UI", 12),
        bg="#68ab98",
        fg="white",
        width=20,
        command=guardar_resultados
    )
    btn_guardar.grid(row=0, column=0, padx=10)

    btn_volver = tk.Button(
        frame_botones,
        text="⬅ Volver al Menú",
        font=("Segoe UI", 12),
        bg="#68ab98",
        fg="white",
        width=20,
        command=volver
    )
    btn_volver.grid(row=0, column=1, padx=10)

    # pie de página
    tk.Label(
        ventana,
        text="Desarrollado por Sintax FC",
        font=("Segoe UI", 9, "italic"),
        fg="#666666",
        bg="#f8f8f8"
    ).pack(side="bottom", pady=5)
