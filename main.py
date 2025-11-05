import tkinter as tk
from views.menu_principal import menu_principal

# --- MAIN ---
def main():
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión de Torneo de Fútbol")
    ventana.geometry("650x350")

    # Primer arranque: menú principal
    menu_principal(ventana)

    ventana.mainloop()


if __name__ == "__main__":
    main()
