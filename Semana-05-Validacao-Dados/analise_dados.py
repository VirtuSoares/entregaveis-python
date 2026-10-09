"""
Entregável de Desenvolvimento em Python - Semana 05 (Sprint 5)
Análise de Dados, Validação com Regex, Tratamento de Exceções e Manipulação de Arquivos.
"""

import csv
import re


class FormatoInvalidoError(Exception):
    """Exceção personalizada para campos com formatos inválidos."""
    pass


class ValidadorDados:
    """Classe responsável por conter os padrões Regex de validação."""

    PADRAO_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    PADRAO_CPF = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    PADRAO_TELEFONE = r"^\(\d{2}\)\s?\d{4,5}-\d{4}$"
    PADRAO_DATA = r"^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/\d{4}$"

    @classmethod
    def validar_email(cls, email: str) -> bool:
        return bool(re.match(cls.PADRAO_EMAIL, email.strip()))

    @classmethod
    def validar_cpf(cls, cpf: str) -> bool:
        return bool(re.match(cls.PADRAO_CPF, cpf.strip()))

    @classmethod
    def validar_telefone(cls, telefone: str) -> bool:
        return bool(re.match(cls.PADRAO_TELEFONE, telefone.strip()))

    @classmethod
    def validar_data(cls, data: str) -> bool:
        return bool(re.match(cls.PADRAO_DATA, data.strip()))


def analisar_arquivo_csv(caminho_arquivo: str) -> None:
    """Lê um arquivo CSV, valida seus campos e exibe um relatório detalhado."""
    registros_validos = []
    registros_invalidos = []
    total_registros = 0

    print("=== INICIANDO LEITURA E ANÁLISE DE DADOS ===")

    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            colunas_esperadas = {"nome", "email", "cpf", "telefone", "data"}
            if not leitor.fieldnames or not colunas_esperadas.issubset(set(leitor.fieldnames)):
                raise KeyError("O arquivo CSV não possui todas as colunas obrigatórias.")

            for linha in leitor:
                total_registros += 1
                erros_registro = []

                if not ValidadorDados.validar_email(linha["email"]):
                    erros_registro.append("E-mail inválido")

                if not ValidadorDados.validar_cpf(linha["cpf"]):
                    erros_registro.append("CPF inválido (use 000.000.000-00)")

                if not ValidadorDados.validar_telefone(linha["telefone"]):
                    erros_registro.append("Telefone inválido (use (XX) 9XXXX-XXXX)")

                if not ValidadorDados.validar_data(linha["data"]):
                    erros_registro.append("Data inválida (use DD/MM/AAAA)")

                try:
                    if erros_registro:
                        raise FormatoInvalidoError(", ".join(erros_registro))
                    registros_validos.append(linha)
                except FormatoInvalidoError as erro:
                    registros_invalidos.append({
                        "registro": linha,
                        "motivo": str(erro)
                    })

    except FileNotFoundError:
        print(f"\n[ERRO CRÍTICO] O arquivo '{caminho_arquivo}' não foi encontrado.")
        return
    except KeyError as erro:
        print(f"\n[ERRO DE ESTRUTURA] {erro}")
        return
    except ValueError as erro:
        print(f"\n[ERRO DE VALOR] Falha ao converter tipo de dado: {erro}")
        return
    except Exception as erro:
        print(f"\n[ERRO INESPERADO] Ocorreu um erro não previsto: {erro}")
        return
    else:
        print("\n[SUCESSO] Processamento do arquivo concluído sem falhas de leitura!")
    finally:
        print("[FINALIZAÇÃO] Encerrando bloco de análise de dados.\n")

    print("=" * 60)
    print(f"{'RELATÓRIO FINAL DE ANÁLISE DE DADOS':^60}")
    print("=" * 60)

    print("\n--- ESTATÍSTICAS GERAIS ---")
    print(f"• Total de registros processados: {total_registros}")
    print(f"• Registros VÁLIDOS             : {len(registros_validos)}")
    print(f"• Registros INVÁLIDOS           : {len(registros_invalidos)}")

    print("\n--- REGISTROS VÁLIDOS ---")
    if registros_validos:
        for reg in registros_validos:
            print(f"• {reg['nome']:<18} | CPF: {reg['cpf']} | Tel: {reg['telefone']} | E-mail: {reg['email']}")
    else:
        print("• Nenhum registro válido encontrado.")

    print("\n--- REGISTROS INVÁLIDOS E MOTIVOS ---")
    if registros_invalidos:
        for item in registros_invalidos:
            nome = item['registro'].get('nome', 'Sem nome')
            print(f"• {nome:<18} -> Motivo(s): {item['motivo']}")
    else:
        print("• Nenhum registro inválido encontrado.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    analisar_arquivo_csv("Semana-05-Validacao-Dados/dados.csv")
