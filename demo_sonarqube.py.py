"""
Código DE PROPÓSITO problemático, para demonstração no SonarQube.
NÃO use este código em produção: ele contém bugs, vulnerabilidades
e code smells de forma intencional.

Como usar na apresentação:
1. Coloque este arquivo numa pasta de projeto.
2. Rode a análise do SonarQube (sonar.sources=.).
3. Mostre no painel as abas Bugs, Vulnerabilities, Security Hotspots e Code Smells.

Os IDs de regra abaixo (Sxxxx) são indicativos e podem variar conforme a versão.
"""
import hashlib
import os
import pickle
import random
import sqlite3
import subprocess

# ---------------------------------------------------------------------
# VULNERABILIDADES / SECURITY HOTSPOTS
# ---------------------------------------------------------------------

# Credenciais fixas no código (S2068)
DB_PASSWORD = "admin123"
API_TOKEN = "ghp_abcdefghijklmnopqrstuvwxyz123456"

# URL sem criptografia (S5332)
API_URL = "http://api.exemplo.com/dados"


def buscar_usuario(nome):
    """SQL Injection: consulta montada com concatenação (S3649)."""
    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM alunos WHERE nome = '" + nome + "'")
    return cursor.fetchall()


def executar_comando(arquivo):
    """Command Injection: entrada do usuário vai direto para o shell (S4721)."""
    subprocess.call("cat " + arquivo, shell=True)


def gerar_hash_senha(senha):
    """Algoritmo de hash fraco: MD5 (S4790)."""
    return hashlib.md5(senha.encode()).hexdigest()


def gerar_token_sessao():
    """Gerador pseudoaleatório não seguro para uso sensível (S2245)."""
    return str(random.random())


def carregar_dados(conteudo):
    """Desserialização insegura com pickle (S5135)."""
    return pickle.loads(conteudo)


def calcular_expressao(expressao):
    """Uso de eval com entrada externa (S1523)."""
    return eval(expressao)


# ---------------------------------------------------------------------
# BUGS
# ---------------------------------------------------------------------

def comparar_notas(a, b):
    """Comparação de float com igualdade (S1244)."""
    if a * 0.1 == b:
        return True
    return False


def dividir(x, y):
    """Divisão por zero constante (S3518)."""
    return x / 0


def classificar(nota):
    """Todos os ramos fazem a mesma coisa (S3923)."""
    if nota >= 7:
        return "resultado"
    else:
        return "resultado"


def funcao_com_codigo_morto():
    """Código inalcançável após o return (S1763)."""
    return 1
    print("nunca executa")


def comparacao_inutil(x):
    """Condição sempre verdadeira / mesma expressão dos dois lados (S1764)."""
    if x == x:
        return "sempre"
    return "nunca"


def tratar_erro():
    """Except genérico que engole o erro (S5754 / S1166)."""
    try:
        int("abc")
    except:
        pass


# ---------------------------------------------------------------------
# CODE SMELLS
# ---------------------------------------------------------------------

def funcao_complexa(a, b, c, d):
    """Complexidade cognitiva alta, ifs aninhados (S3776)."""
    resultado = 0
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    for i in range(10):
                        if i % 2 == 0:
                            if i > 5:
                                resultado += i
                            else:
                                resultado -= i
                        else:
                            if i > 3:
                                resultado *= 2
    return resultado


def parametro_nao_usado(nome, idade, email):
    """Parâmetros que não são usados (S1172)."""
    return nome


def variavel_nao_usada():
    """Variável local atribuída e nunca usada (S1481)."""
    temporario = 42
    outro = "texto"
    return 1


def strings_repetidas():
    """Mesma string literal duplicada várias vezes (S1192)."""
    print("Cadastro de alunos")
    print("Cadastro de alunos")
    print("Cadastro de alunos")
    print("Cadastro de alunos")


def ifs_colapsaveis(x, y):
    """Ifs que poderiam ser combinados (S1066)."""
    if x > 0:
        if y > 0:
            return True
    return False


def ternario_aninhado(n):
    """Operador ternário aninhado, difícil de ler (S3358)."""
    return "alto" if n > 10 else "medio" if n > 5 else "baixo"


# TODO: refatorar esta função depois (S1135)
def funcao_com_todo():
    return None


# Código comentado (S125)
# def funcao_antiga():
#     x = 1
#     y = 2
#     return x + y


class classeMalNomeada:
    """Nome de classe fora do padrão PascalCase (S101)."""

    def MetodoMalNomeado(self, ParametroRuim):
        """Nome de método e parâmetro fora do padrão snake_case (S100 / S117)."""
        return ParametroRuim


def funcao_gigante_com_muitos_parametros(a, b, c, d, e, f, g, h, i, j):
    """Funçao com parâmetros demais (S107)."""
    return a + b + c + d + e + f + g + h + i + j


def abrir_arquivo_sem_fechar(caminho):
    """Recurso aberto sem 'with' (S2095)."""
    f = open(caminho)
    dados = f.read()
    return dados


if __name__ == "__main__":
    print(buscar_usuario("Maria"))
    print(gerar_hash_senha("123456"))
    print(os.getcwd())