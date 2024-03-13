import tkinter as tk
import random
import time


class Buscaminas:
    def __init__(self, ventana, rows, cols, nbombas, banderas):
        self.ventana = ventana
        self.rows = rows
        self.cols = cols
        self.banderas = banderas
        self.nbombas = nbombas
        self.buttons = {}
        self.bombas = set()
        self.widgets()
        self.random_bombas()
        self.contador()
    
    def widgets(self):
        self.contador()
        
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.ventana, text='', width=5, height=2, bg="pale green")
                button.grid(row=row, column=col)
                #button.config(command=lambda r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-1>', lambda event, r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.marcar_bomba(r, c))
                self.buttons[(row, col)] = button
                
    
    
    def random_bombas(self):
        bombas = random.sample(list(self.buttons.keys()), self.nbombas)
        for bomba in bombas:
            self.bombas.add(bomba)
        
    def verificar_bomba(self, row, col):
        if self.buttons[(row, col)]['text'] == 'B':
            return "break"
        elif (row, col) in self.bombas:
            for position, button in self.buttons.items():
                if position in self.bombas:
                    button.config(text='*', bg="tomato")
        else:
            self.buttons[(row, col)].config(text='', bg="bisque")

    def marcar_bomba(self, row, col):
        if self.buttons[(row, col)]['bg'] == "bisque":
            return "break"
        elif self.buttons[(row, col)]['text'] == 'B':
            self.buttons[(row, col)]['text'] = ''
            self.banderas = self.banderas + 1
            self.actualizar_banderas()
        elif self.banderas < 1:
            return "break"
        elif self.buttons[(row, col)]['text'] == '':
            self.buttons[(row, col)]['text'] = 'B'
            self.banderas = self.banderas - 1
            self.actualizar_banderas()
        
        return "break"
    
       
    def contador(self):
        self.s = 0
        self.m = 0
        self.label_tiempo = tk.Label(self.ventana, text='', width=10, height=2, bg="white", fg="black")
        self.label_tiempo.grid(row=self.rows, columnspan=self.cols)
        self.label_banderas = tk.Label(self.ventana, text='', width=5, height=2, bg="white", fg="black")
        self.label_banderas.grid(row=self.rows, column=self.cols - 1)
        
        self.actualizar_banderas()
        self.actualizar_tiempo()
        
        
    def actualizar_banderas(self):
        self.label_banderas.config(text=self.banderas)
    
    
    def actualizar_tiempo(self):
        
        self.s += 1
        
        if self.s == 60:
            self.s = 0
            self.m += 1
        
        tiempo = f"Tiempo: {self.m:02d}:{self.s:02d}"    
        self.label_tiempo.config(text=tiempo)
        
        self.ventana.after(1000, self.actualizar_tiempo)

    

def main():
    root = tk.Tk()
    root.title("Tablero de Buscaminas")
    def configurar_eleccion(opcion):
        #global eleccion
        eleccion = opcion
        verificar_nivel(eleccion)
    def verificar_nivel(eleccion):
        if eleccion == "facil":
            row = 5
            col = 5
            nbombas = 5
            banderas = 5 
        elif eleccion == "medio":
            row = 10
            col = 10
            nbombas = 99
            banderas = 10         
        elif eleccion == "dificil":
            row = 15
            col = 15
            nbombas = 224
            banderas = 10
        else:
            print("Modo de juego no encontrado")
        Buscaminas(root, row, col, nbombas, banderas)


    boton_facil = tk.Button(root, text="Fácil", command=lambda: configurar_eleccion("facil"))
    boton_facil.config(cursor="pirate", bg="grey", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_facil.place(x="0", y="0")

    boton_mediano = tk.Button(root, text="Medio", command=lambda: configurar_eleccion("medio"))
    boton_mediano.config(cursor="hand2", bg="grey", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_mediano.place(x="0", y="40")

    boton_dificil = tk.Button(root, text="Dificil", command=lambda: configurar_eleccion("dificil"))
    boton_dificil.config(cursor="hand2", bg="grey", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_dificil.place(x="0", y="80")
    
    
    root.mainloop()

if __name__ == "__main__":
    main()
