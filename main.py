from funciones_agentes.Rascado import Rascado
from utils import InputUsuario as IU


def main():
    rascado = None

    try:
        # Inicializar el scraper
        rascado = Rascado(headless=True)

        while True:
            opcion = IU.input_usuario()

            match opcion:
                case '1':
                    empresa = input("Digite el nombre de la empresa -> ").strip()
                    print("[*] Buscando información de la acción...")
                    rascado.obtener_precio_accion(empresa)
                case '2':
                    estado = input("Digite el estado -> ").strip()
                    print("[*] Consultando clima...")
                    rascado.obtener_clima(estado)
                case '3':
                    print("\n¡Excelente día! Nos vemos\n")
                    break

                case _:
                    print("[!] Opción no válida. Intente nuevamente.\n")

    except KeyboardInterrupt:
        print("\n\n[!] Programa interrumpido por el usuario")

    finally:
        if rascado:
            rascado.cerrar()


if __name__ == "__main__":
    main()