import tkinter as tk
from tkinter import ttk, messagebox
from controllers.partido import get_partidos, update_partido
from controllers.penales import registrar_penales, get_penales_por_partido
from utils import ultima_fecha_jornada, cerrar_jornada, carga_completa_fechas
from controllers.pool import conectar  # 🔧 AGREGADO: Para consultar el ganador


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
        text="⚽ Registro de Resultados de los Partidos",
        font=("Segoe UI", 18, "bold"),
        fg="#333333",
        bg="#f8f8f8"
    ).pack(pady=20)

    # obtener jornada actual desde la tabla estado_torneo
    jornada_actual = ultima_fecha_jornada()

    # Verificar si el torneo terminó
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

    # 🔧 CORREGIDO: Ahora incluye penales desde octavos (jornada 4) en adelante
    if jornada_actual >= 4:  # Cambiado de 5 a 4 para incluir octavos
        columnas += ("penales1", "penales2")

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

    # 🔧 CORREGIDO: Agregar encabezados de penales desde octavos
    if jornada_actual >= 4:  # Cambiado de 5 a 4 para incluir octavos
        encabezados["penales1"] = "Penales E1"
        encabezados["penales2"] = "Penales E2"

    for col in columnas:
        tabla.heading(col, text=encabezados[col])
        tabla.column(col, anchor="center", width=85)

    # obtener todos los partidos
    partidos = get_partidos()

    # filtrar solo los de la jornada actual
    partidos_actual = [p for p in partidos if int(p[13]) == int(jornada_actual)]

    # si no hay partidos para esa jornada
    if not partidos_actual:
        messagebox.showinfo("Información", "No hay más partidos en el torneo.")
        volver_menu(ventana)
        return

    # cargar datos en la tabla
    for p in partidos_actual:
        # 🔧 CORREGIDO: Buscar penales desde octavos (jornada 4)
        penales = get_penales_por_partido(p[0]) if jornada_actual >= 4 else None

        # Si no hay registro de penales, inicializamos en (0, 0)
        if penales is None:
            penales = (0, 0)

        valores = (
            p[0], p[3], p[4], p[13], p[1], p[2],
            p[7] if p[7] is not None else "0",
            p[8] if p[8] is not None else "0",
            p[9] if p[9] is not None else "0",
            p[10] if p[10] is not None else "0",
            p[11] if p[11] is not None else "0",
            p[12] if p[12] is not None else "0",
        )

        # 🔧 CORREGIDO: Agregar penales desde octavos
        if jornada_actual >= 4:  # Cambiado de 5 a 4 para incluir octavos
            valores += (
                str(penales[0]),
                str(penales[1])
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

        entry.bind("<Return>", guardar_editado)
        entry.bind("<FocusOut>", guardar_editado)

    tabla.bind("<Double-1>", editar_celda)

    # 🔧 NUEVA FUNCIÓN: Determinar ganador de la final
    def determinar_ganador_final():
        """
        Determina el ganador del partido de la final
        """
        if jornada_actual != 8:
            return None
            
        conn = conectar()
        cursor = conn.cursor()
        
        # Buscar el partido de la final (jornada 8)
        cursor.execute("""
            SELECT p.idPartido, p.identificadorEquipoUno, p.identificadorEquipoDos,
                   p.golesEquipoUno, p.golesEquipoDos, 
                   e1.pais AS equipo1, e2.pais AS equipo2
            FROM partido p
            JOIN equipos e1 ON p.identificadorEquipoUno = e1.identificador
            JOIN equipos e2 ON p.identificadorEquipoDos = e2.identificador
            WHERE p.jornada = 8
        """)
        
        final = cursor.fetchone()
        conn.close()
        
        if not final:
            return None
            
        id_partido, id_equipo1, id_equipo2, goles1, goles2, equipo1, equipo2 = final
        
        # Verificar si el partido tiene resultados
        if goles1 is None or goles2 is None:
            return None
            
        # Determinar ganador considerando penales
        if goles1 > goles2:
            return equipo1
        elif goles2 > goles1:
            return equipo2
        else:
            # Empate - verificar penales
            penales = get_penales_por_partido(id_partido)
            if penales and penales != (0, 0):
                p1, p2 = penales
                if p1 > p2:
                    return equipo1
                else:
                    return equipo2
            else:
                return None

    # guardar resultados
    def guardar_resultados():
        filas = tabla.get_children()
        actualizados = 0

        for f in filas:
            valores = tabla.item(f, "values")
            
            # 🔧 CORREGIDO: Manejar diferentes estructuras según la jornada
            if jornada_actual < 4:  # Fase de grupos
                idPartido, _, _, _, _, _, g1, g2, a1, a2, r1, r2 = valores
            else:  # Octavos en adelante
                idPartido, _, _, _, _, _, g1, g2, a1, a2, r1, r2, p1, p2 = valores

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

                # 🔧 CORREGIDO: Registrar penales desde octavos
                if jornada_actual >= 4:  # Cambiado de 5 a 4 para incluir octavos
                    registrar_penales(int(idPartido),
                                      int(p1) if p1.strip() else 0,
                                      int(p2) if p2.strip() else 0)
                actualizados += 1
            except ValueError:
                messagebox.showerror("Error", f"Valores inválidos en el partido ID {idPartido}.")
                return

        if actualizados > 0:
            # 🔧 AGREGADO: Mostrar mensaje del ganador si es la final
            if jornada_actual == 8:
                ganador = determinar_ganador_final()
                if ganador:
                    messagebox.showinfo(
                        "🏆 ¡CAMPEÓN DEL TORNEO!",
                        f"¡FELICITACIONES! 🎉\n\n"
                        f"🏆 {ganador} ES EL CAMPEÓN DEL TORNEO! 🏆\n\n"
                        f"¡El torneo ha concluido con un gran campeón!\n"
                        f"Puedes revisar todos los resultados en los informes."
                    )
                else:
                    messagebox.showinfo("✅ Cambios Guardados", f"Se actualizaron {actualizados} partido(s).")
            else:
                messagebox.showinfo("✅ Cambios Guardados", f"Se actualizaron {actualizados} partido(s).")
            
            pantalla_resultados(ventana, volver_menu)
        else:
            messagebox.showinfo("Sin cambios", "No se detectaron resultados nuevos.")

    # cerrar jornada
    def cerrar_jornada_accion():
        filas = tabla.get_children()
        partidos_sin_resultado = []

        for f in filas:
            valores = tabla.item(f, "values")
            g1, g2 = valores[6], valores[7]
            if not g1.strip() or not g2.strip():
                partidos_sin_resultado.append(valores[1] + " vs " + valores[2])

        if partidos_sin_resultado:
            messagebox.showwarning(
                "Jornada Incompleta",
                f"No puedes cerrar la jornada {jornada_actual}.\nFaltan resultados en:\n\n" +
                "\n".join(partidos_sin_resultado)
            )
            return

        # 🔧 AGREGADO: Validación especial para empates en fase eliminatoria (octavos en adelante)
        if jornada_actual >= 4:
            partidos_con_empate_sin_penales = []
            for f in filas:
                valores = tabla.item(f, "values")
                g1, g2 = int(valores[6].strip() or 0), int(valores[7].strip() or 0)
                p1, p2 = int(valores[12].strip() or 0), int(valores[13].strip() or 0)
                
                # Si hay empate en goles pero no se registraron penales
                if g1 == g2 and p1 == 0 and p2 == 0:
                    partidos_con_empate_sin_penales.append(valores[1] + " vs " + valores[2])
            
            if partidos_con_empate_sin_penales:
                messagebox.showwarning(
                    "Empates sin Penales",
                    f"En la fase eliminatoria, los empates deben resolverse por penales.\n\n"
                    f"Partidos con empate sin penales registrados:\n" +
                    "\n".join(partidos_con_empate_sin_penales) +
                    f"\n\nPor favor, registra los resultados de penales antes de cerrar la jornada."
                )
                return

        if messagebox.askyesno(
            "Confirmar Cierre",
            f"¿Cerrar Jornada {jornada_actual}?\nEsta acción no se podrá deshacer."
        ):
            nueva_jornada = cerrar_jornada()
            
            # 🔧 AGREGADO: Mensaje especial si se cerró la final
            if jornada_actual == 8:
                ganador = determinar_ganador_final()
                if ganador:
                    mensaje = (f"✅ Jornada {jornada_actual} cerrada.\n\n"
                              f"🏆 ¡EL TORNEO HA CONCLUIDO! 🏆\n\n"
                              f"🎉 {ganador} ES EL CAMPEÓN DEL TORNEO! 🎉\n\n"
                              f"¡Felicidades al gran campeón!")
                else:
                    mensaje = f"✅ Jornada {jornada_actual} cerrada.\nSiguiente: {nueva_jornada}"
            else:
                mensaje = f"✅ Jornada {jornada_actual} cerrada.\nSiguiente: {nueva_jornada}"
            
            messagebox.showinfo("Jornada Cerrada", mensaje)
            pantalla_resultados(ventana, volver_menu)

    # volver
    def volver():
        volver_menu(ventana)

    # marco de botones
    frame_botones = tk.Frame(ventana, bg="#f8f8f8")
    frame_botones.pack(pady=20)

    tk.Button(
        frame_botones, text="💾 Guardar Resultados",
        font=("Segoe UI", 12), bg="#68ab98", fg="white", width=20,
        command=guardar_resultados
    ).grid(row=0, column=0, padx=10)

    if jornada_actual < 8:
        tk.Button(
            frame_botones, text="🏁 Cerrar Jornada",
            font=("Segoe UI", 12), bg="#e74c3c", fg="white", width=20,
            command=cerrar_jornada_accion
        ).grid(row=0, column=1, padx=10)
    else:
        def mostrar_final_torneo():
            ganador = determinar_ganador_final()
            if ganador:
                messagebox.showinfo(
                    "🏆 Final del Torneo",
                    f"¡Esta es la última jornada del torneo!\n\n"
                    f"🏆 CAMPEÓN ACTUAL: {ganador} 🏆\n\n"
                    f"Si guardas nuevos resultados, se actualizará el campeón."
                )
            else:
                messagebox.showinfo(
                    "🏆 Final del Torneo", 
                    "¡Esta es la última jornada del torneo!\n\n"
                    "Aún no hay un campeón definido. Guarda los resultados para coronar al ganador."
                )

        tk.Button(
            frame_botones, text="🏆 Final del Torneo",
            font=("Segoe UI", 12), bg="#f39c12", fg="white", width=20,
            command=mostrar_final_torneo
        ).grid(row=0, column=1, padx=10)

    tk.Button(
        frame_botones, text="⬅ Volver al Menú",
        font=("Segoe UI", 12), bg="#68ab98", fg="white", width=20,
        command=volver
    ).grid(row=0, column=2, padx=10)

    # 🔧 AGREGADO: Información sobre penales para fase eliminatoria
    if jornada_actual >= 4:
        tk.Label(
            ventana,
            text="💡 RECUERDA: En fase eliminatoria, los empates se resuelven por penales",
            font=("Segoe UI", 10, "italic"),
            fg="#e74c3c", bg="#f8f8f8"
        ).pack(side="bottom", pady=5)

    # 🔧 AGREGADO: Mensaje especial para la final
    if jornada_actual == 8:
        ganador = determinar_ganador_final()
        if ganador:
            tk.Label(
                ventana,
                text=f"🏆 CAMPEÓN ACTUAL: {ganador}",
                font=("Segoe UI", 12, "bold"),
                fg="#f39c12", bg="#f8f8f8"
            ).pack(side="bottom", pady=5)
        else:
            tk.Label(
                ventana,
                text="🏆 GUARDA LOS RESULTADOS PARA CORONAR AL CAMPEÓN",
                font=("Segoe UI", 11, "bold"),
                fg="#e74c3c", bg="#f8f8f8"
            ).pack(side="bottom", pady=5)

    tk.Label(
        ventana,
        text=f"Desarrollado por Sintax FC — Jornada {jornada_actual}",
        font=("Segoe UI", 9, "italic"),
        fg="#666666", bg="#f8f8f8"
    ).pack(side="bottom", pady=5)