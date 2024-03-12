# read me buscaminas

PROYECTO BUSCAMINAS - David Valverde | Miquel Burguera

**Tareas**: 
  1. [**TERMINADA**]. Arreglar funcionamiento de la funcion [*verificar_bomba*]:
     - Que al tocar una mina todas se muestren todas.
     - Investigar como seleccionar todos lo valores de un diccionario -> "*self.buttons = {}*" 

  2. Investigar sobre como ha de ser la expansion del tablero a la hora de haber seleccionado una casilla y que no haya bomba. << En la misma funcion *verificar_bomba*, apartado '*else*'.
  3. Investigar para funcion de conteo de bombas cercanas a la casilla pulsada. << En la misma funcion *verificar_bomba*, apartado '*else*'.
  4. Al pulsar un NO bomba que no te deje interactuar y se bloquee la casilla (poner bombas) así como en las casillas donde pongas bandera no te deje hacer click (booleano??)
  5. Arreglar contador (suma de 2 en 2).
  6. currarse interfaz
------------

**Parte**:
  1. En la funcion [*verificar_bomba*] -> los tipos booleanos no disponen de atributo .config (revisar)
  2. Función *verificar_bomba* arreglada y añadida al documento principal.
