# Lista 2 - Projeto Polinômio
import re

class No:
    def __init__(self, coeficiente, grau):
        self.coeficiente = coeficiente
        self.grau = grau
        self.proximo = None

class Polinomio:
    def __init__(self):
        self.cabeca = No(0, -1)

    def inserir(self, coeficiente, grau):
        if coeficiente == 0:
            return

        novo = No(coeficiente, grau)
        atual = self.cabeca

        while atual.proximo is not None and atual.proximo.grau > grau:
            atual = atual.proximo

        novo.proximo = atual.proximo
        atual.proximo = novo

    def simplificar(self):
        atual = self.cabeca.proximo
        while atual is not None and atual.proximo is not None:
            if atual.grau == atual.proximo.grau:
                atual.coeficiente += atual.proximo.coeficiente
                atual.proximo = atual.proximo.proximo
                if atual.coeficiente == 0:
                    self.cabeca.proximo = self._remover_no(self.cabeca, atual)
                    atual = self.cabeca.proximo
            else:
                atual = atual.proximo

    def _remover_no(self, cabeca_aux, no_remover):
        anterior = cabeca_aux
        while anterior.proximo is not None:
            if anterior.proximo is no_remover:
                anterior.proximo = anterior.proximo.proximo
                break
            anterior = anterior.proximo
        return cabeca_aux.proximo

    def grau(self):
        if self.cabeca.proximo is None:
            return 0
        return self.cabeca.proximo.grau

    def tamanho(self):
        contador = 0
        atual = self.cabeca.proximo
        while atual is not None:
            contador += 1
            atual = atual.proximo
        return contador

    def avaliar(self, x):
        resultado = 0
        atual = self.cabeca.proximo
        while atual is not None:
            resultado += atual.coeficiente * (x ** atual.grau)
            atual = atual.proximo
        return resultado

    def exibir(self):
        if self.cabeca.proximo is None:
            return "0"

        partes = []
        atual = self.cabeca.proximo
        while atual is not None:
            coef = atual.coeficiente
            g = atual.grau

            if coef == int(coef):
                coef_str = str(int(coef))
            else:
                coef_str = str(coef)

            if g == 0:
                termo = coef_str
            elif g == 1:
                if coef == 1:
                    termo = "x"
                elif coef == -1:
                    termo = "-x"
                else:
                    termo = f"{coef_str}x"
            else:
                if coef == 1:
                    termo = f"x^{g}"
                elif coef == -1:
                    termo = f"-x^{g}"
                else:
                    termo = f"{coef_str}x^{g}"

            partes.append(termo)
            atual = atual.proximo

        resultado = partes[0]
        for parte in partes[1:]:
            if parte.startswith("-"):
                resultado += " - " + parte[1:]
            else:
                resultado += " + " + parte

        return resultado

    def __add__(self, outro):
        novo = Polinomio()
        atual = self.cabeca.proximo
        while atual is not None:
            novo.inserir(atual.coeficiente, atual.grau)
            atual = atual.proximo

        atual = outro.cabeca.proximo
        while atual is not None:
            novo.inserir(atual.coeficiente, atual.grau)
            atual = atual.proximo

        novo.simplificar()
        return novo

    def __sub__(self, outro):
        novo = Polinomio()
        atual = self.cabeca.proximo
        while atual is not None:
            novo.inserir(atual.coeficiente, atual.grau)
            atual = atual.proximo

        atual = outro.cabeca.proximo
        while atual is not None:
            novo.inserir(-atual.coeficiente, atual.grau)
            atual = atual.proximo

        novo.simplificar()
        return novo

    def __mul__(self, outro):
        novo = Polinomio()
        a = self.cabeca.proximo
        while a is not None:
            b = outro.cabeca.proximo
            while b is not None:
                novo.inserir(a.coeficiente * b.coeficiente, a.grau + b.grau)
                b = b.proximo
            a = a.proximo

        novo.simplificar()
        return novo


def _parse_termos_em_formato_pares(texto):
    numeros = re.findall(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)', texto)
    if not numeros:
        return []

    valores = [float(n) for n in numeros]
    termos = []

    for i in range(0, len(valores), 2):
        if i + 1 >= len(valores):
            break
        termos.append((valores[i], int(valores[i + 1])))

    return termos


def _parse_termos_em_formato_x(texto):
    texto = re.sub(r'\s+', '', texto)
    if texto and texto[0] not in ('+', '-'):
        texto = '+' + texto
    texto = re.sub(r'([+-])([+-])', lambda m: '+' if m.group(1) == m.group(2) else '-', texto)

    padrao = r'[+-]?(?:(?:\d+(?:\.\d*)?|\.\d+)?x(?:\^\d+)?|(?:\d+(?:\.\d*)?|\.\d+))'
    termos = []

    for termo in re.findall(padrao, texto):
        match = re.fullmatch(r'(?P<signal>[+-]?)(?:(?P<coef>(?:\d+(?:\.\d*)?|\.\d+)?)x(?:\^(?P<grau>\d+))?|(?P<constante>(?:\d+(?:\.\d*)?|\.\d+)))', termo)
        if not match:
            continue

        if 'x' in termo.lower():
            coef = 1.0 if match.group('coef') in ('', None) else float(match.group('coef'))
            grau = int(match.group('grau')) if match.group('grau') is not None else 1
            if match.group('signal') == '-':
                coef *= -1
            termos.append((coef, grau))
        else:
            coef = float(match.group('constante'))
            if match.group('signal') == '-':
                coef *= -1
            termos.append((coef, 0))

    return termos


def string_para_polinomio(texto):
    p = Polinomio()
    if texto is None:
        return p

    texto = str(texto).strip()
    if not texto:
        return p

    if 'x' in texto.lower() or '^' in texto.lower():
        termos = _parse_termos_em_formato_x(texto)
    else:
        termos = _parse_termos_em_formato_pares(texto)

    for coef, grau in termos:
        p.inserir(coef, grau)

    return p


def processar_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    i = 0
    while i < len(linhas):
        linha = linhas[i].lower()

        if linha in ('+', '-', '*'):
            if i + 2 >= len(linhas):
                i += 1
                continue

            p1 = string_para_polinomio(linhas[i + 1])
            p2 = string_para_polinomio(linhas[i + 2])

            if p1.tamanho() == 0 or p2.tamanho() == 0:
                i += 3
                continue

            if linha == '+':
                resultado = p1 + p2
            elif linha == '-':
                resultado = p1 - p2
            else:
                resultado = p1 * p2

            print(resultado.exibir())
            i += 3
            continue

        if linha == 'p':
            if i + 1 >= len(linhas):
                i += 1
                continue

            p = string_para_polinomio(linhas[i + 1])
            print("0 (polinomio nulo)" if p.tamanho() == 0 else p.exibir())
            i += 2
            continue

        if linha == 'g':
            if i + 1 >= len(linhas):
                i += 1
                continue

            p = string_para_polinomio(linhas[i + 1])
            print(0 if p.tamanho() == 0 else p.grau())
            i += 2
            continue

        if linha == 't':
            if i + 1 >= len(linhas):
                i += 1
                continue

            p = string_para_polinomio(linhas[i + 1])
            print(p.tamanho())
            i += 2
            continue

        if linha == 'a':
            if i + 2 >= len(linhas):
                i += 1
                continue

            try:
                x = float(linhas[i + 1])
                p = string_para_polinomio(linhas[i + 2])
            except ValueError:
                try:
                    p = string_para_polinomio(linhas[i + 1])
                    x = float(linhas[i + 2])
                except ValueError:
                    i += 1
                    continue

            resultado = 0 if p.tamanho() == 0 else p.avaliar(x)
            if resultado == int(resultado):
                resultado = int(resultado)
            print(resultado)
            i += 3
            continue

        i += 1


def main():
    nome_arquivo = "entrada.txt"
    processar_arquivo(nome_arquivo)


if __name__ == "__main__":
    main()
