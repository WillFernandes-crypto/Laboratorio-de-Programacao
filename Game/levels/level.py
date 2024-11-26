from utils.settings import *
from utils.sprites import *
from entities.player import *
from entities.enemies import *
from core.groups import *
from puzzles.automata_puzzle import *
from random import uniform

class Level:
    def __init__(self, tmx_map, level_frames, data):
        self.display_surface = pygame.display.get_surface()
        self.data = data

        # Level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        self.level_unlock = tmx_level_properties['level_unlock']
        if tmx_level_properties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None

        
        # Grupos
        self.all_sprites = AllSprites(
			width = tmx_map.width, 
			height = tmx_map.height,
			bg_tile = bg_tile, 
			top_limit = tmx_level_properties['top_limit'], 
			clouds = {'large': level_frames['cloud_large'], 'small': level_frames['cloud_small']},
			horizon_line = tmx_level_properties['horizon_line'])
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()
        self.pearl_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

        # Frames
        self.pearl_surf = level_frames['pearl']
        self.particle_frames = level_frames['particle']

        self.puzzle_active = False
        self.automata_puzzle = None
        self.switch_stage_func = None  # Adiciona referência para a função de troca de estágio
        self.game = None  # Referência para o objeto Game
        self.puzzle_completed = False  # Novo atributo para controlar se o puzzle foi completado

    def setup(self, tmx_map, level_frames):
        self.player = None  # Inicializa como None
        
        # Tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == "Terrain": groups.append(self.collision_sprites)
                if layer == "Platforms": groups.append(self.semi_collision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        # Objetos
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player' and self.player is None:  # Só cria se ainda não existir
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites, 
                    semi_collision_sprites = self.semi_collision_sprites,
                    frames = level_frames['player'],
                    data = self.data)
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    # frames 
                    frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    if obj.name == 'floor_spike' and obj.properties['inverted']:
                        frames = [pygame.transform.flip(frame, False, True) for frame in frames]

                    # groups 
                    groups = [self.all_sprites]
                    if obj.name in('palm_small', 'palm_large'): groups.append(self.semi_collision_sprites)
                    # if obj.name in ('saw', 'floor_spike'): groups.append(self.damage_sprites)

                    # z index
                    z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']

                    # animation speed
                    animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1,1)
                    AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)
            if obj.name == 'flag':
                self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))    

        # Objetos que se movem
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'spike':
                Spike(
                    pos = (obj.x + obj.width, obj.y + obj.height),
                    surf = level_frames['spike'],
                    radius = obj.properties['radius'],
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start_angle'],
                    end_angle = obj.properties['end_angle'],
                    groups = (self.all_sprites, self.damage_sprites))
                for radius in range(0, obj.properties['radius'], 20):
                    Spike(
                        pos = (obj.x + obj.width, obj.y + obj.height),
                        surf = level_frames['spike_chain'],
                        radius = radius,
                        speed = obj.properties['speed'],
                        start_angle = obj.properties['start_angle'],
                        end_angle = obj.properties['end_angle'],
                        groups = self.all_sprites,
                        z = Z_LAYERS['bg details'])
            else:
                frames = level_frames[obj.name]
                groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.collision_sprites)
                if obj.width > obj.height: # horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height)
                else: # vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height / 2)
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])

                if obj.name == 'saw':
                    if move_dir == 'x':
                        y = start_pos[1] - level_frames['saw_chain'].get_height() / 2
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left, right, 20):
                           Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
                    else:
                        x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
                        top, bottom = int(start_pos[1]), int(end_pos[1])
                        for y in range(top, bottom, 20):
                           Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])

        # Inimigos
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth(
                    (obj.x, obj.y), 
                    level_frames['tooth'], 
                    (self.all_sprites, self.damage_sprites, self.tooth_sprites), 
                    self.collision_sprites)
            if obj.name == 'shell':
                Shell(
                    pos = (obj.x, obj.y),
                    frames = level_frames['shell'], 
                    groups = (self.all_sprites, self.collision_sprites),
                    reverse = obj.properties['reverse'],
                    player = self.player,
                    create_pearl = self.create_pearl)

        # Items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, 
                 (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), 
                 level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), 
                 self.data)

        # Água
        for obj in tmx_map.get_layer_by_name('Water'):
            rows = int(obj.height / TILE_SIZE) 
            cols = int(obj.width / TILE_SIZE) 
            for row in range(rows):
                for col in range(cols):
                    x = obj.x + col * TILE_SIZE
                    y = obj.y + row * TILE_SIZE
                    if row == 0:
                        AnimatedSprite((x,y), level_frames['water_top'], self.all_sprites, Z_LAYERS['water'])
                    else:
                        Sprite((x,y), level_frames['water_body'], self.all_sprites, Z_LAYERS['water'])

    def create_pearl(self, pos, direction):
        Pearl(pos, (self.all_sprites, self.damage_sprites, self.pearl_sprites), self.pearl_surf, direction, 150)

    def pearl_collision(self):
        for sprite in self.collision_sprites:
            sprite = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)
            if sprite:
                ParticleEffectSprite(sprite[0].rect.center, self.particle_frames, self.all_sprites)

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                self.player.get_damage()
                if hasattr(sprite, 'pearl'):
                    sprite.kill()
                    ParticleEffectSprite(sprite.rect.center, self.particle_frames, self.all_sprites)

    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, 
                                                       self.item_sprites, 
                                                       True)
            if item_sprites:
                item_sprites[0].activate()
                ParticleEffectSprite(item_sprites[0].rect.center, 
                                     self.particle_frames, 
                                     self.all_sprites)
                item_sprites[0].kill()

    def attack_collision(self):
        for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites():
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.reverse()

    def check_constraint(self):
        # esqueda direita
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width

        # borda abaixo 
        if self.player.hitbox_rect.bottom > self.level_bottom:
            self.switch_stage('overworld', -1)

        # se der certo... 
        if self.player.hitbox_rect.colliderect(self.level_finish_rect):
            self.switch_stage('overworld', self.level_unlock)

    def setup_game(self, game):
        """Configura a referência para o objeto Game"""
        self.game = game
        
    def handle_puzzle_events(self, event):
        """Gerencia eventos específicos do puzzle"""
        if self.puzzle_active and self.automata_puzzle:
            self.automata_puzzle.handle_event(event)
            
    def check_flag_interaction(self):
        """Verifica interação com a bandeira apenas se o puzzle ainda não foi completado"""
        if (self.player.hitbox_rect.colliderect(self.level_finish_rect) and 
            self.player.interacting and 
            not self.puzzle_active and 
            not self.puzzle_completed):  # Verifica se o puzzle já foi completado
            self.puzzle_active = True
            self.automata_puzzle = AutomataPuzzle()
            if self.game:
                self.game.paused = True
                
    def setup_stage_func(self, switch_stage_func):
        """Configura a função de troca de estágio"""
        self.switch_stage_func = switch_stage_func
        
    def switch_stage(self, stage_type, level_unlock):
        """Chama a função de troca de estágio"""
        if self.switch_stage_func:
            self.switch_stage_func(stage_type, level_unlock)

    def draw_only(self):
        """Apenas renderiza o nível sem atualizações"""
        self.display_surface.fill('gray')
        self.all_sprites.draw(self.player.hitbox_rect.center, 0)  # delta_time = 0 pois não queremos animações
        
    def run_puzzle(self, delta_time):
        """Executa apenas a lógica do puzzle"""
        if self.puzzle_active and self.automata_puzzle:
            self.automata_puzzle.run(delta_time)
            
            # Só fecha o puzzle quando o ESC for pressionado
            if self.automata_puzzle.escape_pressed:
                self.puzzle_active = False
                if self.game:
                    self.game.paused = False
                # Se o puzzle foi completado, marca como concluído e avança para o próximo nível
                if self.automata_puzzle.completed:
                    self.puzzle_completed = True  # Marca o puzzle como concluído
                    self.switch_stage('overworld', self.level_unlock)
    
    def run(self, delta_time):
        """Método principal de execução do nível"""
        if not self.puzzle_active:
            self.display_surface.fill('gray')
            self.all_sprites.update(delta_time)
            self.pearl_collision()
            self.hit_collision()
            self.item_collision()
            self.attack_collision()
            self.check_flag_interaction()
            self.all_sprites.draw(self.player.hitbox_rect.center, delta_time)