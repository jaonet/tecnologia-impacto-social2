"""Protótipo de console: EcoPonto (ODS 12)."""
from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome, email):
        self.nome, self.email = nome, email
    @abstractmethod
    def acao_principal(self): pass

class Cidadao(Usuario):
    def __init__(self, nome, email):
        super().__init__(nome, email); self._saldo_pontos = 0
    def acao_principal(self): return "Entregar resíduos eletrônicos"
    @property
    def saldo_pontos(self): return self._saldo_pontos
    def adicionar_pontos(self, pontos):
        if pontos < 0: raise ValueError("Pontos não podem ser negativos.")
        self._saldo_pontos += pontos

class Operador(Usuario):
    def __init__(self, nome, email, identificacao):
        super().__init__(nome, email); self.identificacao = identificacao
    def acao_principal(self): return "Validar entrega"

class ResiduoEletronico(ABC):
    def __init__(self, tipo, peso_kg):
        if peso_kg <= 0: raise ValueError("O peso deve ser maior que zero.")
        self.tipo, self.peso_kg = tipo, float(peso_kg)
    @abstractmethod
    def calcular_pontos(self): pass

class PequenoEletronico(ResiduoEletronico):
    def calcular_pontos(self): return int(self.peso_kg * 10)

class GrandeEletronico(ResiduoEletronico):
    def calcular_pontos(self): return int(self.peso_kg * 6)

class PontoColeta:
    def __init__(self, nome, endereco):
        self.nome, self.endereco = nome, endereco
        self.entregas = []
    def receber_residuo(self, entrega): self.entregas.append(entrega)

class Entrega:
    proximo_codigo = 1
    def __init__(self, cidadao, operador, residuo, ponto):
        self.codigo = Entrega.proximo_codigo; Entrega.proximo_codigo += 1
        self.cidadao, self.operador, self.residuo, self.ponto = cidadao, operador, residuo, ponto
        self.pontos = residuo.calcular_pontos()
        self.status = "Validada"
        cidadao.adicionar_pontos(self.pontos)
        ponto.receber_residuo(self)

class SistemaEcoPonto:
    def __init__(self): self.entregas = []
    def registrar_entrega(self, cidadao, operador, residuo, ponto):
        entrega = Entrega(cidadao, operador, residuo, ponto); self.entregas.append(entrega); return entrega
    def consultar_historico(self, cidadao):
        return [e for e in self.entregas if e.cidadao is cidadao]

def demonstracao():
    sistema = SistemaEcoPonto()
    cidadao = Cidadao("Beatriz", "bia@exemplo.com")
    operador = Operador("Rafael", "rafael@ecoponto.org", "OP-12")
    ponto = PontoColeta("EcoPonto Central", "Av. Principal, 100")
    residuos = [PequenoEletronico("Celular", 0.5), GrandeEletronico("Monitor", 4)]
    print("=== ECOPONTO ===")
    print("Ação do cidadão:", cidadao.acao_principal())
    for residuo in residuos:
        entrega = sistema.registrar_entrega(cidadao, operador, residuo, ponto)
        print(f"Entrega #{entrega.codigo}: {residuo.tipo}, {residuo.peso_kg} kg -> {entrega.pontos} pontos")
    print("Pontos acumulados:", cidadao.saldo_pontos)
    print("Entregas no ponto:", len(ponto.entregas))

if __name__ == "__main__": demonstracao()
