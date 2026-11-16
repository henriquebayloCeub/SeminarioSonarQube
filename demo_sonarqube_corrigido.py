"""
Versão CORRIGIDA do demo_sonarqube.py, para o "antes e depois" no seminário.
Cada função mantém o mesmo nome da versão original, com a correção aplicada.
"""
import hashlib
import hmac
import json
import math
import os
import secrets
import sqlite3
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------
# VULNERABILIDADES CORRIGIDAS
# ---------------------------------------------------------------------

# Segredos vêm do ambiente, nunca do código (S2068)
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
API_TOKEN = os.environ.get("API_TOKEN", "")

# HTTPS em vez de HTTP (S5332)
API_URL = "https://api.exemplo.com/dados"

PASTA_PERMITIDA = Path("dados").resolve()
TITULO_CADASTRO = "Cadastro de alunos"


def buscar_usuario(nome):
    """Consulta parametrizada evita SQL Injection (S3649)."""
    with sqlite3.connect("alunos.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM alunos WHERE nome = ?", (nome,))
        return cursor.fetchall()


def executar_comando(arquivo):
    """Sem shell, com lista de argumentos e caminho validado (S4721)."""
    caminho = (PASTA_PERMITIDA / arquivo).resolve()
    if PASTA_PERMITIDA not in caminho.parents:
        raise ValueError("Caminho fora da pasta permitida")
    subprocess.run(["cat", str(caminho)], check=True)


def gerar_hash_senha(senha, sal=None):
    """PBKDF2 com sal em vez de MD5 (S4790)."""
    sal = sal or secrets.token_bytes(16)
    derivado = hashlib.pbkdf2_hmac("sha256", senha.encode(), sal, 600_000)
    return sal.hex() + ":" + derivado.hex()


def verificar_senha(senha, armazenado):
    """Comparação em tempo constante."""
    sal_hex, hash_hex = armazenado.split(":")
    derivado = hashlib.pbkdf2_hmac(
        "sha256", senha.encode(), bytes.fromhex(sal_hex), 600_000
    )
    return hmac.compare_digest(derivado.hex(), hash_hex)


def gerar_token_sessao():
    """Gerador criptograficamente seguro (S2245)."""
    return secrets.token_urlsafe(32)


def carregar_dados(conteudo):
    """JSON em vez de pickle (S5135)."""
    return json.loads(conteudo)


def calcular_expressao(a, b, operador):
    """Operações permitidas explicitamente, sem eval (S1523)."""
    operacoes = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
    }
    if operador not in operacoes:
        raise ValueError("Operador não permitido")
    return operacoes[operador](a, b)


# ---------------------------------------------------------------------
# BUGS CORRIGIDOS
# ---------------------------------------------------------------------

def comparar_notas(a, b):
    """Comparação de float com tolerância (S1244)."""
    return math.isclose(a * 0.1, b, rel_tol=1e-9)


def dividir(x, y):
    """Divisor real, com tratamento do zero (S3518)."""
    if y == 0:
        raise ZeroDivisionError("O divisor não pode ser zero")
    return x / y


def classificar(nota):
    """Ramos com resultados distintos (S3923)."""
    return "aprovado" if nota >= 7 else "reprovado"


def funcao_com_codigo_morto():
    """Sem código depois do return (S1763)."""
    return 1


def comparacao_inutil(x, y):
    """Compara valores diferentes (S1764)."""
    return "iguais" if x == y else "diferentes"


def tratar_erro():
    """Exceção específica e registrada (S5754 / S1166)."""
    try:
        return int("abc")
    except ValueError as erro:
        print(f"Valor inválido: {erro}")
        return None


# ---------------------------------------------------------------------
# CODE SMELLS CORRIGIDOS
# ---------------------------------------------------------------------

def _ajustar_por_indice(resultado, i):
    """Parte da lógica extraída para reduzir a complexidade (S3776)."""
    if i % 2 == 0:
        return resultado + i if i > 5 else resultado - i
    return resultado * 2 if i > 3 else resultado


def funcao_complexa(a, b, c, d):
    """Guard clause em vez de ifs aninhados, com lógica extraída."""
    if not (a > 0 and b > 0 and c > 0 and d > 0):
        return 0
    resultado = 0
    for i in range(10):
        resultado = _ajustar_por_indice(resultado, i)
    return resultado


def parametro_nao_usado(nome):
    """Só os parâmetros necessários (S1172)."""
    return nome


def variavel_nao_usada():
    """Sem variáveis sobrando (S1481)."""
    return 1


def strings_repetidas():
    """Constante em vez de literal repetido (S1192)."""
    for _ in range(4):
        print(TITULO_CADASTRO)


def ifs_colapsaveis(x, y):
    """Condições combinadas (S1066)."""
    return x > 0 and y > 0


def ternario_aninhado(n):
    """If/elif legível no lugar do ternário aninhado (S3358)."""
    if n > 10:
        return "alto"
    if n > 5:
        return "medio"
    return "baixo"


def funcao_sem_pendencias():
    """Pendência resolvida e sem código comentado (S1135 / S125)."""
    return None


class ClasseBemNomeada:
    """Nomes seguindo PEP 8 (S101 / S100 / S117)."""

    def metodo_bem_nomeado(self, parametro_bom):
        return parametro_bom


def somar_valores(*valores):
    """Parâmetros variáveis no lugar de dez parâmetros fixos (S107)."""
    return sum(valores)


def abrir_arquivo_sem_fechar(caminho):
    """Context manager garante o fechamento (S2095)."""
    with open(caminho, encoding="utf-8") as arquivo:
        return arquivo.read()


if __name__ == "__main__":
    print(buscar_usuario("Maria"))
    print(gerar_hash_senha("123456"))