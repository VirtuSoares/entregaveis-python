"""
Entregável de Desenvolvimento em Python - Sistema de Produtos
Estruturas de Dados: Listas, Tuplas e Conjuntos (set)
"""

def cadastrar_produtos() -> list[dict]:
    """Lê e armazena o nome, preço e categoria dos produtos em uma lista."""
    produtos = []
    print("=== CADASTRO DE PRODUTOS ===")
    
    while True:
        nome = input("Nome do produto: ").strip()
        
        while True:
            try:
                preco = float(input("Preço do produto (R$): "))
                if preco >= 0:
                    break
                print("O preço não pode ser negativo.")
            except ValueError:
                print("Por favor, digite um valor numérico válido.")

        categoria = input("Categoria do produto: ").strip().capitalize()

        produtos.append({
            "nome": nome,
            "preco": preco,
            "categoria": categoria
        })

        continuar = input("Deseja cadastrar outro produto? (S/N): ").strip().upper()
        if continuar != "S":
            break

    return produtos


def filtrar_por_preco(produtos: list[dict], valor_limite: float, acima: bool = True) -> list[dict]:
    """Filtra produtos que custam acima ou abaixo de um determinado valor."""
    if acima:
        return [p for p in produtos if p["preco"] > valor_limite]
    return [p for p in produtos if p["preco"] < valor_limite]


def obter_categorias_unicas(produtos: list[dict]) -> set:
    """Retorna um conjunto (set) com as categorias únicas dos produtos."""
    return {p["categoria"] for p in produtos}


def calcular_estatisticas(produtos: list[dict]) -> tuple[float, float, float]:
    """Retorna uma tupla imutável com (menor_preco, maior_preco, media_precos)."""
    precos = [p["preco"] for p in produtos]
    
    menor_preco = min(precos)
    maior_preco = max(precos)
    media_precos = sum(precos) / len(precos)

    return (menor_preco, maior_preco, media_precos)


def exibir_relatorio(produtos: list[dict]) -> None:
    """Gera e exibe o relatório final formatado com f-strings."""
    if not produtos:
        print("\nNenhum produto cadastrado.")
        return

    print("\n" + "=" * 50)
    print(f"{'RELATÓRIO FINAL DE PRODUTOS':^50}")
    print("=" * 50)

    print("\n--- TODOS OS PRODUTOS ---")
    for p in produtos:
        print(f"• {p['nome']:<20} | Categoria: {p['categoria']:<15} | Preço: R$ {p['preco']:>8.2f}")

    produtos_crescente = produtos.copy()
    produtos_crescente.sort(key=lambda p: p["preco"])
    
    print("\n--- PRODUTOS POR PREÇO (CRESCENTE - sort()) ---")
    for p in produtos_crescente:
        print(f"• R$ {p['preco']:>8.2f} - {p['nome']} ({p['categoria']})")

    produtos_decrescente = sorted(produtos, key=lambda p: p["preco"], reverse=True)
    
    print("\n--- PRODUTOS POR PREÇO (DECRESCENTE - sorted()) ---")
    for p in produtos_decrescente:
        print(f"• R$ {p['preco']:>8.2f} - {p['nome']} ({p['categoria']})")

    categorias = obter_categorias_unicas(produtos)
    print("\n--- CATEGORIAS ÚNICAS (set) ---")
    print(f"Categorias cadastradas ({len(categorias)}): {', '.join(categorias)}")

    menor, maior, media = calcular_estatisticas(produtos)
    estatisticas = (menor, maior, media)
    
    print("\n--- ESTATÍSTICAS DE PREÇOS (Tupla Imutável) ---")
    print(f"• Menor Preço : R$ {estatisticas[0]:.2f}")
    print(f"• Maior Preço : R$ {estatisticas[1]:.2f}")
    print(f"• Média Preços: R$ {estatisticas[2]:.2f}")

    print("\n--- FILTRAGEM DE PRODUTOS ---")
    limite = estatisticas[2]
    filtrados_acima = filtrar_por_preco(produtos, limite, acima=True)
    
    print(f"Produtos com preço ACIMA da média (R$ {limite:.2f}):")
    if filtrados_acima:
        for p in filtrados_acima:
            print(f"• {p['nome']} - R$ {p['preco']:.2f}")
    else:
        print("• Nenhum produto encontrado acima da média.")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    lista_de_produtos = cadastrar_produtos()
    exibir_relatorio(lista_de_produtos)
