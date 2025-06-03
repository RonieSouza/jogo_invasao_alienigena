class GameStats:
    """Rastreia as estatísticas de Invasão Alienígena"""

    def __init__(self, ai_game):
        """Inicializa as estatísticas"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Inicializa as estatísticas que podem mudar durante o jogo"""
        self.ships_left = self.settings.ship_limit