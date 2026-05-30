import struct
import os
"""

SEMANA 12 problema nuemro 5
gestion de turnos medicos
archivo binario de longitud fija
mantiene indices de memoria mediante diccionarios
reportes ORDENADOS
resuelve busquedas eficientes por distintos criterios
asigan turnos a una agenda diaria mediante backtracking
se diuvide en 4modulos
en este caso desarrollaremos el modulo 3 REPORTES ORDENAODS
"""

"""
Necesitamos implementar  la funcion listar_pacientes_ordenados (archivo donde estan los registros, criterio de ordenamiento)
donde los criterios son los siguientes:
Apellido "alfabetico"
Prioridad de 1 a 3 y dentro de 1,2,3 apellido alfabetico
utilizando merge_sort
"""

# AGREGAMOS CONSTANTES
FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)
NOMBRE_ARCHIVO = "pacientes_test.dat"
# ===================================
#           FUNCIONES
# ===================================


def leer_registro(ruta):
    """
    leemos todos los registros y los agregamos a una lista.
    Precondición: 0 <= k < cantidad de registros.
    Postcondición: devuelve (activo, siguiente, id, nombre, telefono, email).
    """
    lista_datos = []
    tamano_total = os.path.getsize(ruta)
    cantidad_registros = tamano_total // TAM_REGISTRO
    with open(ruta, "rb") as f:
        for i in range(cantidad_registros):
            leido = f.read(TAM_REGISTRO)
            dni, apellido_conceros, nombre_conceros, telefono_conceros, prioridad= struct.unpack(FORMATO, leido)
            apellido = apellido_conceros.rstrip(b'\x00').decode('utf-8')
            nombre = nombre_conceros.rstrip(b'\x00').decode('utf-8')
            telefono = telefono_conceros.rstrip(b'\x00').decode('utf-8')
            lista_datos.append((dni,apellido,nombre,telefono, prioridad))
    return lista_datos

def merge_sort(lista, columna):
    """
    Ordena una secuencia comparándola por divide y vencerás.

    Precondición: secuencia es una lista de elementos comparables entre sí.
                  La ruta tiene formato <i30s24s16sB y donde entra
                  Dni apellido nombre telefono prioridad
    Postcondición: devuelve una nueva lista con los mismos elementos en
                   orden no decreciente; secuencia no se modifica.
    Complejidad: O(n log n) en tiempo, O(n) en espacio auxiliar.
    """
    # --- Prólogo: caso base de la recursión -------------------------
    if len(lista) <= 1:
        return lista[:]          # copia defensiva

    # --- Resolución: dividir, recurrir, combinar --------------------
    medio = len(lista) >> 1            # división por 2 a nivel ALU
    mitad_izq = merge_sort(lista[:medio],columna)
    mitad_der = merge_sort(lista[medio:],columna)
    resultado = _fusionar(mitad_izq, mitad_der,columna)

    # --- Epílogo: devolver la solución del problema -----------------
    return resultado


def _fusionar(izq, der,columna):
    """Fusiona dos listas ordenadas en una sola lista ordenada.

    Precondición: izq y der están ordenadas en forma no decreciente.
    Postcondición: devuelve una nueva lista con todos los elementos
                   de izq y der, en orden no decreciente y estable.
    """
    # --- Prólogo: estructuras de trabajo ----------------------------
    resultado = []
    i, j = 0, 0
    n_izq, n_der = len(izq), len(der)

    # --- Resolución: avanzar ambos punteros tomando el menor --------
    while i < n_izq and j < n_der:    # mientras haya ambos
        if izq[i][columna] <= der[j][columna]:          # ≤ preserva estabilidad
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])         # cola de la izquierda
    resultado.extend(der[j:])         # cola de la derecha

    # --- Epílogo: devolver lista fusionada --------------------------
    return resultado

def listar_pacientes_ordenados(ruta, criterio):
    """
    Toma un bytearray de pacientes y devuelve una lista ordenada de pacientes segun el criterio
    pre-condicion: criterio solo puede ser apellido o prioridad
    post-condicion: si criterio no es ni apellido ni prioridad, devuelve prioridad
        una lista de
    """
    lista = leer_registro(ruta)
    lista_apellido = merge_sort(lista,1)
    if criterio == "apellido":
        return lista_apellido
    else:
        return merge_sort(lista_apellido,4)

if __name__ == "__main__":
    #=========================================
    # PRUEBA MOMENTANEA CON DATOS HARCODEADOS
    #=========================================
    respuesta_apellido = listar_pacientes_ordenados (NOMBRE_ARCHIVO, "apellido")
    respuesta_prioridad =listar_pacientes_ordenados(NOMBRE_ARCHIVO, "prioridad")
    
    print("=== Ordenado por apellido ===")
    for dni, apellido, nombre, telefono, prioridad in respuesta_apellido:
        print(f" {apellido}, {nombre}  | DNI: {dni} | Tel: {telefono} | Prioridad: {prioridad}")

    print()
    print("=== Ordenado por prioridad ===")
    for dni, apellido, nombre, telefono, prioridad in respuesta_prioridad:
        print(f"  Prioridad {prioridad} | {apellido}, {nombre} | DNI: {dni} | Tel: {telefono} ")

"""Que el merge sort sea estable es una funcionalidad que en este ejercicio es de suma importancia, debido al uso de dos pasadas para realizar el ordenamiento mediante el criterio prioridad.
Primero realizamos una pasada OBLIGATORIA donde ordenamos la lista mediante apellido, entonces cuando ordenemos por prioridad, en caso q este mismo sea igual al que este analizando
se va respetar el orden de la lista anterior, es decir el que ya estaba ordenada."""