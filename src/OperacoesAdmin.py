from sqlalchemy.orm import Session
from models import Votacao, Voto
from LogicaMotor import LogicaMotor

class OperacoesAdmin:
    """Classe responsável pelas operações de nível superusuário."""
    
    def __init__(self, session: Session):
        self.session = session
        self.motor = LogicaMotor(session)

    def visualizarResultados(self, votacao: Votacao) -> None:
        """
        Busca os dados e apresenta os resultados parciais ou finais[cite: 4].
        Os resultados das votações devem ser visualizados em percentuais[cite: 5].
        """
        print(f"\n" + "="*40)
        print(f" RELATÓRIO DE DECISÃO: {votacao.titulo} ")
        print("="*40)
        
        opcoes = votacao.opcoes
        if not opcoes:
            print("Esta votação não possui opções cadastradas.")
            return

        # Simula um voto genérico para utilizar os métodos de contagem do motor
        for op in opcoes:
            voto_temp = Voto(votacoes_idVotacoes=votacao.idVotacoes, opcoes_idOpcoes=op.idOpcoes)
            
            # Conta votos e tira médias conforme os requisitos funcionais [cite: 4]
            quantidade = self.motor.contarVotos(voto_temp)
            percentual = self.motor.tirarMedia(voto_temp)
            
            print(f"Opção: '{op.textoOpcao}' | Votos Absolutos: {quantidade} | Percentual: {percentual}%")

        print("-" * 40)
        # Gera indicadores de consenso de grupo utilizando o Pandas na LogicaMotor [cite: 8]
        consenso = self.motor.analisarConsenso(votacao.idVotacoes)
        print(f"INDICADOR DE CONSENSO: {consenso}")
        print("=" * 40)
        
        # Nota: A integração gráfica com Streamlit/Plotly para visualização 
        # visual dos gráficos deverá consumir estes mesmos dados posteriormente.

    def encerrarVotacao(self, votacao: Votacao) -> None:
        """
        Altera o status da votação para 'ENCERRADA', preservando 
        o histórico no banco de dados.
        """
        if votacao.status == "ENCERRADA":
            print("Esta votação já se encontra encerrada.")
            return
            
        try:
            # Atualiza o status conforme a regra de negócio 
            votacao.status = "ENCERRADA"
            self.session.commit()
            print(f"A votação '{votacao.titulo}' foi encerrada antecipadamente com sucesso!")
        except Exception as e:
            self.session.rollback()
            print(f"Erro no sistema ao tentar encerrar a votação: {e}")