import time
from fastapi import FastAPI, HTTPException
import db

app = FastAPI()

@app.get("/")
def read_root():
    return {"servidor intermediario entre sql y csv de pokemon"}

@app.get("/pokemon/csv/{clave}")
def pokemon_csv(clave):
    inicio = time.perf_counter()
    origen = "csv"
    poke = db.busca_en_csv(clave)

    if poke is None:
       origen = "PokeAPI"
       poke = db.agregar_en_csv(clave)
    if poke is None:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")

    fin = time.perf_counter()
    tiempo = round((fin - inicio) * 1000, 2)
    return {"origen": origen, "pokemon": poke, "tiempo": tiempo}


@app.get("/pokemon/db/{clave}")
def pokemon_db(clave: str):
    inicio = time.perf_counter()
    origen = "SQLlite"
    poke = db.busca_en_db(clave)

    if poke is None:
       origen = "PokeAPI"
       poke = db.agregar_en_db(clave)
    if poke is None:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")

    fin = time.perf_counter()
    tiempo = round((fin - inicio) * 1000, 2)
    return {"origen": origen, "pokemon": poke, "tiempo": tiempo}