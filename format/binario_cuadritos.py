def transformar_binario_a_cuadritos(cadena_binaria: str) -> str:
    """
    Transforma una cadena de texto binaria tradicional ('1' y '0')
    en los caracteres visuales de la Regla de Kav ('■' y '□').
    """
    # Usamos un diccionario de mapeo para reemplazar los caracteres directos
    mapeo = {"1": "■", "0": "□"}

    # Recorremos cada caracter de la cadena. Si no es 1 o 0, dejamos el caracter original.
    resultado = [mapeo.get(char, char) for char in cadena_binaria]

    return "".join(resultado)