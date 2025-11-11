import tkinter as tk
from tkinter import ttk, messagebox
from controllers.partido import get_partidos, update_partido
from utils import ultima_fecha_jornada, cerrar_jornada


def pantalla_resultados(ventana, volver_menu):
    # limpiar la ventana principal
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.configure(bg="#f8f8f8")

    # título principal
    tk.Label(
        ventana,
        text="⚽ registro de resultados de los partidos",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#f8f8f8"
    ).pack(pady=20)

    # obtener jornada actual desde la tabla estado_torneo
    jornada_actual = ultima_fecha_jornada()

    # marco de tabla
    frame_tabla = tk.Frame(ventana, bg="#f8f8f8")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = (
        "idPartido", "equipo1", "equipo2", "jornada",
        "fecha", "hora",
        "goles1", "goles2",
        "amarillas1", "amarillas2",
        "rojas1", "rojas2"
    )

    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=18)
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
    }

    for col in columnas:
        tabla.heading(col, text=encabezados[col])
        tabla.column(col, anchor="center", width=90)

    # obtener todos los partidos
    partidos = get_partidos()

    # filtrar solo los de la jornada actual
    partidos_actual = [p for p in partidos if int(p[13]) == int(jornada_actual)]

    # si no hay partidos para esa jornada, mostrar aviso y volver
    if not partidos_actual:
        messagebox.showinfo("Información", f"No hay partidos cargados para la jornada {jornada_actual}.")
        volver_menu(ventana)
        return

    # cargar datos en la tabla
    for p in partidos_actual:
        valores = (
            p[0],  # idPartido
            p[3],  # equipo1_nombre
            p[4],  # equipo2_nombre
            p[13], # jornada
            p[1],  # fecha
            p[2],  # hora
            p[7] if p[7] != 0 else "",  # golesEquipoUno (mostrar vacío si es 0)
            p[8] if p[8] != 0 else "",  # golesEquipoDos (mostrar vacío si es 0)
            p[9] if p[9] != 0 else "",  # tarjetasAmarillasEquipoUno
            p[10] if p[10] != 0 else "", # tarjetasAmarillasEquipoDos
            p[11] if p[11] != 0 else "", # tarjetasRojasEquipoUno
            p[12] if p[12] != 0 else ""  # tarjetasRojasEquipoDos
        )
        tabla.insert("", "end", values=valores)

    # permitir edición de celdas numéricas
    def editar_celda(event):
        item = tabla.identify_row(event.y)
        col = tabla.identify_column(event.x)
        if not item or col in ("#1", "#2", "#3", "#4", "#5", "#6"):
            return

        col_index = int(col[1:]) - 1
        old_value = tabla.item(item, "values")[col_index]
        entry = tk.Entry(frame_tabla, font=("Segoe UI", 11))
        entry.insert(0, old_value)
        entry.focus()

        bbox = tabla.bbox(item, col)
        if not bbox:
            return
        entry.place(x=bbox[0] + 2, y=bbox[1] + 2, width=bbox[2] - 4, height=bbox[3] - 4)

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

    # guardar resultados en la base de datos
    def guardar_resultados():
        filas = tabla.get_children()
        actualizados = 0

        for f in filas:
            valores = tabla.item(f, "values")
            (
                idPartido, _, _, _, _, _,
                g1, g2, a1, a2, r1, r2
            ) = valores

            # si no hay goles cargados, ignorar
            if not g1.strip() and not g2.strip() and not a1.strip() and not a2.strip() and not r1.strip() and not r2.strip():
                continue

            try:
                datos = (
                    int(g1 or 0),
                    int(g2 or 0),
                    int(a1 or 0),
                    int(a2 or 0),
                    int(r1 or 0),
                    int(r2 or 0),
                    int(idPartido)
                )
            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"Valores inválidos en el partido ID {idPartido}. Usa solo números."
                )
                return

            update_partido(datos)
            actualizados += 1

        if actualizados > 0:
            messagebox.showinfo("Éxito", f"Se actualizaron {actualizados} partido(s) correctamente ✅")
            pantalla_resultados(ventana, volver_menu)
        else:
            messagebox.showinfo("Sin cambios", "No se ingresaron resultados.")

    # función para cerrar jornada
    def cerrar_jornada_accion():
        """
        Verifica que todos los partidos tengan resultados y cierra la jornada
        """
        # Verificar que todos los partidos de la jornada actual tengan al menos goles cargados
        partidos_sin_resultados = []
        filas = tabla.get_children()
        
        for f in filas:
            valores = tabla.item(f, "values")
            idPartido, equipo1, equipo2, _, _, _, g1, g2, a1, a2, r1, r2 = valores
            
            # Verificar si faltan goles (campos obligatorios)
            if not g1.strip() or not g2.strip():
                partidos_sin_resultados.append(f"{equipo1} vs {equipo2} (ID: {idPartido})")
        
        if partidos_sin_resultados:
            messagebox.showwarning(
                "Jornada Incompleta", 
                f"No puedes cerrar la jornada {jornada_actual}. \n"
                f"Faltan resultados en los siguientes partidos:\n\n" +
                "\n".join(partidos_sin_resultados)
            )
            return
        
        # Confirmar cierre de jornada
        if messagebox.askyesno(
            "Confirmar Cierre", 
            f"¿Estás seguro de cerrar la Jornada {jornada_actual}?\n\n"
            "Una vez cerrada, no podrás modificar los resultados.\n"
            "Esta acción avanzará a la siguiente jornada."
        ):
            try:
                nueva_jornada = cerrar_jornada()
                messagebox.showinfo(
                    "Jornada Cerrada", 
                    f"✅ Jornada {jornada_actual} cerrada exitosamente.\n"
                    f"🏁 Ahora estás en la Jornada {nueva_jornada}"
                )
                # Recargar la pantalla para mostrar la nueva jornada
                pantalla_resultados(ventana, volver_menu)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cerrar la jornada: {str(e)}")

    # volver al menú
    def volver():
        volver_menu(ventana)

    # marco de botones
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

    btn_cerrar_jornada = tk.Button(
        frame_botones,
        text="🏁 Cerrar Jornada",
        font=("Segoe UI", 12),
        bg="#e74c3c",
        fg="white",
        width=20,
        command=cerrar_jornada_accion
    )
    btn_cerrar_jornada.grid(row=0, column=1, padx=10)

    btn_volver = tk.Button(
        frame_botones,
        text="⬅ Volver al Menú",
        font=("Segoe UI", 12),
        bg="#68ab98",
        fg="white",
        width=20,
        command=volver
    )
    btn_volver.grid(row=0, column=2, padx=10)

    # pie de página
    tk.Label(
        ventana,
        text=f"Desarrollado por Sintax FC — Jornada {jornada_actual}",
        font=("Segoe UI", 9, "italic"),
        fg="#666666",
        bg="#f8f8f8"
    ).pack(side="bottom", pady=5)