import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import tkinter.font as tkfont
from controllers.equipos import get_equipo
from controllers.grupos import get_grupo
from Informes import InformeUno, InformeDos, InformeTres, InformeCuatro, InformeCinco


def pantalla_informes(ventana, volver_menu):
    """
    Pantalla principal para la emisión de informes del torneo
    """
    # limpiar la ventana principal
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.configure(bg="#f8f8f8")

    # título principal
    tk.Label(
        ventana,
        text="📊 Emisión de Informes del Torneo",
        font=("Segoe UI", 20, "bold"),
        fg="#333333",
        bg="#f8f8f8"
    ).pack(pady=20)

    # frame principal
    frame_principal = tk.Frame(ventana, bg="#f8f8f8")
    frame_principal.pack(fill="both", expand=True, padx=30, pady=10)

    # frame para los botones de informes
    frame_botones = tk.Frame(frame_principal, bg="#f8f8f8")
    frame_botones.pack(side="left", fill="y", padx=(0, 20))

    # frame para mostrar los resultados
    frame_resultados = tk.Frame(frame_principal, bg="white", bd=2, relief="groove")
    frame_resultados.pack(side="right", fill="both", expand=True)

    # título del área de resultados
    tk.Label(
        frame_resultados,
        text="Resultados del Informe",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#333333"
    ).pack(pady=10)

    # área de texto para mostrar resultados
    texto_resultados = tk.Text(
        frame_resultados,
        wrap=tk.WORD,
        font=("Segoe UI", 10),
        bg="#fafafa",
        fg="#333333",
        padx=10,
        pady=10,
        width=80,
        height=25
    )
    texto_resultados.pack(fill="both", expand=True, padx=10, pady=10)
    texto_resultados.config(state=tk.DISABLED)

    # scrollbar para el área de texto
    scrollbar = tk.Scrollbar(texto_resultados)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    texto_resultados.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=texto_resultados.yview)

    def limpiar_resultados():
        texto_resultados.config(state=tk.NORMAL)
        texto_resultados.delete(1.0, tk.END)
        texto_resultados.config(state=tk.DISABLED)

    def mostrar_resultados(texto):
        texto_resultados.config(state=tk.NORMAL)
        texto_resultados.delete(1.0, tk.END)
        texto_resultados.insert(tk.END, texto)
        texto_resultados.config(state=tk.DISABLED)

    # estilo común para los botones
    estilo_boton = {
        "font": ("Segoe UI", 11, "bold"),
        "bg": "#68ab98",
        "fg": "white",
        "activebackground": "#5a9686",
        "activeforeground": "white",
        "relief": "flat",
        "width": 25,
        "height": 2,
        "cursor": "hand2"
    }

    # FUNCIÓN 1: Partidos por fecha
    def informe_partidos_fecha():
        limpiar_resultados()

        ventana_fecha = tk.Toplevel(ventana)
        ventana_fecha.title("Partidos por Fecha")
        ventana_fecha.configure(bg="#f8f8f8")
        ventana_fecha.geometry("300x150")
        ventana_fecha.transient(ventana)
        ventana_fecha.grab_set()

        tk.Label(ventana_fecha, text="Ingrese la fecha (YYYY-MM-DD):",
                 font=("Segoe UI", 11), bg="#f8f8f8").pack(pady=10)

        entry_fecha = tk.Entry(ventana_fecha, font=("Segoe UI", 11), justify="center")
        entry_fecha.pack(pady=5)
        entry_fecha.focus()

        def generar_informe():
            fecha = entry_fecha.get().strip()
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                resultados = InformeUno(fecha)
                ventana_fecha.destroy()

                if not resultados:
                    mostrar_resultados(f"No hay partidos programados para la fecha {fecha}")
                    return

                texto = f"📅 PARTIDOS PROGRAMADOS PARA {fecha}\n\n"
                texto += "=" * 60 + "\n\n"

                for id_partido, fecha_p, equipo1, equipo2, jornada, fase, hora, estadio in resultados:
                    texto += f"⏰ {hora} - {equipo1} vs {equipo2}\n"
                    texto += f"   📍 {fase} - Jornada {jornada}\n"
                    texto += f"   🏟️ Estadio: {estadio}\n"
                    texto += f"   🆔 Partido ID: {id_partido}\n"
                    texto += "-" * 40 + "\n"

                mostrar_resultados(texto)

            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")

        tk.Button(ventana_fecha, text="Generar Informe", command=generar_informe,
                  bg="#68ab98", fg="white", font=("Segoe UI", 10)).pack(pady=10)

    # FUNCIÓN 2: Tabla de posiciones por grupo
    def informe_tabla_grupo():
        limpiar_resultados()
        ventana_grupo = tk.Toplevel(ventana)
        ventana_grupo.title("Tabla de Posiciones por Grupo")
        ventana_grupo.configure(bg="#f8f8f8")
        ventana_grupo.geometry("350x180")
        ventana_grupo.transient(ventana)
        ventana_grupo.grab_set()

        tk.Label(ventana_grupo, text="Seleccione el grupo:",
                 font=("Segoe UI", 11), bg="#f8f8f8").pack(pady=5)

        grupos = [g[1] for g in get_grupo()]
        combo_grupo = ttk.Combobox(ventana_grupo, values=grupos, state="readonly",
                                   font=("Segoe UI", 10))
        combo_grupo.pack(pady=5)
        if grupos:
            combo_grupo.set(grupos[0])

        tk.Label(ventana_grupo, text="Fecha límite (YYYY-MM-DD):",
                 font=("Segoe UI", 11), bg="#f8f8f8").pack(pady=5)

        entry_fecha = tk.Entry(ventana_grupo, font=("Segoe UI", 11), justify="center")
        entry_fecha.pack(pady=5)

        def generar_informe():
            grupo = combo_grupo.get()
            fecha = entry_fecha.get().strip()

            if not grupo or not fecha:
                messagebox.showerror("Error", "Debe completar ambos campos")
                return

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                grupo_nombre, fecha_limite, tabla = InformeDos(grupo, fecha)
                ventana_grupo.destroy()

                if not tabla:
                    mostrar_resultados(f"No hay datos para el grupo {grupo} hasta la fecha {fecha}")
                    return

                texto = f"🏆 TABLA DE POSICIONES - GRUPO {grupo_nombre}\n"
                texto += f"📅 Hasta: {fecha_limite}\n\n"
                texto += "=" * 70 + "\n"
                texto += f"{'Equipo':<15} {'PJ':<3} {'PG':<3} {'PE':<3} {'PP':<3} {'GF':<3} {'GC':<3} {'DG':<4} {'Pts':<3}\n"
                texto += "=" * 70 + "\n"

                for pais, PJ, PG, PE, PP, GF, GC, DG, Pts in tabla:
                    texto += f"{pais:<15} {PJ:<3} {PG:<3} {PE:<3} {PP:<3} {GF:<3} {GC:<3} {DG:<4} {Pts:<3}\n"

                mostrar_resultados(texto)

            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")

        tk.Button(ventana_grupo, text="Generar Informe", command=generar_informe,
                  bg="#68ab98", fg="white", font=("Segoe UI", 10)).pack(pady=10)

    # FUNCIÓN 3: Cuadro de resultados por equipo
    def informe_cuadro_equipo():
        limpiar_resultados()

        ventana_equipo = tk.Toplevel(ventana)
        ventana_equipo.title("Cuadro de Resultados por Equipo")
        ventana_equipo.configure(bg="#f8f8f8")
        ventana_equipo.geometry("350x180")
        ventana_equipo.transient(ventana)
        ventana_equipo.grab_set()

        tk.Label(ventana_equipo, text="Seleccione el equipo:",
                 font=("Segoe UI", 11), bg="#f8f8f8").pack(pady=5)

        equipos = [e[1] for e in get_equipo()]
        combo_equipo = ttk.Combobox(ventana_equipo, values=equipos, state="readonly",
                                    font=("Segoe UI", 10))
        combo_equipo.pack(pady=5)
        if equipos:
            combo_equipo.set(equipos[0])

        tk.Label(ventana_equipo, text="Fecha límite (YYYY-MM-DD):",
                 font=("Segoe UI", 11), bg="#f8f8f8").pack(pady=5)

        entry_fecha = tk.Entry(ventana_equipo, font=("Segoe UI", 11), justify="center")
        entry_fecha.pack(pady=5)

        def generar_informe():
            equipo = combo_equipo.get()
            fecha = entry_fecha.get().strip()

            if not equipo or not fecha:
                messagebox.showerror("Error", "Debe completar ambos campos")
                return

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                equipo_nombre, fecha_limite, partidos, estado = InformeTres(equipo, fecha)
                ventana_equipo.destroy()

                texto = f"⚽ CUADRO DE RESULTADOS - {equipo_nombre}\n"
                texto += f"📅 Hasta: {fecha_limite}\n"
                texto += f"📊 Estado: {estado}\n\n"
                texto += "=" * 60 + "\n\n"

                if not partidos:
                    texto += "No hay partidos disputados hasta esta fecha\n"
                else:
                    for fecha_p, fase, eq1, g1, eq2, g2, estadio in partidos:
                        texto += f"📅 {fecha_p} - {fase}\n"
                        texto += f"   {eq1} {g1} - {g2} {eq2}\n"
                        texto += f"   🏟️ Estadio: {estadio}\n"
                        texto += "-" * 40 + "\n"

                mostrar_resultados(texto)

            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")

        tk.Button(ventana_equipo, text="Generar Informe", command=generar_informe,
                  bg="#68ab98", fg="white", font=("Segoe UI", 10)).pack(pady=10)

    # FUNCIÓN 4: Próximo partido de un equipo
    def informe_proximo_partido():
        limpiar_resultados()

        ventana_equipo = tk.Toplevel(ventana)
        ventana_equipo.title("Próximo Partido de un Equipo")
        ventana_equipo.configure(bg="#f8f8f8")
        ventana_equipo.geometry("350x150")
        ventana_equipo.transient(ventana)
        ventana_equipo.grab_set()

        tk.Label(ventana_equipo, text="Seleccione el equipo:",
                 font=("Segoe UI", 11), bg="#f8f8f8").pack(pady=5)

        equipos = [e[1] for e in get_equipo()]
        combo_equipo = ttk.Combobox(ventana_equipo, values=equipos, state="readonly",
                                    font=("Segoe UI", 10))
        combo_equipo.pack(pady=5)
        if equipos:
            combo_equipo.set(equipos[0])

        tk.Label(ventana_equipo, text="Fecha de referencia (YYYY-MM-DD):",
                 font=("Segoe UI", 11), bg="#f8f8f8").pack(pady=5)

        entry_fecha = tk.Entry(ventana_equipo, font=("Segoe UI", 11), justify="center")
        entry_fecha.pack(pady=5)

        def generar_informe():
            equipo = combo_equipo.get()
            fecha = entry_fecha.get().strip()

            if not equipo or not fecha:
                messagebox.showerror("Error", "Debe completar ambos campos")
                return

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                equipo_nombre, fecha_ref, partido = InformeCuatro(equipo, fecha)
                ventana_equipo.destroy()

                texto = f"⏭️  PRÓXIMO PARTIDO - {equipo_nombre}\n"
                texto += f"📅 Fecha de referencia: {fecha_ref}\n\n"
                texto += "=" * 50 + "\n\n"

                if not partido:
                    texto += "No hay partidos programados después de esta fecha\n"
                else:
                    fecha_p, hora, eq1, eq2, jornada, fase, estadio = partido
                    texto += f"📅 Fecha: {fecha_p}\n"
                    texto += f"⏰ Hora: {hora}\n"
                    texto += f"⚽ Partido: {eq1} vs {eq2}\n"
                    texto += f"📍 {fase} - Jornada {jornada}\n"
                    texto += f"🏟️ Estadio: {estadio}\n"

                mostrar_resultados(texto)

            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")

        tk.Button(ventana_equipo, text="Generar Informe", command=generar_informe,
                  bg="#68ab98", fg="white", font=("Segoe UI", 10)).pack(pady=10)

    # FUNCIÓN 5: Tabla general de todos los grupos
    def informe_tabla_general():
        limpiar_resultados()

        ventana_fecha = tk.Toplevel(ventana)
        ventana_fecha.title("Tabla General de Todos los Grupos")
        ventana_fecha.configure(bg="#f8f8f8")
        ventana_fecha.geometry("300x120")
        ventana_fecha.transient(ventana)
        ventana_fecha.grab_set()

        tk.Label(ventana_fecha, text="Fecha límite (YYYY-MM-DD):",
                 font=("Segoe UI", 11), bg="#f8f8f8").pack(pady=10)

        entry_fecha = tk.Entry(ventana_fecha, font=("Segoe UI", 11), justify="center")
        entry_fecha.pack(pady=5)
        entry_fecha.focus()

        def generar_informe():
            fecha = entry_fecha.get().strip()
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                resultados = InformeCinco(fecha)
                ventana_fecha.destroy()

                texto = f"🏆 TABLA GENERAL DE POSICIONES\n"
                texto += f"📅 Hasta: {fecha}\n\n"
                texto += "=" * 70 + "\n\n"

                if not resultados:
                    texto += "No hay datos disponibles para los grupos\n"
                else:
                    for fecha_g, grupo, tabla in resultados:
                        texto += f"📊 GRUPO {grupo}\n"
                        texto += "=" * 70 + "\n"
                        texto += f"{'Equipo':<15} {'PJ':<3} {'PG':<3} {'PE':<3} {'PP':<3} {'GF':<3} {'GC':<3} {'DG':<4} {'Pts':<3}\n"
                        texto += "-" * 70 + "\n"

                        for pais, PJ, PG, PE, PP, GF, GC, DG, Pts in tabla:
                            texto += f"{pais:<15} {PJ:<3} {PG:<3} {PE:<3} {PP:<3} {GF:<3} {GC:<3} {DG:<4} {Pts:<3}\n"

                        texto += "\n" + "═" * 70 + "\n\n"

                mostrar_resultados(texto)

            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")

        tk.Button(ventana_fecha, text="Generar Informe", command=generar_informe,
                  bg="#68ab98", fg="white", font=("Segoe UI", 10)).pack(pady=10)

    # BOTONES DE INFORMES
    tk.Button(
        frame_botones,
        text="📅 Partidos por Fecha",
        command=informe_partidos_fecha,
        **estilo_boton
    ).pack(pady=8)

    tk.Button(
        frame_botones,
        text="🏆 Tabla por Grupo",
        command=informe_tabla_grupo,
        **estilo_boton
    ).pack(pady=8)

    tk.Button(
        frame_botones,
        text="⚽ Cuadro por Equipo",
        command=informe_cuadro_equipo,
        **estilo_boton
    ).pack(pady=8)

    tk.Button(
        frame_botones,
        text="⏭️  Próximo Partido",
        command=informe_proximo_partido,
        **estilo_boton
    ).pack(pady=8)

    tk.Button(
        frame_botones,
        text="📊 Tabla General",
        command=informe_tabla_general,
        **estilo_boton
    ).pack(pady=8)

    # botón volver
    def volver():
        volver_menu(ventana)

    tk.Button(
        frame_botones,
        text="⬅ Volver al Menú",
        command=volver,
        **estilo_boton
    ).pack(pady=15)

    # pie de página
    tk.Label(
        ventana,
        text="Desarrollado por Sintax FC — Módulo de Informes",
        font=("Segoe UI", 9, "italic"),
        fg="#666666",
        bg="#f8f8f8"
    ).pack(side="bottom", pady=5)