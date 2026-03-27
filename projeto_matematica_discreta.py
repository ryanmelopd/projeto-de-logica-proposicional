#Parte 1: Conectivos lógicos

def negacao(p):
   return not p

def conjuncao (p,q):
    return p and q

def disjuncao (p,q):
    return p or q

def implicacao (p,q):
    return (not p) or q

def bicondicional (p,q):
    return p == q

def classificar(resultados):
    if all(resultados):
        return "Tautologia"
    elif not any(resultados):
        return "Contradição"
    else:
        return "Contingência"

def f(v): return "V" if v else "F"

# Parte 2: Tabelas-verdade

#p->q;
print("-" * 12)
print("p | q | p -> q")
resultados = []
for p in [True,False]:
    for q in [True,False]:
        resultado = implicacao(p,q)
        resultados.append(resultado)
        print(f"{f(p)} | {f(q)} | {f(resultado)}")
print("Classificação: ", classificar(resultados))

#(p^q)->r;
print("-" * 28)
print("p | q | r | p^q | (p^q)->r ")
resultados = []
for p in[True,False]:
    for q in[True,False]:
        for r in [True,False]:
            p_e_q = p and q 
            resultado = implicacao(p_e_q, r)
            resultados.append(resultado)
            print(f"{f(p)} | {f(q)} | {f(r)} | {f(p_e_q)}   | {f(resultado)}")
print("Classificação: ", classificar(resultados))

#(p->q)^(q->r)->(p->r);
print("-" * 50)
print("p | q | r | p->q | q->r | p->r | (p->q)^(q->r) | (p->q)^(q->r)->(p->r)")
resultados = []
for p in[True,False]:
    for q in[True,False]:
        for r in[True,False]:
            p_q = implicacao(p,q)
            q_r = implicacao(q,r)
            p_r = implicacao(p,r)
            p_implica_q_e_q_implica_r = conjuncao(p_q,q_r)
            resultado = implicacao(p_implica_q_e_q_implica_r,p_r)
            resultados.append(resultado)
            print(f"{f(p)} | {f(q)} | {f(r)} | {f(p_q)}    | {f(q_r) }    | {f(p_r)}    | {f(p_implica_q_e_q_implica_r)}             | {f(resultado)}")
print("Classificação: ", classificar(resultados))

#Parte 3: Classificação de Fórmulas
    
#pV¬q;
print("-" * 28)
print("p | q | ¬q | pV¬q ")
resultados = []
for p in[True,False]:
    for q in[True,False]:
        nao_q = not q 
        resultado = conjuncao(p,nao_q)
        resultados.append(resultado)
        print(f"{f(p)} | {f(q)} |  {f(nao_q)} |  {f(resultado)} ")
print("Classificação: ", classificar(resultados))

#p^¬q;
print("-" * 28)
print("p | q | ¬q | p^¬q ")
resultados = []
for p in[True,False]:
    for q in[True,False]:
        nao_q = not q
        resultado = disjuncao(p,nao_q)
        resultados.append(resultado)
        print(f"{f(p)} | {f(q)} |  {f(nao_q)} |  {f(resultado)} ")
print("Classificação: ", classificar(resultados))

#p->q;
print("-" * 28) 
print("p | q | p->q " )
resultados = []
for p in[True,False]:
    for q in[True,False]:
        resultado = implicacao(p,q)
        resultados.append(resultado)
        print(f"{f(p)} | {f(q)} | {f(resultado)} ")
print("Classificação: ", classificar(resultados))