class MenuUsuario:
    """Interface de contato com o usuário comum."""
    
    def __init__(self):
        self.logado: bool = False

    def menuLoop(self) -> None:
        # Loop principal do menu do usuário
        pass

    def logar(self) -> None:
        # Identificação por matrícula
        pass

    def usuarioVotar(self) -> None:
        # Fluxo de exibição de opções e registro de voto
        pass

    def usuarioCriarVotacao(self) -> None:
        # Fluxo de inputs para criação de uma votação com prazo
        pass