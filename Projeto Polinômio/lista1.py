# Lista 1 - Listas Encadeadas
class No:
    def __init__(self, valor1, valor2):
        self.valor1 = valor1
        self.valor2 = valor2
        self.proximo = None


class Lista:
    def __init__(self):
        self.cabeca = None

    def obter_proximo(self, no):
        return no.proximo

    def obter_valor(self, no):
        return (no.valor1, no.valor2)

    def alterar_no(self, no, novo_valor1, novo_valor2):
        no.valor1 = novo_valor1
        no.valor2 = novo_valor2

    def tamanho(self):
        contador = 0
        atual = self.cabeca
        while atual is not None:
            contador += 1
            atual = atual.proximo
        return contador

    def existe(self, no):
        atual = self.cabeca
        while atual is not None:
            if atual is no:
                return True
            atual = atual.proximo
        return False

    def mostrar_all(self):
        elementos = []
        atual = self.cabeca
        while atual is not None:
            elementos.append((atual.valor1, atual.valor2))
            atual = atual.proximo
        return elementos

    def buscar(self, valor1):
        atual = self.cabeca
        while atual is not None:
            if atual.valor1 == valor1:
                return atual
            atual = atual.proximo
        return None

    def inserir(self, valor1, valor2):
        novo_no = No(valor1, valor2)

        if self.cabeca is None or self.cabeca.valor1 >= valor1:
            novo_no.proximo = self.cabeca
            self.cabeca = novo_no
            return

        atual = self.cabeca
        while atual.proximo is not None and atual.proximo.valor1 < valor1:
            atual = atual.proximo

        novo_no.proximo = atual.proximo
        atual.proximo = novo_no

    def excluir(self, valor1):
        if self.cabeca is None:
            print("Lista vazia!")
            return

        if self.cabeca.valor1 == valor1:
            self.cabeca = self.cabeca.proximo
            return

        atual = self.cabeca
        while atual.proximo is not None:
            if atual.proximo.valor1 == valor1:
                atual.proximo = atual.proximo.proximo
                return
            atual = atual.proximo

        print(f"Nó com valor1={valor1} não encontrado.")

    def destrutor(self, valor1):
        self.excluir(valor1)



def main():
    lista = Lista()

    print("Inserindo elementos...")
    lista.inserir(5, 50)
    lista.inserir(2, 20)
    lista.inserir(8, 80)
    lista.inserir(1, 10)
    lista.inserir(4, 40)

    print("Lista atual:")
    print(lista.mostrar_all())

    print(f"\nTamanho da lista: {lista.tamanho()}")

    print("\nBuscar nó com valor1 = 4:")
    no_encontrado = lista.buscar(4)
    if no_encontrado:
        print(f"Encontrado: {lista.obter_valor(no_encontrado)}")
    else:
        print("Não encontrado.")

    print("\nVerificar se um nó existe:")
    no_teste = lista.cabeca
    print(f"O primeiro nó existe na lista?: {lista.existe(no_teste)}")

    print("\nObter próximo do primeiro nó:")
    proximo = lista.obter_proximo(no_teste)
    if proximo:
        print(f"Próximo do primeiro: {lista.obter_valor(proximo)}")

    print("\nAlterar o nó com valor1 = 2:")
    no_alterar = lista.buscar(2)
    if no_alterar:
        lista.alterar_no(no_alterar, 2, 999)
        print("Lista depois da alteração:")
        print(lista.mostrar_all())

    print("\nExcluir nó com valor1 = 5:")
    lista.excluir(5)
    print("Lista depois da exclusão:")
    print(lista.mostrar_all())

    print("\nDestrutor do nó com valor1 = 8:")
    lista.destrutor(8)
    print("Lista depois do destrutor:")
    print(lista.mostrar_all())

    print(f"\nTamanho final da lista: {lista.tamanho()}")


if __name__ == "__main__":
    main()
