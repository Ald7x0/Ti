def soma_segura(a, b):
    try:
        resultado = a + b
        print(f"Somando {a} com {b}... resultado: {resultado}")
        return resultado
    except TypeError:
        print(f"Não consegui somar {a} com {b} Verifique se ambos são números")
        return 0


def divisao(x, y):
    try:
        resultado = x / y
        print(f"Dividindo {x} por {y}... resultado: {resultado}")
        return resultado
    except ZeroDivisionError:
        print(f"Tentativa de dividir {x} por {y} Isso não é permitido")
        return "Não divida por zero!"