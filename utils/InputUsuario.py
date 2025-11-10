from unidecode import unidecode


def input_usuario():
    print("\n\nHola soy tu bot personal. En que puedo ayudarte!")
    print("\t\nMenu:")
    print("\t1. Consultar acciones")
    print("\t2. Consultar clima")
    print("\t3. Salir")



    texto = input("Digite el nombre-> ")

    return unidecode(texto.lower())

