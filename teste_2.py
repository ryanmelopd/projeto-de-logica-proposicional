"""
Avaliador de Fórmulas Lógicas
Suporta: ¬ (negação), ∧ (conjunção), ∨ (disjunção), → (implicação), ↔ (bicondicional)
Variáveis: letras maiúsculas (P, Q, R, S, ...)
Também aceita: ~ para ¬, & ou ^ para ∧, | para ∨, > para →, = para ↔
"""

import itertools
import re


# ── Normalização de símbolos alternativos ──────────────────────────────────────

def normalizar(formula):
    formula = formula.replace('~', '¬')
    formula = formula.replace('&', '∧').replace('^', '∧')
    formula = formula.replace('|', '∨')
    formula = formula.replace('->', '→').replace('>', '→')
    formula = formula.replace('<->', '↔').replace('=', '↔')
    return formula


# ── Tokenizador ────────────────────────────────────────────────────────────────

def tokenizar(formula):
    tokens = []
    i = 0
    while i < len(formula):
        c = formula[i]
        if c == ' ':
            i += 1
            continue
        elif re.match(r'[A-Z]', c):
            tokens.append(('VAR', c))
        elif c == '¬':
            tokens.append(('NEG', c))
        elif c == '∧':
            tokens.append(('AND', c))
        elif c == '∨':
            tokens.append(('OR', c))
        elif c == '→':
            tokens.append(('IMP', c))
        elif c == '↔':
            tokens.append(('BIC', c))
        elif c == '(':
            tokens.append(('LPAREN', c))
        elif c == ')':
            tokens.append(('RPAREN', c))
        else:
            raise ValueError(f'Símbolo inválido: "{c}"')
        i += 1
    return tokens


# ── Parser recursivo descendente ───────────────────────────────────────────────
# Precedência (menor para maior): ↔ → ∨ ∧ ¬

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse(self):
        node = self.parse_bic()
        if self.pos < len(self.tokens):
            raise ValueError(f'Fórmula com partes não reconhecidas a partir de "{self.tokens[self.pos][1]}"')
        return node

    def parse_bic(self):
        left = self.parse_imp()
        while self.peek() and self.peek()[0] == 'BIC':
            self.consume()
            right = self.parse_imp()
            left = ('BIC', left, right)
        return left

    def parse_imp(self):
        left = self.parse_or()
        if self.peek() and self.peek()[0] == 'IMP':
            self.consume()
            right = self.parse_imp()  # recursão → associativa à direita
            return ('IMP', left, right)
        return left

    def parse_or(self):
        left = self.parse_and()
        while self.peek() and self.peek()[0] == 'OR':
            self.consume()
            right = self.parse_and()
            left = ('OR', left, right)
        return left

    def parse_and(self):
        left = self.parse_neg()
        while self.peek() and self.peek()[0] == 'AND':
            self.consume()
            right = self.parse_neg()
            left = ('AND', left, right)
        return left

    def parse_neg(self):
        if self.peek() and self.peek()[0] == 'NEG':
            self.consume()
            operand = self.parse_neg()
            return ('NEG', operand)
        return self.parse_atom()

    def parse_atom(self):
        t = self.peek()
        if t is None:
            raise ValueError('Fórmula incompleta ou inválida')
        if t[0] == 'VAR':
            self.consume()
            return ('VAR', t[1])
        if t[0] == 'LPAREN':
            self.consume()
            node = self.parse_bic()
            if self.peek() is None or self.peek()[0] != 'RPAREN':
                raise ValueError('Parêntese não fechado')
            self.consume()
            return node
        raise ValueError(f'Token inesperado: "{t[1]}"')


# ── Avaliador de árvore ────────────────────────────────────────────────────────

def avaliar(node, env):
    tipo = node[0]
    if tipo == 'VAR':
        return env[node[1]]
    elif tipo == 'NEG':
        return not avaliar(node[1], env)
    elif tipo == 'AND':
        return avaliar(node[1], env) and avaliar(node[2], env)
    elif tipo == 'OR':
        return avaliar(node[1], env) or avaliar(node[2], env)
    elif tipo == 'IMP':
        return (not avaliar(node[1], env)) or avaliar(node[2], env)
    elif tipo == 'BIC':
        return avaliar(node[1], env) == avaliar(node[2], env)
    raise ValueError(f'Nó desconhecido: {tipo}')


# ── Extração de variáveis ──────────────────────────────────────────────────────

def extrair_variaveis(formula):
    return sorted(set(re.findall(r'[A-Z]', formula)))


# ── Classificação ──────────────────────────────────────────────────────────────

def classificar(resultados):
    if all(resultados):
        return 'Tautologia'
    elif not any(resultados):
        return 'Contradição'
    else:
        return 'Contingência'


# ── Formatação da tabela ───────────────────────────────────────────────────────

def formatar_valor(v):
    return 'V' if v else 'F'


def imprimir_tabela(formula, variaveis, arvore):
    col_vars = [v.center(3) for v in variaveis]
    col_formula = formula.center(max(len(formula), 6))

    cabecalho = ' | '.join(col_vars) + ' | ' + col_formula
    separador = '-' * len(cabecalho)

    print()
    print(separador)
    print(cabecalho)
    print(separador)

    resultados = []
    for combo in itertools.product([True, False], repeat=len(variaveis)):
        env = dict(zip(variaveis, combo))
        resultado = avaliar(arvore, env)
        resultados.append(resultado)

        vals_vars = ' | '.join(formatar_valor(env[v]).center(3) for v in variaveis)
        val_res = formatar_valor(resultado).center(max(len(formula), 6))
        print(f'{vals_vars} | {val_res}')

    print(separador)

    cls = classificar(resultados)
    print(f'Classificação: {cls}')
    print()
    return cls


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print('=' * 55)
    print('       AVALIADOR DE FÓRMULAS LÓGICAS')
    print('=' * 55)
    print('Símbolos aceitos:')
    print('  ¬  ou  ~          →  negação')
    print('  ∧  ou  &  ou  ^   →  conjunção (E)')
    print('  ∨  ou  |          →  disjunção (OU)')
    print('  →  ou  ->         →  implicação')
    print('  ↔  ou  <->        →  bicondicional')
    print('Variáveis: letras maiúsculas (P, Q, R, S, ...)')
    print('Digite "sair" para encerrar.')
    print('=' * 55)

    while True:
        print()
        entrada = input('Fórmula: ').strip()

        if entrada.lower() in ('sair', 'exit', 'quit'):
            print('Encerrando...')
            break

        if not entrada:
            continue

        try:
            formula = normalizar(entrada)
            variaveis = extrair_variaveis(formula)

            if not variaveis:
                print('Erro: nenhuma variável encontrada. Use letras maiúsculas (P, Q, R...).')
                continue

            tokens = tokenizar(formula)
            parser = Parser(tokens)
            arvore = parser.parse()

            imprimir_tabela(formula, variaveis, arvore)

        except ValueError as e:
            print(f'Erro: {e}')
        except Exception as e:
            print(f'Erro inesperado: {e}')


if __name__ == '__main__':
    main()