import sqlite3
import csv
import requests

def consultar_api(url):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()             
    except requests.exceptions.RequestException as e:
        print("Error al consultar la API:", e)
        return None 


def agregar_en_csv(clave):
    clave = str(clave).lower().strip()
    url = f"https://pokeapi.co/api/v2/pokemon/{clave}"
    datos = consultar_api(url)
    stats_dict = {} 

    if datos is None:
        return None
    
    for d in datos["stats"]:
        nombre_stat = d["stat"]["name"] 
        stats_dict[nombre_stat] = d["base_stat"]
    archivo_existe = True 
    try: 
        with open("pokemones.csv", "r", encoding="utf-8") as f: 
            pass 
    except FileNotFoundError: 
        archivo_existe = False
    if archivo_existe is False:
        with open("pokemones.csv", "w", newline="", encoding="utf-8") as f:
            campos = ["id", "nombre", "tipo","altura", "peso", "experiencia_base" , "hp", "ataque", "defensa", "velocidad"]
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
    
    if datos is not None:
        agregado = ({"id": datos["id"], "nombre": datos["name"], "tipo": datos["types"][0]["type"]["name"], "altura": datos["height"], "peso": datos["weight"], "experiencia_base": datos["base_experience"], "hp": stats_dict.get("hp", 0), "ataque": stats_dict.get("attack", 0), "defensa": stats_dict.get("defense", 0), "velocidad": stats_dict.get("speed", 0)}) 
        with open("pokemones.csv", "a", newline="") as f:
            campos = ["id", "nombre", "tipo","altura", "peso", "experiencia_base" , "hp", "ataque", "defensa", "velocidad"]
            escritor = csv.DictWriter(f, fieldnames=campos)                
            escritor.writerow(agregado)
    return agregado

def busca_en_csv(clave):
    clave = str(clave).lower().strip()
    
    try:
        with open("pokemones.csv", "r") as f:
            lector = csv.DictReader(f)
            for datos in lector:
                if  clave == datos["nombre"].lower() or clave == datos["id"]:
                    print("se encontró el pokemon")
                    return ({"id": int(datos["id"]),
                             "nombre": datos["nombre"],
                             "tipo": datos["tipo"],
                             "altura": int(datos["altura"]),
                             "peso": int(datos["peso"]),
                             "experiencia_base": int(datos["experiencia_base"]),
                             "hp": int(datos["hp"]),
                             "ataque": int(datos["ataque"]),
                             "defensa": int(datos["defensa"]),
                             "velocidad": int(datos["velocidad"])
                            })
    except FileNotFoundError:
        return None


def busca_en_db(clave):
    clave = str(clave).lower().strip()
    conn = sqlite3.connect("pokemones.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS pokemones (
      id INTEGER PRIMARY KEY, 
      nombre TEXT NOT NULL, 
      tipo TEXT NOT NULL, 
      altura INTEGER, 
      peso INTEGER, 
      experiencia_base 
      INTEGER, hp INTEGER, 
      ataque INTEGER, 
      defensa INTEGER, 
      velocidad INTEGER) 
      """)
    cursor.execute("SELECT * FROM pokemones WHERE LOWER(nombre) = ? OR CAST(id AS TEXT) = ?", (clave, clave))
    datos = cursor.fetchone()
    conn.close()
    if datos:
        return {
            "id": datos[0],
            "nombre": datos[1],
            "tipo": datos[2],
            "altura": datos[3],
            "peso": datos[4],
            "experiencia_base": datos[5],
            "hp": datos[6],
            "ataque": datos[7],
            "defensa": datos[8],
            "velocidad": datos[9]
            }
    return None

def agregar_en_db(clave):
    clave = str(clave).lower().strip()
    url = f"https://pokeapi.co/api/v2/pokemon/{clave}"
    datos = consultar_api(url)
    stats_dict = {} 
    
    if datos is None:
        return None
        
    for d in datos["stats"]:
        nombre_stat = d["stat"]["name"] 
        stats_dict[nombre_stat] = d["base_stat"]
        
    datos = ({"id": datos["id"], "nombre": datos["name"], "tipo": datos["types"][0]["type"]["name"], "altura": datos["height"], "peso": datos["weight"], "experiencia_base": datos["base_experience"], "hp": stats_dict.get("hp", 0), "ataque": stats_dict.get("attack", 0), "defensa": stats_dict.get("defense", 0), "velocidad": stats_dict.get("speed", 0)}) 

    
    con = sqlite3.connect("pokemones.db")
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS pokemones (
    id INTEGER PRIMARY KEY, 
    nombre TEXT NOT NULL, 
    tipo TEXT NOT NULL, 
    altura INTEGER, 
    peso INTEGER, 
    experiencia_base INTEGER, 
    hp INTEGER, 
    ataque INTEGER, 
    defensa INTEGER, 
    velocidad INTEGER) 
    """)
    cursor.execute("INSERT INTO pokemones VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        datos["id"],
        datos["nombre"],
        datos["tipo"],
        datos["altura"],
        datos["peso"],
        datos["experiencia_base"],
        datos["hp"],
        datos["ataque"],
        datos["defensa"],
        datos["velocidad"]
    ))
    con.commit()
    con.close()
    return datos