import os

def contar_visitas():
    archivo_contador = 'contador_visitas.txt'

    if os.path.exists(archivo_contador):
        with open(archivo_contador, 'r') as file:
            visitas = int(file.read())
    else:
        visitas = 0

    visitas += 1

    with open(archivo_contador, 'w') as file:
        file.write(str(visitas))

    return visitas