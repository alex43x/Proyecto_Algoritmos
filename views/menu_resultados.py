import tkinter as tk
from tkinter import ttk, messagebox
from controllers.partido import get_partidos, update_partido
from utils import ultima_fecha_jornada, cerrar_jornada, carga_completa_fechas


def pantalla_resultados(ventana, volver_menu):
    # limpiar la ventana principal
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.configure(bg="#f8f8f8")

    # Verificar si todas las fechas están cargadas
    if not carga_completa_fechas():
        messagebox.showwarning(
            "Calendario Incompleto", 
            "No se pueden registrar resultados hasta que todas las fechas y horas de los partidos estén cargadas.\n\n"
            "Por favor, completa primero el calendario en la Configuración del Torneo."
        )
        volver_menu(ventana)
        return

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

    # Verificar si es la última jornada (jornada 8)
    if jornada_actual > 8:
        messagebox.showinfo(
            "Torneo Finalizado", 
            "🏆 ¡El torneo ha finalizado! No hay más jornadas por jugar.\n\n"
            "Todas las jornadas han sido completadas."
        )
        volver_menu(ventana)
        return

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
        messagebox.showinfo("Información", "No hay más partidos en el torneo.")
        volver_menu(ventana)
        return

    # cargar datos en la tabla - MOSTRAR "0" EN LUGAR DE VACÍO
    for p in partidos_actual:
        valores = (
            p[0],  # idPartido
            p[3],  # equipo1_nombre
            p[4],  # equipo2_nombre
            p[13], # jornada
            p[1],  # fecha
            p[2],  # hora
            p[7] if p[7] is not None else "0",  # golesEquipoUno (mostrar "0" si es None o 0)
            p[8] if p[8] is not None else "0",  # golesEquipoDos (mostrar "0" si es None o 0)
            p[9] if p[9] is not None else "0",  # tarjetasAmarillasEquipoUno
            p[10] if p[10] is not None else "0", # tarjetasAmarillasEquipoDos
            p[11] if p[11] is not None else "0", # tarjetasRojasEquipoUno
            p[12] if p[12] is not None else "0"  # tarjetasRojasEquipoDos
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

        def guardar_editado(_=None):
            nuevo_valor = entry.get().strip()
            valores = list(tabla.item(item, "values"))
            valores[col_index] = nuevo_valor
            tabla.item(item, values=valores)
            entry.destroy()

        def destruir_entry(_=None):
            # Guardar el valor antes de destruir el entry
            guardar_editado()

        entry.bind("<Return>", guardar_editado)
        entry.bind("<FocusOut>", destruir_entry)

    tabla.bind("<Double-1>", editar_celda)

    # guardar resultados en la base de datos
    def guardar_resultados():
        filas = tabla.get_children()
        actualizados = 0
        cambios_detectados = False

        for f in filas:
            valores = tabla.item(f, "values")
            (
                idPartido, _, _, _, _, _,
                g1, g2, a1, a2, r1, r2
            ) = valores

            # Verificar si hay al menos un campo con datos (no vacío)
            tiene_datos = (g1.strip() or g2.strip() or a1.strip() or a2.strip() or r1.strip() or r2.strip())

            if tiene_datos:
                cambios_detectados = True
                
                # Verificar que los goles obligatorios estén completos si hay otros datos
                tiene_goles = g1.strip() or g2.strip()
                goles_incompletos = (g1.strip() and not g2.strip()) or (not g1.strip() and g2.strip())
                
                if tiene_goles and goles_incompletos:
                    messagebox.showwarning(
                        "Datos incompletos",
                        f"El partido ID {idPartido} tiene datos incompletos.\n"
                        "Si ingresas goles, debes completar los goles de ambos equipos."
                    )
                    return

                try:
                    # Convertir campos vacíos a 0, campos con texto a número
                    datos = (
                        int(g1) if g1.strip() else 0,
                        int(g2) if g2.strip() else 0,
                        int(a1) if a1.strip() else 0,
                        int(a2) if a2.strip() else 0,
                        int(r1) if r1.strip() else 0,
                        int(r2) if r2.strip() else 0,
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
            messagebox.showinfo("Cambios Guardados", f"Se actualizaron {actualizados} partido(s) correctamente ✅")
            pantalla_resultados(ventana, volver_menu)
        elif cambios_detectados:
            messagebox.showinfo("Sin cambios", "Se detectaron datos pero no se pudieron guardar debido a errores.")
        else:
            messagebox.showinfo("Sin cambios", "No se ingresaron resultados.")

    # función para cerrar jornada
    def cerrar_jornada_accion():
        """
        Verifica que todos los partidos tengan resultados y cierra la jornada
        """
        # Verificar que todos los partidos de la jornada actual tengan al menos goles cargados
        partidos_sin_resultados = []
        partidos_con_datos_parciales = []
        filas = tabla.get_children()
        
        for f in filas:
            valores = tabla.item(f, "values")
            idPartido, equipo1, equipo2, _, _, _, g1, g2, a1, a2, r1, r2 = valores
            
            # Verificar si faltan goles (campos obligatorios)
            if not g1.strip() or not g2.strip():
                # Verificar si tiene otros datos pero le faltan goles
                otros_datos = a1.strip() or a2.strip() or r1.strip() or r2.strip()
                
                if otros_datos:
                    partidos_con_datos_parciales.append(f"{equipo1} vs {equipo2} (ID: {idPartido})")
                else:
                    partidos_sin_resultados.append(f"{equipo1} vs {equipo2} (ID: {idPartido})")
        
        if partidos_con_datos_parciales:
            messagebox.showwarning(
                "Datos incompletos", 
                f"No puedes cerrar la jornada {jornada_actual}. \n"
                f"Los siguientes partidos tienen tarjetas pero faltan goles:\n\n" +
                "\n".join(partidos_con_datos_parciales) +
                "\n\nPor favor, completa los goles de ambos equipos."
            )
            return
            
        if partidos_sin_resultados:
            messagebox.showwarning(
                "Jornada Incompleta", 
                f"No puedes cerrar la jornada {jornada_actual}. \n"
                f"Faltan resultados en los siguientes partidos:\n\n" +
                "\n".join(partidos_sin_resultados) +
                "\n\nTodos los partidos deben tener al menos los goles cargados."
            )
            return
        
        # Primero guardar todos los resultados para asegurar consistencia
        filas = tabla.get_children()
        for f in filas:
            valores = tabla.item(f, "values")
            (
                idPartido, _, _, _, _, _,
                g1, g2, a1, a2, r1, r2
            ) = valores

            if g1.strip() or g2.strip():
                try:
                    datos = (
                        int(g1) if g1.strip() else 0,
                        int(g2) if g2.strip() else 0,
                        int(a1) if a1.strip() else 0,
                        int(a2) if a2.strip() else 0,
                        int(r1) if r1.strip() else 0,
                        int(r2) if r2.strip() else 0,
                        int(idPartido)
                    )
                    update_partido(datos)
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        f"Valores inválidos en el partido ID {idPartido}. No se pudo cerrar la jornada."
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

    # Función para mostrar información del final del torneo
    def mostrar_final_torneo():
        messagebox.showinfo("Final del Torneo", "¡Esta es la última jornada del torneo!")

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

    # Solo mostrar botón de cerrar jornada si no es la última jornada
    if jornada_actual < 8:
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
    else:
        # Para la última jornada, mostrar un botón especial
        btn_final_torneo = tk.Button(
            frame_botones,
            text="🏆 Final del Torneo",
            font=("Segoe UI", 12),
            bg="#f39c12",
            fg="white",
            width=20,
            command=mostrar_final_torneo
        )
        btn_final_torneo.grid(row=0, column=1, padx=10)

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