import tkinter as tk
import random

class Buscaminas:
    def __init__(self, ventana, rows, cols, nbombas):
        self.ventana = ventana
        self.rows = rows
        self.cols = cols
        self.nbombas = nbombas
        self.buttons = {}
        self.bombas = set()
        self.widgets()
        self.random_bombas()

    def widgets(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.ventana, text='', width=2, height=1)
                button.grid(row=row, column=col)
                #button.config(command=lambda r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-1>', lambda event, r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.marcar_bomba(event, r, c))
                self.buttons[(row, col)] = button
                
    
    
    def random_bombas(self):
        bombas = random.sample(list(self.buttons.keys()), self.nbombas)
        for bomba in bombas:
            self.bombas.add(bomba)
        print(self.buttons)
        print(bomba)
        print(self.bombas)
        
    def verificar_bomba(self, row, col):
        if (row, col) in self.bombas:
            for position, button in self.buttons.items():
                if position in self.bombas:
                    button.config(text='*', bg="red")
        else:
            self.buttons[(row, col)].config(text='', bg="white")

    def marcar_bomba(self, event, row, col):
        if self.buttons[(row, col)]['text'] == '':
            self.buttons[(row, col)]['text'] = 'B'
        elif self.buttons[(row, col)]['text'] == 'B':
            self.buttons[(row, col)]['text'] = ''
        return "break"



def main():
    root = tk.Tk()
    root.title("Tablero de Buscaminas")
    estado = True
    def configurar_eleccion(opcion):
        #global eleccion
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
            nbombas = 99         
        elif eleccion == "dificil":
            row = 15
            col = 15
            nbombas = 224
        else:
            print("Modo de juego no encontrado")
        Buscaminas(root, row, col, nbombas)


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
