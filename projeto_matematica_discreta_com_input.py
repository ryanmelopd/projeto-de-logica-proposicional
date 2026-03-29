import itertools

# Parte 1: Conectivos Lógicos

def negacao(p):
    return not p

def conjuncao(p, q):
    return p and q

def disjuncao(p, q):
    return p or q

def implicacao(p, q):
    return (not p) or q

def bicondicional(p, q):
    return p == q

def f(v):
    return "V" if v else "F"

# Conversor para o Python entender 

def converter(expressao):
    expressao = expressao.replace("¬", " not ")
    expressao = expressao.replace("^", " and ")
    expressao = expressao.replace("V", " or ")

    while "<->" in expressao:
        i = expressao.index("<->")
        esquerda = expressao[:i].strip().split()[-1]
        direita = expressao[i+3:].strip().split()[0]
        expressao = expressao.replace(f"{esquerda}<->{direita}", f"({esquerda} == {direita})")

    while "->" in expressao:
        i = expressao.index("->")
        esquerda = expressao[:i].strip().split()[-1]
        direita = expressao[i+2:].strip().split()[0]
        expressao = expressao.replace(f"{esquerda}->{direita}", f"(not {esquerda} or {direita})")

    return expressao

# Formatação dos símbolos

def formatar_nome(expr):
    expr = expr.replace("<->", " ↔ ")
    expr = expr.replace("->", " → ")
    expr = expr.replace("^", " ∧ ")
    expr = expr.replace("V", " ∨ ")
    expr = expr.replace("¬", " ¬ ")
    return expr

# Parte 3 - Classificação da tabela-verdade 

def classificar(resultados):
    if all(resultados):
        return "Tautologia"
    elif not any(resultados):
        return "Contradição"
    else:
        return "Contingência"

# Parte 2: Tabela-verdade

def tabela_verdade(expr):
    variaveis = sorted(set([c for c in expr if c.isalpha()]))
    expr_python = converter(expr)
    expr_formatada = formatar_nome(expr)

    print("Tabela-verdade:")
    print(" | ".join(variaveis) + " | " + expr_formatada)

    resultados = []

    for valores in itertools.product([True, False], repeat=len(variaveis)):
        contexto = dict(zip(variaveis, valores))

        try:
            resultado = eval(expr_python, {}, contexto)
        except:
            print("Erro na expressão!")
            return

        resultados.append(resultado)

        linha = " | ".join(f(v) for v in valores)
        print(linha + " | " + f(resultado))

    print("Classificação:", classificar(resultados))

# Input para o usuário inserir a expressão

expr = input("Digite a expressão (use ^, V, ¬, ->, <->): ")
tabela_verdade(expr)