# core/game.py
import pygame
from utils.settings import *
from utils.support import *
from utils.debug import debug
from ui.ui import UI
from levels.level import Level
from core.data import Data
from pytmx.util_pygame import load_pygame
from os.path import join
import sys  # Para permitir encerramento correto do jogo

class Game:
    def __init__(self):
        # Inicializa o Pygame e configura o jogo
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("The Empytiness Machine")
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)


        # Carrega os mapas
        self.tmx_maps = {
            0: load_pygame(join('assets', 'data', 'levels', 'omni.tmx'))
        }
        # Configura o nível inicial
        self.current_stage = Level(self.tmx_maps[0], self.level_frames, self.data)
        self.current_stage.setup_stage_func(self.switch_stage)
        self.current_stage.setup_game(self)

        self.paused = False

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('assets', 'graphics', 'level', 'flag'),
            'saw': import_folder('assets', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('assets', 'graphics','enemies', 'floor_spikes'),
			'palms': import_sub_folders('assets', 'graphics', 'level', 'palms'),
			'candle': import_folder('assets', 'graphics','level', 'candle'),
			'window': import_folder('assets', 'graphics','level', 'window'),
			'big_chain': import_folder('assets', 'graphics','level', 'big_chains'),
			'small_chain': import_folder('assets', 'graphics','level', 'small_chains'),
			'candle_light': import_folder('assets', 'graphics','level', 'candle light'),
			'player': import_sub_folders('assets', 'images','player'),
			'saw': import_folder('assets', 'graphics', 'enemies', 'saw', 'animation'),
			'saw_chain': import_image('assets',  'graphics', 'enemies', 'saw', 'saw_chain'),
			'helicopter': import_folder('assets', 'graphics', 'level', 'helicopter'),
			'boat': import_folder('assets',  'graphics', 'objects', 'boat'),
			'spike': import_image('assets',  'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
			'spike_chain': import_image('assets',  'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
			'tooth': import_folder('assets', 'graphics','enemies', 'tooth', 'run'),
			'shell': import_sub_folders('assets', 'graphics','enemies', 'shell'),
			'pearl': import_image('assets',  'graphics', 'enemies', 'bullets', 'pearl'),
			'items': import_sub_folders('assets', 'graphics', 'items'),
			'particle': import_folder('assets', 'graphics', 'effects', 'particle'),
			'water_top': import_folder('assets', 'graphics', 'level', 'water', 'top'),
			'water_body': import_image('assets', 'graphics', 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict('assets', 'graphics', 'level', 'bg', 'tiles'),
			'cloud_small': import_folder('assets', 'graphics','level', 'clouds', 'small'),
			'cloud_large': import_image('assets', 'graphics','level', 'clouds', 'large_cloud')
        }

        self.font = pygame.font.Font(join('assets', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_folder('assets', 'graphics', 'ui', 'heart'), 
			'coin':import_image('assets', 'graphics', 'ui', 'coin')
		}
        self.overworld_frames = {
			'palms': import_folder('assets', 'graphics', 'overworld', 'palm'),
			'water': import_folder('assets', 'graphics', 'overworld', 'water'),
			'path': import_folder_dict('assets', 'graphics', 'overworld', 'path'),
			'icon': import_sub_folders('assets', 'graphics', 'overworld', 'icon'),
		}

        self.audio_files = {
			'coin': pygame.mixer.Sound(join('assets', 'audio', 'coin.wav')),
			'attack': pygame.mixer.Sound(join('assets', 'audio', 'attack.wav')),
			'jump': pygame.mixer.Sound(join('assets', 'audio', 'jump.wav')), 
			'damage': pygame.mixer.Sound(join('assets', 'audio', 'damage.wav')),
			'pearl': pygame.mixer.Sound(join('assets', 'audio', 'pearl.wav')),
		}
        self.bg_music = pygame.mixer.Sound(join('assets', 'audio', 'starlight_city.mp3'))
        self.bg_music.set_volume(0.5)

    def check_game_over(self):
        if self.data.health <= 0:
            pygame.quit()
            sys.exit()

    def run(self):
        """Loop principal do jogo."""
        while True:
            delta_time = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # Passa os eventos para o puzzle quando estiver ativo
                if hasattr(self.current_stage, 'puzzle_active') and self.current_stage.puzzle_active:
                    self.current_stage.handle_puzzle_events(event)

            # Atualiza e renderiza o nível atual
            self.check_game_over()
            
            # Renderiza o jogo base primeiro
            if not self.paused:
                self.current_stage.run(delta_time)
            else:
                # Quando pausado, ainda mostra o último frame do jogo
                self.current_stage.draw_only()
            
            # Renderiza o puzzle por cima se estiver ativo
            if hasattr(self.current_stage, 'puzzle_active') and self.current_stage.puzzle_active:
                self.current_stage.run_puzzle(delta_time)
            
            self.ui.update(delta_time)
            self.ui.draw()
            pygame.display.update()

    def switch_stage(self, stage_type, level_unlock):
        """Troca o estágio atual do jogo"""
        if stage_type == 'overworld':
            # Aqui você implementaria a lógica para voltar ao overworld
            # Por enquanto, vamos apenas desativar o puzzle
            if hasattr(self.current_stage, 'puzzle_active'):
                self.current_stage.puzzle_active = False
