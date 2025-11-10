import tkinter as tk
from views.menu_principal import menu_principal
from controllers.pool import crear_tablas,crear_partidos_fase_grupos,crear_partidos_fase_final
from controllers.equipos import get_equipo
from controllers.partido import get_partidos


# MAIN
def main():
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión Torneo")
    ventana.state('zoomed')
    
    # Primer arranque: menú principal
    menu_principal(ventana)
    crear_tablas()
    ventana.mainloop()
 

if __name__ == "__main__":
    main()
