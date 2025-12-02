import json
import uuid
import redis
from dotenv import load_dotenv
import os

load_dotenv()

r = redis.Redis(
    host=os.getenv("KEYDB_HOST"),
    port=int(os.getenv("KEYDB_PORT")),
    password=os.getenv("KEYDB_PASSWORD"),
    decode_responses=True
)

def agregar_libro():
    data = {}
    data["id"] = str(uuid.uuid4())
    data["titulo"] = input("Título: ")
    data["autor"] = input("Autor: ")
    data["genero"] = input("Género: ")
    data["estado"] = input("Estado de lectura: ")
    r.set(f"libro:{data['id']}", json.dumps(data))
    print("Libro agregado.")

def actualizar_libro():
    libro_id = input("ID del libro a actualizar: ")
    key = f"libro:{libro_id}"
    libro_raw = r.get(key)
    if not libro_raw:
        print("Libro no encontrado.")
        return
    libro = json.loads(libro_raw)
    for campo in ["titulo", "autor", "genero", "estado"]:
        nuevo = input(f"{campo} ({libro[campo]}): ")
        if nuevo.strip():
            libro[campo] = nuevo
    r.set(key, json.dumps(libro))
    print("Libro actualizado.")

def eliminar_libro():
    libro_id = input("ID del libro a eliminar: ")
    if r.delete(f"libro:{libro_id}"):
        print("Libro eliminado.")
    else:
        print("Libro no encontrado.")

def ver_libros():
    for key in r.scan_iter("libro:*"):
        print(r.get(key))

def buscar_libros():
    termino = input("Buscar por título, autor o género: ").lower()
    for key in r.scan_iter("libro:*"):
        libro = json.loads(r.get(key))
        if termino in libro["titulo"].lower() or termino in libro["autor"].lower() or termino in libro["genero"].lower():
            print(libro)

def menu():
    while True:
        print("""
1. Agregar libro
2. Actualizar libro
3. Eliminar libro
4. Ver libros
5. Buscar libros
6. Salir
""")
        op = input("> ")
        if op == "1": agregar_libro()
        elif op == "2": actualizar_libro()
        elif op == "3": eliminar_libro()
        elif op == "4": ver_libros()
        elif op == "5": buscar_libros()
        elif op == "6": break

if __name__ == "__main__":
    menu()
