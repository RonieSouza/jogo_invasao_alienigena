class Settings:
    """Classe para armazenar as configurações do Jogo Invação Alienígena"""

    def __init__(self):
        """inicializa as configurações estáticas do jogo"""
        # Configurações da tela
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Configuração da espaçonave
        self.ship_limit = 3

        # Configurações do projétil
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Configuração do alienígena
        self.fleet_drop_speed = 10

        # Rapidez com que o jogo acelera
        self.speedup_scale = 1.1
        # Com que rapidez os valores dos pontos alienígenas aumentam
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """inicializa as configurações que mudam ao longo do jogo"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # fleet_direction de 1 representa a direita; -1 representa a esquerda
        self.fleet_direction = 1

        # Configurações de pontuação
        self.alien_points = 50

    def increase_speed(self):
        """Aumenta configurações de velocidade e valores dos pontos
        alienígenas"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)