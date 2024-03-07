import tkinter as tk
import random

class buscaminas:
    def __init__(self, ventana, rows, cols, nbombas):
        self.ventana = ventana
        self.rows = rows
        self.cols = cols
        self.nbombas = nbombas
        self.buttons = {}
        self.widgets()
        self.random_bombas()
    
    def widgets(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.ventana, text='', width=2, height=1)
                button.grid(row=row, column=col)
                self.buttons[(row, col)] = button

    def random_bombas(self):
        bombas = random.sample(list(self.buttons.keys()), self.nbombas)
        for bomba in bombas:
            self.buttons[bomba].config(text='*', bg="red")





def main():
    root = tk.Tk()
    root.title("Tablero de Buscaminas")
    def configurar_eleccion(opcion):
        global eleccion
        eleccion = opcion
        verificar_nivel(eleccion)
    def verificar_nivel(eleccion):
        if eleccion == "facil":
            row = 5
            col = 5
            nbombas = 5
        elif eleccion == "mediano":
            row = 10
            col = 10
            nbombas = 10           
        elif eleccion == "dificil":
            row = 15
            col = 15
            nbombas = 15
        else:
            print("Modo de juego no encontrado")
        buscaminas(root, row, col, nbombas)


    boton_facil = tk.Button(root, text="Fácil", command=lambda: configurar_eleccion("facil"))
    boton_facil.config(cursor="pirate", bg="grey", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_facil.place(x="0", y="0")

    boton_mediano = tk.Button(root, text="Mediano", command=lambda: configurar_eleccion("mediano"))
    boton_mediano.config(cursor="hand2", bg="grey", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_mediano.place(x="0", y="40")

    boton_dificil = tk.Button(root, text="Dificil", command=lambda: configurar_eleccion("dificil"))
    boton_dificil.config(cursor="hand2", bg="grey", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_dificil.place(x="0", y="80")
    
    
    root.mainloop()

if __name__ == "__main__":
    main()
