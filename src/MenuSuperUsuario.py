class MenuSuperUsuario:
    """Interface de contato com o superusuário (Admin)."""
    
    def __init__(self):
        self.logado: bool = False

    def deslogar(self) -> None:
        self.logado = False

    def encerrarVotacao(self) -> None:
        # Fluxo para encerrar votação antes do prazo
        pass

    def suResultados(self) -> None:
        # Visualização exclusiva para evitar viés de resultados
        pass