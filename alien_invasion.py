import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvasion:
    """Classe geral para gerenciar ativos e comportamentos do jogo"""

    def __init__(self):
        """Inicializa o jogo e cria recursos do jogo"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Cria uma instância para armazenar estatísticas do jogo
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Inicializa Invasão Alienígena em um estado inativo
        self.game_active = False

        # Cria o botão Play
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Inicia o loop principal do jogo"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self.bullets.update()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Responde as teclas pressionadas e a eventos de mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    
    def _check_keydown_events(self, event):
        """Responde a teclas pressionadas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responde a teclas soltas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Cria um novo projétil e o adiciona ao grupo projéteis"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Atualiza as imagens na tela e mude para a nova tela"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Desenha o botão Play se o jogo estiver inativo
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_bullets(self):
        """Atualiza a posição dos projéteis e descarta os projéteis antigos"""
        # Atualiza as posições dos projéteis
        self.bullets.update()

        # Descarta os projéteis que desaparecem
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Responde à colisões alienígenas"""
        # Remove todos os projéteis e os alienígenas  que tenham colidido
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens:
            # Destrói os projéteis existentes e cria uma frota nova
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Cria a frota de alienígenas"""
        # Cria um alienígena e continua adicionando alienígenas
        # ate que não haja mais espaço
        # O distanciamento entre alienígenas é a largura de um alienígena 
        # de alienígena e uma altura de alienígena
        alien = Alien(self)
        alien_width, alien_heigth = alien.rect.size

        current_x, current_y = alien_width, alien_heigth
        while current_y < (self.settings.screen_height - 3 * alien_heigth):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Termina uma fileira; redefine o valor de x, e incrementa o valor de y
            current_x = alien_width
            current_y += 2 * alien_heigth

    def _create_alien(self, x_position, y_position):
        """Cria um alienígena e o posicionamento na fileira"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Verifica se a frota está na borda e, em seguida, atualiza as posições"""
        self._check_fleet_edges()
        self.aliens.update()

        # Detecta colisões entre alienígenas e espaçonaves
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Procura por alienígenas se chocando contra a parte inferior da tela
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Responde apropriadamente se algum alienígena alcançou uma borda"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Faz toda a frota descer e mudar de direção"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Responde à espaçonave sendo abatida por um alienígena"""
        if self.stats.ships_left > 0:                
            # Decrementa ships_left
            self.stats.ships_left -= 1

            # Descarta quaisquer projéteis e alienígenas restantes
            self.bullets.empty()
            self.aliens.empty()

            # Cria uma frota e centraliza a espaçonave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Verifica se algum alienígena chegou à parte inferior da tela"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Trata isso como se a espaçonave tivesse sido abatida
                self._ship_hit()
                break
    
    def _check_play_button(self, mouse_pos):
        """Inicia um jogo quando o jogo clica em Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            if self.play_button.rect.collidepoint(mouse_pos):
                # Redefine as estatísticas do jogo
                self.stats.reset_stats()
                self.game_active = True

                # Descarta quaisquer projéteis e alienígenas restantes
                self.bullets.empty()
                self.aliens.empty()

                # Cria uma frota nova e centraliza a espaçonave
                self._create_fleet()
                self.ship.center_ship()

                # Oculta o cursor do mouse
                pygame.mouse.set_visible(False)

if __name__ == '__main__':
    # Cria uma instância do jogo e execute o jogo
    ai = AlienInvasion()
    ai.run_game()