def verificar_expressao(expressao: str) -> bool:
    pilha = []
    pares = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    for caractere in expressao:
        if caractere in '([{':
            pilha.append(caractere)
        elif caractere in ')]}':
            if not pilha or pilha[-1] != pares[caractere]:
                return False
            pilha.pop()

    return len(pilha) == 0


def main():
    expressao = input("Digite a expressão matemática: ")

    if verificar_expressao(expressao):
        print("A expressão está balanceada!")
    else:
        print("A expressão não está balanceada.")


if __name__ == "__main__":
    main()
