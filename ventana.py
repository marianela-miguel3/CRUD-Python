from tkinter import *
from tkinter import messagebox
import sqlite3 as sq3
from asyncio.windows_events import NULL



def conectar():
    global con
    global cur
    con= sq3.connect("mi_basededatos")
    cur= con.cursor()
    messagebox.showinfo("STATUS","Conectando a la base de datos")


#SQL para crear la tabla escuela
instruct1= '''CREATE TABLE IF NOT EXISTS escuelas (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,  
    nombre varchar(45) DEFAULT NULL,
    localidad varchar(45) DEFAULT NULL,
    provincia varchar(45) DEFAULT NULL,
    capacidad INTEGER DEFAULT NULL)'''
    
    #SQL para crear la tabla alumnos 
instruct2= '''CREATE TABLE  IF NOT EXISTS alumnos (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_escuela INTEGER DEFAULT NULL,
    legajo INTEGER DEFAULT NULL,
    nombre varchar(45) DEFAULT NULL,
    nota decimal(10,0) DEFAULT NULL,
    grado INTEGER DEFAULT NULL,
    email varchar(45) NOT NULL,
    FOREIGN KEY (id_escuela) REFERENCES escuelas(id))'''
    
cur.execute(instruct1)#ejecutara la creacion de escuelas
cur.execute(instruct2)#ejecutara la creacion de alumnos

#DATOS PARA LAS TABLAS
lista1=[(1,'Normal 1','Quilmes','Buenos Aires',250),(2,'Gral. San Martín','San Salvador','Jujuy',100),(3,'Belgrano','Belgrano','Córdoba',150),(4,'EET Nro 2','Avellaneda','Buenos Aires',500),(5,'Esc. N° 2 Tomás Santa coloma','Capital Federal','Buenos Aires',250)]
lista2=[(1,2,1000,'Ramón Mesa',8,1,'rmesa@mail.com'),(2,2,1002,'Tomás Smith',8,1,''),(4,1,101,'Juan Perez',10,3,''),(5,1,105,'Pedro González',9,3,''),(6,5,190,'Roberto Luis Sánchez',8,3,'robertoluissanchez@gmail.com'),(7,2,106,'Martín Bossio',NULL,3,''),(8,4,100,'Paula Remmi',3,1,'mail@mail.com'),(9,4,1234,'Pedro Gómez',6,2,'')]

    #Estructura de control, que nos evitara errores
try:
        #Por ejemplo esta se va a ejecutar 5 veces, una por cada escuela
        cur.executemany("INSERT INTO escuelas VALUES (?,?,?,?,?)",lista1)
        #Por ejemplo esta se va a ejecutar 9 veces, una por cada alumno
        cur.executemany("INSERT INTO alumnos VALUES (?,?,?,?,?,?,?)",lista2)
except:
        print("Posiblemente estos valores ya existen en la Base de Datos")
    
con.commit()#se encarga de que los cambios en la base de datos se guarden



def salir():
    respuesta=messagebox.askquestion("CONFIRMACION","Esta seguro que desea salir?")
    if respuesta=="yes":
        try:#intenta lo siguiente
            con.close()
        except:#si falla lo anterior hace lo siguiente
            pass
        raiz.destroy()

def limpiar():
    legajo.set("")
    alumnos.set("")
    email.set("")
    calificacion.set("")
    escuela.set("")
    localidad.set("")
    provincia.set("")
    legajo_input.config(state="normal")

def licencia():
    mensaje='''
    GNU GENERAL PUBLIC LICENSE
                CRUD PYTHON Version 1, November 2022
                Copyright (C) 2022 Codo a Codo 4.0 , Inc.
                Everyone is permitted to copy and distribute verbatim copies
                of this license document, but changing it is not allowed.
    '''
    messagebox.showinfo("LICENCIA",mensaje)

def sobre_app():
    messagebox.showinfo("ACERCA DE","Creado por la comision 22622 \n para Codo a Codo 4.0 - Big Data \n 2022")

def leer():
     query='''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia
        FROM alumnos INNER JOIN escuelas 
        ON alumnos.id_escuela = escuelas._id 
        WHERE alumnos.legajo='''

     cur.execute(query+legajo.get())
     resultado=cur.fetchall()
     if resultado==[]:
        messagebox.showerror("ERROR","este lagajo no existe")
     else:
        legajo.set(resultado[0][0])
        alumnos.set(resultado[0][1])
        calificacion.set(resultado[0][2])
        email.set(resultado[0][3])
        escuela.set(resultado[0][4])
        localidad.set(resultado[0][5])
        provincia.set(resultado[0][6])
        legajo_input.config(state="disabled")

def buscar_escuelas(intencion):
    conectar()
    con=sq3.connect("mi_db")
    cur=con.cursor()
    if intencion:
        cur.execute("SELECT _id, localidad, provincia FROM escuelas where nombre=?", (escuela.get(),))
    else:
        cur.execute("SELECT nombre FROM escuelas")
    resultado= cur.fetchall()
    escuelas=[]
    for escuela in resultado:
        if intencion:
             provincia.set(escuela[2])
             localidad.set(escuela[1])
        escuelas.append(escuela[0])
    con.close()
    return escuelas

def localizar_escuelas(event):
    conectar()
    con=sq3.connect("mi_db")
    cur=con.cursor()
    cur.execute("SELECT localidad, provincia FROM escuelas where nombre=?", (escuela.get(),))
    resultado=cur.fetchall()
    provincia.set(resultado[0][1])
    localidad.set(resultado[0][0])


def crear():
    id_escuela=buscar_escuelas(True)
    id_escuela=int(id_escuela[0])
    datos=id_escuela, legajo.get(), alumnos.get(), calificacion.get(), email.get()
    cur.execute("INSERT INTO alumnos(id_escuela, legajo, nombre, nota, email) values(?,?,?,?,?)", datos)
    con.commit()
    messagebox.showinfo("STATUS", "Registro agregado")
    limpiar()

def eliminar():
    respuesta=messagebox.askquestion("CONFIRMACION","estas seguro que quiere eliminar este registro?")
    if respuesta=="yes":
      nro_legajo=legajo.get()
      cur.execute("DELETE FROM alumnos where legajo="+nro_legajo)
      con.commit()
      limpiar()

# def listado():
#      query='''SELECT alumnos.legajo, alumnos.nombre, escuelas.localidad, escuelas.provincia
#         FROM alumnos INNER JOIN escuelas 
#         ON alumnos.id_escuela = escuelas._id 
#         WHERE alumnos.legajo='''
#      cur.execute(query+legajo.get())
#      resultado=cur.fetchall()
#      texto=""
#      for valor in resultado:
#         texto+=str(valor)
#         texto+="\n"
#         messagebox.showinfo("ALUMNOS",texto)

def actualizar():
    id_escuela=int(buscar_escuelas(TRUE)[0])#consegumos el id, solo queremos el primer parametro
    datos=id_escuela, alumnos.get(), calificacion.get(), email.get()
    cur.execute("UPDATE alumnos SET id_escuela=?, nombre=?, nota=?, email=?", datos)
    con.commit()
    messagebox.showinfo("STATUS", "Registro modificado correctamente")
    limpiar()


raiz= Tk()
raiz.title('Python CRUD - Comision 22622')
barramenu = Menu(raiz)
raiz.config(menu = barramenu)

bbddmenu= Menu (barramenu , tearoff = 0)
bbddmenu.add_command(label="Conectar", command=conectar)
bbddmenu.add_command(label="Listado de alumnos")
bbddmenu.add_command(label="Salir", command=salir)
barramenu.add_cascade(label="BBDD", menu=bbddmenu)

limpiarmenu= Menu(barramenu, tearoff=0)
limpiarmenu.add_command(label="Limpiar campos", command=limpiar)
barramenu.add_cascade(label="Limpiar", menu=limpiarmenu)

acercademenu = Menu(barramenu, tearoff=0)
acercademenu.add_command(label="Licencia", command=licencia)
acercademenu.add_command(label="Sobre la app", command=sobre_app)
barramenu.add_cascade(label="Acerca de", menu=acercademenu)

framecampos = Frame(raiz)
framecampos.pack()

legajo=StringVar()
alumnos=StringVar()
email=StringVar()
escuela=StringVar()
calificacion=DoubleVar()
localidad=StringVar()
provincia=StringVar()


legajo_input=Entry(framecampos,textvariable=legajo)
legajo_input.grid(row=0, column=1, padx=10, pady=10)

alumnos_input=Entry(framecampos,textvariable=alumnos)
alumnos_input.grid(row=1, column=1, padx=10, pady=10)

email_input=Entry(framecampos,textvariable=email)
email_input.grid(row=2, column=1, padx=10, pady=10)

calificacion_input=Entry(framecampos,textvariable=calificacion)
calificacion_input.grid(row=3, column=1, padx=10, pady=10)

escuela_input=OptionMenu(framecampos, escuela, *schools , command=localizar_escuelas)
escuela_input.grid(row=4, column=1, padx=10, pady=10)

localidad_input=Entry(framecampos,textvariable=localidad)
localidad_input.grid(row=5, column=1, padx=10, pady=10)

provincia_input=Entry(framecampos,textvariable=provincia)
provincia_input.grid(row=6, column=1, padx=10, pady=10)
'''IntVar, BooleanVar'''

legajolabel=Label(framecampos, text="legajo")
legajolabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

alumnoslabel=Label(framecampos, text="Alumnos")
alumnoslabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")

emaillabel=Label(framecampos, text="Email")
emaillabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")

calificacionlabel=Label(framecampos, text="Calificacion")
calificacionlabel.grid(row=3, column=0, padx=10, pady=10, sticky="w")

escuelalabel=Label(framecampos, text="Escuela")
escuelalabel.grid(row=4, column=0, padx=10, pady=10, sticky="w")

localidadlabel=Label(framecampos, text="Localidad")
localidadlabel.grid(row=5, column=0, padx=10, pady=10, sticky="w")

provincialabel=Label(framecampos, text="Provincia")
provincialabel.grid(row=6, column=0, padx=10, pady=10, sticky="w")

framebotones=Frame(raiz)
framebotones.pack()

boton_crear=Button(framebotones, text="Crear", command=crear)
boton_crear.grid(row=0, column=0, pady=10)

boton_leer=Button(framebotones, text="Leer", command=leer)
boton_leer.grid(row=0, column=1, pady=10)

boton_actualizar=Button(framebotones, text="Actualizar", command=actualizar)
boton_actualizar.grid(row=0, column=2, pady=10)

boton_borrar=Button(framebotones, text="Borrar", command=eliminar)
boton_borrar.config(bg="pink", fg="white")
boton_borrar.grid(row=0, column=3, pady=10)

framecopy=Frame(raiz)
framecopy.pack()

copylabel=Label(framecopy, text="2022 Copyright C22622")
copylabel.grid(row=0, column=0,)

raiz.mainloop()