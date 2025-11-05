import tkinter as tk
from tkinter import messagebox
from controllers.pool import crear_tablas
from controllers.torneo import get_torneos
from models.equipos import Equipos
from models.torneo import Torneo
from models.partido import Partido
import datetime

def crear_datos():
    crear_tablas()

    equipo1 = Equipos(
        identificador="A1",
        pais="Chile",
        abreviatura="CHI",
        confederacion="CONMEBOL",
        idGrupo="1"
    )
    equipo2 = Equipos(
        identificador="A3",
        pais="Paraguay",
        abreviatura="PAR",
        confederacion="CONMEBOL",
        idGrupo="1"
    )

    id1 = equipo1.guardar()
    id2 = equipo2.guardar()

    partido = Partido(
        anio=2025, mes=11, dia=25, minuto=30, horaDeInicio=13,
        identificadorEquipoUno=equipo1.identificador,
        identificadorEquipoDos=equipo2.identificador,
        golesEquipoUno=0, golesEquipoDos=0,
        tarjetasAmarillasEquipoUno=0, tarjetasAmarillasEquipoDos=0,
        tarjetasRojasEquipoUno=0, tarjetasRojasEquipoDos=0,
        idPartido=3, puntosEquipoUno=0, puntosEquipoDos=0,
        jornada=1
    )

    partido.simularPartido(15)
    partido.mostrarPartido()



# ---- Pantalla de configuración ----
def pantalla_configuracion(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

    data = get_torneos()
    print(data)

    def volver_al_menu():
        menu_principal(ventana)

    def validar_fecha(dia, mes, anio):
        try:
            datetime.date(int(anio), meses.index(mes) + 1, int(dia))
            return True
        except ValueError:
            return False

    def guardar_torneo():
        #Se obtienen los datos de los inputs
        dia_i, mes_i, anio_i = e_dia_inicio.get(), var_mes_inicio.get(), var_anio_inicio.get()
        dia_f, mes_f, anio_f = e_dia_fin.get(), var_mes_fin.get(), var_anio_fin.get()
        nombre=lnombre.get()
        sede=lsede.get()
        
        #Validaciones
        if not nombre:
            messagebox.showerror("Error", "Debes agregar el nombre del Torneo")
            return
        
        if not sede:
            messagebox.showerror("Error", "Debes agregar la sede del Torneo")
            return
        
        if not validar_fecha(dia_i, mes_i, anio_i):
            messagebox.showerror("Error", "La fecha de inicio no es válida.")
            return
        
        if not validar_fecha(dia_f, mes_f, anio_f):
            messagebox.showerror("Error", "La fecha de cierre no es válida.")
            return

        fecha_inicio = f"{anio_i}-{meses.index(mes_i)+1:02d}-{int(dia_i):02d}"
        fecha_fin = f"{anio_f}-{meses.index(mes_f)+1:02d}-{int(dia_f):02d}"
        
        if fecha_fin<=fecha_inicio:
            messagebox.showerror("Error", "La fecha de cierre no puede ser menor/igual a la de inicio")
            return
        
        #Si pasa todas las validaciones, guarda los datos
        print("Datos aceptados para torneo: ", fecha_inicio, fecha_fin,nombre,sede)
        data=Torneo(nombre,sede,fecha_inicio,fecha_fin)
        data.guardar()
        messagebox.showinfo("Éxito", "Torneo registrado correctamente")

    tk.Label(
        ventana, text="Configuración del Torneo",
        font=("Segoe UI",16)
    ).pack(pady=20)

    # --- Contenido principal ---
    if len(data) == 0:
        frame_inputs = tk.Frame(ventana)
        frame_inputs.pack(pady=10)

        # --- Nombre ---
        tk.Label(frame_inputs, text="Nombre:",font=("Segoe UI",12)).grid(row=0, column=0, sticky="w",pady=5,padx=(0,3))
        lnombre = tk.Entry(frame_inputs,width=25,font=("Segoe UI",12))
        lnombre.grid(row=0, column=1,sticky="w")

        # --- Sede ---
        tk.Label(frame_inputs, text="Sede:",font=("Segoe UI",12)).grid(row=1, column=0,sticky="w", pady=5)
        lsede = tk.Entry(frame_inputs,width=20,font=("Segoe UI",12))
        lsede.grid(row=1, column=1, sticky="w")

        # --- Fechas ---
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        anios = [str(i) for i in range(2025, 2031)]

        # --- Fecha de inicio ---
        tk.Label(frame_inputs, text="Fecha de Inicio:",font=("Segoe UI",12)).grid(row=2, column=0, sticky="w", pady=5,padx=(0,3))

        e_dia_inicio = tk.Entry(frame_inputs, width=8,font=("Segoe UI",12))
        e_dia_inicio.grid(row=2, column=1, sticky="w")

        var_mes_inicio = tk.StringVar(value=meses[0])
        op_mes_inicio = tk.OptionMenu(frame_inputs, var_mes_inicio, *meses)
        op_mes_inicio.config(width=12,font=("Segoe UI",12))
        op_mes_inicio.grid(row=2, column=1,sticky="e")
        op_mes_inicio["menu"].config(font=("Segoe UI",12))

        var_anio_inicio = tk.StringVar(value=anios[0])
        op_anio_inicio = tk.OptionMenu(frame_inputs, var_anio_inicio, *anios)
        op_anio_inicio.config(width=5,font=("Segoe UI",12))
        op_anio_inicio.grid(row=2, column=2)
        op_anio_inicio["menu"].config(font=("Segoe UI",12))

        # --- Fecha de cierre ---
        tk.Label(frame_inputs, text="Fecha de Cierre:",font=("Segoe UI",12)).grid(row=3, column=0,sticky="w", pady=5,padx=(0,3))

        e_dia_fin = tk.Entry(frame_inputs, width=8,font=("Segoe UI",12))
        e_dia_fin.grid(row=3, column=1, sticky="w")

        var_mes_fin = tk.StringVar(value=meses[0])
        op_mes_fin = tk.OptionMenu(frame_inputs, var_mes_fin, *meses)
        op_mes_fin.config(width=12,font=("Segoe UI",12))
        op_mes_fin.grid(row=3, column=1,sticky="e")
        op_mes_fin["menu"].config(font=("Segoe UI",12))

        var_anio_fin = tk.StringVar(value=anios[0])
        op_anio_fin = tk.OptionMenu(frame_inputs, var_anio_fin, *anios)
        op_anio_fin.config(width=5,font=("Segoe UI",12))
        op_anio_fin.grid(row=3, column=2)
        op_anio_fin["menu"].config(font=("Segoe UI",12))

        # Botón de guardar
        tk.Button(
            ventana, text="Guardar torneo",
            font=("Arial", 12), bg="#4CAF50", fg="white",
            command=guardar_torneo
        ).pack(pady=4)

    else:
        torneo = data[0]
        tk.Label(
            ventana, text=torneo[1],
            font=("Arial", 12, "bold")
        ).pack(pady=4)
        tk.Label(
            ventana, text="Sede: " + torneo[2],
            font=("Arial", 10, "bold")
        ).pack(pady=4)
        tk.Label(
            ventana, text="Fecha de Inicio: " + torneo[3],
            font=("Arial", 10, "bold")
        ).pack(pady=4)
        tk.Label(
            ventana, text="Fecha de Cierre: " + torneo[4],
            font=("Arial", 10, "bold")
        ).pack(pady=4)

    # --- Botón de volver ---
    tk.Button(
        ventana, text="Volver al menú principal",
        font=("Arial", 12), bg="#2196F3", fg="white",
        command=volver_al_menu
    ).pack(pady=4)
    
    
# ---- Menú principal ----
def menu_principal(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

    tk.Label(
        ventana, text="Gestión de Torneo de Fútbol",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    def abrir_configuracion():
        pantalla_configuracion(ventana)

    tk.Button(
        ventana, text="Configuración del torneo",
        font=("Arial", 12), bg="#4CAF50", fg="white",
        command=abrir_configuracion
    ).pack(pady=10)

    tk.Button(
        ventana, text="Registro de Resultados",
        font=("Arial", 12), bg="#4CAF50", fg="white",
        state="disabled"
    ).pack(pady=10)

    tk.Button(
        ventana, text="Informes",
        font=("Arial", 12), bg="#4CAF50", fg="white",
        state="disabled"
    ).pack(pady=10)

    tk.Button(
        ventana, text="Crear Torneo y Simular Partido",
        font=("Arial", 12), bg="#4CAF50", fg="white",
        command=crear_datos
    ).pack(pady=10)

    tk.Button(
        ventana, text="Salir",
        font=("Arial", 12), bg="#f44336", fg="white",
        command=ventana.destroy
    ).pack(pady=10)


# ---- MAIN ----
def main():
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión de Torneo de Fútbol")
    ventana.geometry("800x350")
    menu_principal(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
