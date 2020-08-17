"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista.
"""

import config as cf
import sys
import csv
from time import process_time 

def loadCSVFile (file, lst, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file 
            Archivo de texto del cual se cargaran los datos requeridos.
        lst :: []
            Lista a la cual quedaran cargados los elementos despues de la lectura del archivo.
        sep :: str
            Separador escodigo para diferenciar a los distintos elementos dentro del archivo.
    Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None   
    """
    del lst[:]
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lst.append(row)
    except:
        del lst[:]
        print("Se presento un error en la carga del archivo")
    
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Contar los elementos de la Lista")
    print("3- Contar elementos filtrados por palabra clave")
    print("4- Consultar elementos a partir de dos listas")
    print("0- Salir")

def countElementsFilteredByColumn(criteria, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        retdict :: dict
            counter: la cantidad de veces que aparece un elemento con el criterio definido
            ids: los id de dichas apariciones
    """
    ids = []
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        for element in lst:
            
            if criteria.lower() in element[column].lower(): #filtrar por palabra clave 
                counter+=1
                ident = ([element][0]).get("id")
                ids.append(ident)
        t1_stop = process_time() #tiempo final

        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        retdict = {"counter" : counter, "ids": ids}
    return retdict

def countElementsByCriteria(criteria, column, lst):
    infomovie = []
    mov = input("Ingrese la ubicación del archivo donde estan los metadatos de la película, \n por ejemplo: Data/themoviesdb/SmallMoviesDetailsCleaned.csv: ")
    loadCSVFile(mov, infomovie)
    
    goodcnt = 0
    cnt = 0

    counter=countElementsFilteredByColumn(criteria, column, lst) #filtrar una columna por criterio  
    for element in infomovie:
        if ([element][0]).get("id") in counter.get("ids"):
            if float(([element][0]).get("vote_average")) >= 6.0:
                goodcnt += 1
            cnt += float(([element][0]).get("vote_average"))
    
    avg = cnt/int(counter.get("counter"))
    retdict = {"average":avg, "goodfilm": goodcnt,}
    
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    return retdict


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lista = [] #instanciar una lista vacia
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                files= input("Ingrese el nombre y ubicación del archivo con el casting de la película, por defecto, Data/themoviesdb/MoviesCastingRaw-small.csv: \n")

                loadCSVFile(files, lista) #llamar funcion cargar datos
                print("Datos cargados, "+str(len(lista))+" elementos cargados")
            elif int(inputs[0])==2: #opcion 2
                if len(lista)==0: #obtener la longitud de la lista
                    print("La lista esta vacía")    
                else: print("La lista tiene "+str(len(lista))+" elementos")
            elif int(inputs[0])==3: #opcion 3
                criteria =input('Ingrese el criterio de búsqueda\n')
                tipo_dato =input("Ingrese en que categoría quiere buscar, por ejemplo: director_name: \n")
                counter=countElementsFilteredByColumn(criteria, tipo_dato, lista) #filtrar una columna por criterio  
                print("Coinciden ",counter.get("counter")," elementos con el crtierio: ", criteria  )
                print (counter.get("ids"))
            elif int(inputs[0])==4: #opcion 4
                criteria =input('Ingrese el criterio de búsqueda\n')
                tipo_dato =input("Ingrese en que categoría quiere buscar, por ejemplo: director_name: \n")
                counter=countElementsByCriteria(criteria,tipo_dato,lista)
                print("Coinciden ",counter.get("goodfilm")," elementos de 6.0 o más de calificación con el crtierio: '", criteria ,",con una calificación promedio de ", counter.get("average"))
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)

if __name__ == "__main__":
    main()
