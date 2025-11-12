"""
Archivo: src/main.py
Punto de entrada de la aplicación de consola.
"""

from .cli import ejecutar_aplicacion


def main() -> None:
    """
    Punto de entrada lógico de la aplicación.
    """
    ejecutar_aplicacion()


if __name__ == "__main__":
    main()
