"""Protótipo de console: Prato Cheio (ODS 2)."""
from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome, email):
        self.nome, self.email = nome, email
    @abstractmethod
    def tipo_usuario(self): pass

class Doador(Usuario):
    def __init__(self, nome, email, estabelecimento):
        super().__init__(nome, email)
        self.estabelecimento = estabelecimento
    def tipo_usuario(self): return "Doador"
    def cadastrar_alimento(self, sistema, alimento):
        return sistema.registrar_doacao(self, alimento)

class Instituicao(Usuario):
    def __init__(self, nome, email, nome_instituicao):
        super().__init__(nome, email)
        self.nome_instituicao = nome_instituicao
    def tipo_usuario(self): return "Instituição"
    def reservar_doacao(self, sistema, codigo):
        return sistema.reservar(codigo, self)

class Alimento:
    def __init__(self, descricao, quantidade, validade):
        self.descricao = descricao
        self._quantidade = float(quantidade)
        self.validade = validade
    @property
    def quantidade(self): return self._quantidade
    def atualizar_quantidade(self, nova):
        if nova < 0: raise ValueError("Quantidade não pode ser negativa.")
        self._quantidade = float(nova)
    def esta_disponivel(self): return self._quantidade > 0

class Doacao:
    proximo_codigo = 1
    def __init__(self, doador, alimento):
        self.codigo = Doacao.proximo_codigo
        Doacao.proximo_codigo += 1
        self.doador, self.alimento = doador, alimento
        self.status = "Disponível"
        self.reservada_por = None
    def confirmar_retirada(self):
        if self.status != "Reservada":
            raise ValueError("A doação precisa estar reservada.")
        self.status = "Retirada"

class Reserva:
    def __init__(self, doacao, instituicao):
        self.doacao, self.instituicao = doacao, instituicao
        self.status = "Ativa"
    def cancelar(self):
        if self.status == "Ativa":
            self.status = "Cancelada"
            self.doacao.status = "Disponível"
            self.doacao.reservada_por = None

class SistemaPratoCheio:
    def __init__(self):
        self.doacoes, self.reservas = [], []
    def registrar_doacao(self, doador, alimento):
        doacao = Doacao(doador, alimento); self.doacoes.append(doacao); return doacao
    def listar_disponiveis(self):
        return [d for d in self.doacoes if d.status == "Disponível" and d.alimento.esta_disponivel()]
    def reservar(self, codigo, instituicao):
        doacao = next((d for d in self.doacoes if d.codigo == codigo), None)
        if not doacao or doacao.status != "Disponível":
            raise ValueError("Doação não encontrada ou indisponível.")
        doacao.status, doacao.reservada_por = "Reservada", instituicao
        reserva = Reserva(doacao, instituicao); self.reservas.append(reserva); return reserva

def demonstracao():
    sistema = SistemaPratoCheio()
    doador = Doador("Mercado Bom Preço", "contato@mercado.com", "Mercado Bom Preço")
    ong = Instituicao("Ana", "ong@exemplo.org", "ONG Esperança")
    alimento = Alimento("Cestas de frutas", 12, "30/11/2026")
    doacao = doador.cadastrar_alimento(sistema, alimento)
    print("=== PRATO CHEIO ===")
    print(f"Usuário: {doador.nome} ({doador.tipo_usuario()})")
    print(f"Doação #{doacao.codigo}: {alimento.descricao} - {alimento.quantidade} unidades")
    reserva = ong.reservar_doacao(sistema, doacao.codigo)
    print(f"Reserva realizada pela {reserva.instituicao.nome_instituicao}. Status: {doacao.status}")
    doacao.confirmar_retirada()
    print("Retirada confirmada. Status final:", doacao.status)

if __name__ == "__main__": demonstracao()
