"""Protótipo de console: Olho d'Água (ODS 6)."""
from abc import ABC, abstractmethod
from datetime import datetime

class Pessoa(ABC):
    def __init__(self, nome, contato):
        self.nome, self.contato = nome, contato
    @abstractmethod
    def acao_principal(self): pass

class Morador(Pessoa):
    def __init__(self, nome, contato, bairro):
        super().__init__(nome, contato); self.bairro = bairro
    def acao_principal(self): return "Registrar vazamento"

class Tecnico(Pessoa):
    def __init__(self, nome, contato, matricula):
        super().__init__(nome, contato); self.matricula = matricula
    def acao_principal(self): return "Atualizar atendimento"

class Localizacao:
    def __init__(self, rua, bairro, referencia):
        self.rua, self.bairro, self.referencia = rua, bairro, referencia
    def endereco_completo(self): return f"{self.rua}, {self.bairro} - {self.referencia}"

class HistoricoStatus:
    def __init__(self, status, observacao):
        self.status, self.data = status, datetime.now().strftime("%d/%m/%Y %H:%M")
        self.observacao = observacao
    def resumo(self): return f"{self.data}: {self.status} - {self.observacao}"

class Ocorrencia:
    proximo_protocolo = 1000
    STATUS_VALIDOS = {"Aberta", "Em atendimento", "Concluída"}
    def __init__(self, morador, localizacao, descricao):
        self.protocolo = Ocorrencia.proximo_protocolo; Ocorrencia.proximo_protocolo += 1
        self.morador, self.localizacao, self.descricao = morador, localizacao, descricao
        self._status = "Aberta"
        self.historico = [HistoricoStatus("Aberta", "Ocorrência registrada.")]
    @property
    def status(self): return self._status
    def atualizar_status(self, novo_status, observacao, tecnico):
        if novo_status not in self.STATUS_VALIDOS: raise ValueError("Status inválido.")
        self._status = novo_status
        self.historico.append(HistoricoStatus(novo_status, f"{observacao} (Técnico: {tecnico.nome})"))

class SistemaOlhoDAgua:
    def __init__(self): self.ocorrencias = []
    def abrir_ocorrencia(self, morador, local, descricao):
        ocorrencia = Ocorrencia(morador, local, descricao); self.ocorrencias.append(ocorrencia); return ocorrencia
    def consultar_protocolo(self, protocolo):
        return next((o for o in self.ocorrencias if o.protocolo == protocolo), None)

def demonstracao():
    sistema = SistemaOlhoDAgua()
    morador = Morador("Carlos", "(27) 99999-0000", "Centro")
    tecnico = Tecnico("Marina", "(27) 3333-0000", "TEC-07")
    local = Localizacao("Rua das Flores", "Centro", "próximo à praça")
    ocorrencia = sistema.abrir_ocorrencia(morador, local, "Vazamento na tubulação da calçada")
    print("=== OLHO D'ÁGUA ===")
    print("Ação do morador:", morador.acao_principal())
    print("Protocolo:", ocorrencia.protocolo, "| Local:", local.endereco_completo())
    ocorrencia.atualizar_status("Em atendimento", "Equipe enviada ao local", tecnico)
    ocorrencia.atualizar_status("Concluída", "Vazamento reparado", tecnico)
    consultada = sistema.consultar_protocolo(ocorrencia.protocolo)
    print("Status atual:", consultada.status)
    print("Histórico:")
    for item in consultada.historico: print("-", item.resumo())

if __name__ == "__main__": demonstracao()
