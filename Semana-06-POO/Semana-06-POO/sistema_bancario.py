"""
Entregável de Desenvolvimento em Python - Semana 06 (Sprint 6)
Sistema Bancário Orientado a Objetos (POO).
Aplicações de: Classes Abstratas, Encapsulamento (@property), Herança,
Polimorfismo, Métodos Especiais (Dunder) e Tratamento de Exceções.
"""

from abc import ABC, abstractmethod


# --- CLASSES DE EXCEÇÃO PERSONALIZADAS ---
class SaldoInsuficienteError(Exception):
    """Lançada quando o valor do saque/transferência excede o saldo disponível."""
    pass


class ValorInvalidoError(ValueError):
    """Lançada quando um valor informado é menor ou igual a zero."""
    pass


# --- CLASSE ABSTRATA (MÃE) ---
class ContaBancaria(ABC):
    """Classe abstrata base para representar uma conta bancária."""

    def __init__(self, numero_conta: str, titular: str, saldo_inicial: float = 0.0) -> None:
        self._numero_conta = numero_conta
        self.titular = titular  # Usa o setter da property para validação
        self._saldo = 0.0
        self.saldo = saldo_inicial  # Usa o setter da property para validação

    @property
    def numero_conta(self) -> str:
        return self._numero_conta

    @property
    def titular(self) -> str:
        return self._titular

    @titular.setter
    def titular(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("O nome do titular não pode ser vazio.")
        self._titular = valor.strip().title()

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        if valor < 0:
            raise ValorInvalidoError("O saldo inicial não pode ser negativo.")
        self._saldo = valor

    def depositar(self, valor: float) -> None:
        """Realiza depósito na conta."""
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser maior que zero.")
        self._saldo += valor

    @abstractmethod
    def sacar(self, valor: float) -> None:
        """Método abstrato para saque. Deve ser implementado pelas subclasses."""
        pass

    @abstractmethod
    def calcular_tarifa_mensal(self) -> float:
        """Método abstrato para calcular a tarifa de manutenção mensal."""
        pass

    # --- MÉTODOS ESPECIAIS (DUNDER) ---
    def __str__(self) -> str:
        return f"Conta {self._numero_conta} | Titular: {self._titular} | Saldo: R$ {self._saldo:.2f}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(numero_conta='{self._numero_conta}', titular='{self._titular}', saldo={self._saldo})"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, ContaBancaria):
            return False
        return self._numero_conta == outro._numero_conta

    def __lt__(self, outro: "ContaBancaria") -> bool:
        return self._saldo < outro._saldo


# --- CLASSE FILHA 1: CONTA CORRENTE ---
class ContaCorrente(ContaBancaria):
    """Representa uma Conta Corrente que possui limite de cheque especial."""

    def __init__(self, numero_conta: str, titular: str, saldo_inicial: float = 0.0, limite_cheque_especial: float = 500.0) -> None:
        super().__init__(numero_conta, titular, saldo_inicial)
        self.limite_cheque_especial = limite_cheque_especial

    @property
    def limite_cheque_especial(self) -> float:
        return self._limite_cheque_especial

    @limite_cheque_especial.setter
    def limite_cheque_especial(self, valor: float) -> None:
        if valor < 0:
            raise ValorInvalidoError("O limite do cheque especial não pode ser negativo.")
        self._limite_cheque_especial = valor

    def sacar(self, valor: float) -> None:
        """Sobrescreve o método de saque permitindo o uso do cheque especial."""
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser maior que zero.")
        if valor > (self._saldo + self._limite_cheque_especial):
            raise SaldoInsuficienteError(f"Saldo + limite insuficiente para o saque de R$ {valor:.2f}.")
        self._saldo -= valor

    def calcular_tarifa_mensal(self) -> float:
        """Calcula tarifa mensal fixa para Conta Corrente."""
        return 20.00


# --- CLASSE FILHA 2: CONTA POUPANÇA ---
class ContaPoupanca(ContaBancaria):
    """Representa uma Conta Poupança que rende juros e não aceita saldo negativo."""

    def __init__(self, numero_conta: str, titular: str, saldo_inicial: float = 0.0, taxa_rendimento: float = 0.005) -> None:
        super().__init__(numero_conta, titular, saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self) -> float:
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor: float) -> None:
        if valor < 0:
            raise ValorInvalidoError("A taxa de rendimento não pode ser negativa.")
        self._taxa_rendimento = valor

    def sacar(self, valor: float) -> None:
        """Sobrescreve o método de saque garantindo que o saldo não fique negativo."""
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser maior que zero.")
        if valor > self._saldo:
            raise SaldoInsuficienteError(f"Saldo insuficiente para realizar o saque de R$ {valor:.2f}.")
        self._saldo -= valor

    def aplicar_rendimento(self) -> float:
        """Aplica o rendimento mensal ao saldo."""
        rendimento = self._saldo * self._taxa_rendimento
        self._saldo += rendimento
        return rendimento

    def calcular_tarifa_mensal(self) -> float:
        """Conta poupança é isenta de tarifa mensal."""
        return 0.00


# --- CLASSE 4: BANCO (COMPOSIÇÃO / GERENCIAMENTO) ---
class Banco:
    """Classe responsável por gerenciar um conjunto de contas bancárias."""

    def __init__(self, nome: str) -> None:
        self.nome = nome
        self._contas: list[ContaBancaria] = []

    def adicionar_conta(self, conta: ContaBancaria) -> None:
        """Adiciona uma conta ao banco mantendo a consistência sem duplicatas."""
        if conta in self._contas:
            raise ValueError(f"A conta {conta.numero_conta} já está cadastrada no banco.")
        self._contas.append(conta)

    def listar_contas(self) -> list[ContaBancaria]:
        return self._contas.copy()

    def processar_tarifas_mensais(self) -> None:
        """Demonstra o Polimorfismo: aplica cobranças chamando o método correspondente de cada subclasse."""
        print(f"\n--- Processando Tarifas Mensais no Banco '{self.nome}' ---")
        for conta in self._contas:
            tarifa = conta.calcular_tarifa_mensal()
            if tarifa > 0:
                conta.sacar(tarifa)
                print(f"• {conta.titular} ({conta.__class__.__name__}): Cobrado R$ {tarifa:.2f} de tarifa.")
            else:
                print(f"• {conta.titular} ({conta.__class__.__name__}): Isento de tarifa.")


# --- TESTES E DEMONSTRAÇÃO COMPLETA ---
if __name__ == "__main__":
    print("=" * 60)
    print("      SISTEMA BANCÁRIO ORIENTADO A OBJETOS (DEMO)      ")
    print("=" * 60)

    banco = Banco("Banco Central Python")

    # 1. Instanciando pelo menos 10 objetos
    contas = [
        ContaCorrente("1001", "Carlos Silva", 1500.0, 500.0),
        ContaCorrente("1002", "Ana Souza", 3000.0, 1000.0),
        ContaCorrente("1003", "Mariana Costa", 200.0, 300.0),
        ContaCorrente("1004", "Pedro Rocha", 50.0, 200.0),
        ContaCorrente("1005", "Fernanda Lima", 5000.0, 1500.0),
        ContaPoupanca("2001", "Lucas Mendes", 800.0, 0.006),
        ContaPoupanca("2002", "Beatriz Alves", 1200.0, 0.005),
        ContaPoupanca("2003", "Gabriel Santos", 4500.0, 0.007),
        ContaPoupanca("2004", "Juliana Paes", 10000.0, 0.005),
        ContaPoupanca("2005", "Rafael Oliveira", 350.0, 0.005)
    ]

    for c in contas:
        banco.adicionar_conta(c)

    # 2. Demonstração do Polimorfismo (Iteração sobre tipos diferentes)
    print("\n--- RELATÓRIO INICIAL DE CONTAS E POLIMORFISMO ---")
    for conta in banco.listar_contas():
        # Chama a implementação específica de sacar() e calcular_tarifa_mensal()
        print(f"• [{conta.__class__.__name__}] {conta} | Tarifa: R$ {conta.calcular_tarifa_mensal():.2f}")

    # Processamento em lote usando polimorfismo
    banco.processar_tarifas_mensais()

    # 3. Teste de Operações
    print("\n--- TESTE DE OPERAÇÕES BANCÁRIAS ---")
    cc = contas[0]  # Carlos
    cp = contas[5]  # Lucas

    print(f"Antes do saque: {cc}")
    cc.sacar(1800.0)  # Usa o saldo de 1480 + limite especial
    print(f"Após saque com cheque especial: {cc}")

    print(f"\nAntes do rendimento: {cp}")
    rendimento = cp.aplicar_rendimento()
    print(f"Rendimento de R$ {rendimento:.2f} aplicado. Novo saldo: R$ {cp.saldo:.2f}")

    # 4. Demonstração do Tratamento de Exceções
    print("\n--- TESTANDO VALIDAÇÕES E CAPTURA DE EXCEÇÕES ---")

    # Tentativa de criar conta com titular inválido
    try:
        ContaCorrente("9999", "", 100.0)
    except ValueError as e:
        print(f"[ERRO CAPTURADO - Titular Vazio]: {e}")

    # Tentativa de criar conta com saldo negativo
    try:
        ContaCorrente("9998", "João Ninguém", -50.0)
    except ValorInvalidoError as e:
        print(f"[ERRO CAPTURADO - Saldo Negativo]: {e}")

    # Tentativa de saque além do saldo + limite
    try:
        cp.sacar(5000.0)
    except SaldoInsuficienteError as e:
        print(f"[ERRO CAPTURADO - Saldo Insuficiente]: {e}")

    # 5. Demonstração de Métodos Especiais (Dunder)
    print("\n--- DEMONSTRAÇÃO DE MÉTODOS ESPECIAIS (__lt__, __eq__, __repr__) ---")
    print(f"Repr de uma conta: {repr(cc)}")

    print(f"A conta {contas[0].numero_conta} é menor que a conta {contas[1].numero_conta}? {contas[0] < contas[1]}")
    
    # Ordenação automática usando o método __lt__
    contas_ordenadas = sorted(banco.listar_contas())
    print("\nContas ordenadas por saldo (crescente):")
    for c in contas_ordenadas:
        print(f"  - {c.titular}: R$ {c.saldo:.2f}")

    print("\n" + "=" * 60)
