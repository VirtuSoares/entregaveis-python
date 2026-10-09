# 🐍 Entregáveis de Python

Repositório dedicado ao armazenamento e organização dos desafios e atividades práticas desenvolvidos em Python.

---

## 📁 Estrutura de Entregáveis

- 📂 **[Listas-Tuplas-Conjuntos](./Listas-Tuplas-Conjuntos)** (Sprint 04)
  - **Descrição:** Sistema de gerenciamento de produtos.
  - **Recursos aplicados:** Listas, Tuplas, Conjuntos (`set`) e f-strings.

- 📂 **[Semana-05-Validacao-Dados](./Semana-05-Validacao-Dados)** (Sprint 05)
  - **Descrição:** Sistema de análise de dados e validação de cadastros em CSV.
  - **Recursos aplicados:** Leitura de arquivos, Expressões Regulares (`re`), Tratamento de Exceções (`try/except/else/finally`) e Exceção Personalizada.

- 📂 **[Semana-06-POO](./Semana-06-POO)** (Sprint 06)
  - **Descrição:** Sistema Bancário com Orientação a Objetos completa.
  - **Recursos aplicados:**
    - **Classe Abstrata:** `ContaBancaria` utilizando a biblioteca `abc` (`ABC` e `@abstractmethod`).
    - **Herança e `super()`:** Classes `ContaCorrente` e `ContaPoupanca` herdando comportamentos de `ContaBancaria`.
    - **Encapsulamento:** Uso de `@property` e setters com validação de regras de negócio.
    - **Polimorfismo:** Métodos `sacar()` e `calcular_tarifa_mensal()` redefinidos de forma específica em cada classe filha.
    - **Métodos Especiais (Dunder):** Implementação de `__str__`, `__repr__`, `__eq__` e `__lt__`.
    - **Composição:** Classe `Banco` gerenciando uma lista de contas bancárias.

---

## 📊 Diagrama de Classes (Mermaid)

```mermaid
classDiagram
    class ContaBancaria {
        <<Abstract>>
        #str _numero_conta
        #str _titular
        #float _saldo
        +depositar(valor: float)
        +sacar(valor: float)*
        +calcular_tarifa_mensal()* float
    }

    class ContaCorrente {
        -float _limite_cheque_especial
        +sacar(valor: float)
        +calcular_tarifa_mensal() float
    }

    class ContaPoupanca {
        -float _taxa_rendimento
        +sacar(valor: float)
        +aplicar_rendimento() float
        +calcular_tarifa_mensal() float
    }

    class Banco {
        +str nome
        -list~ContaBancaria~ _contas
        +adicionar_conta(conta: ContaBancaria)
        +processar_tarifas_mensais()
    }

    ContaBancaria <|-- ContaCorrente : "é uma"
    ContaBancaria <|-- ContaPoupanca : "é uma"
    Banco "1" o-- "*" ContaBancaria : "gerencia (composição)"
