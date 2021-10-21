from levels import *
from tiles import *
from button import Button
from player import Player
from vars import *


class World:

    def __init__(self):
        # Init pygame
        os.environ['SDL_VIDEO_CENTERED'] = "1"
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(background_color)
        pygame.display.set_caption("Impossible Mode Pixel")
        pygame.display.set_icon(pygame.image.load(os.path.join(sprites_folder, 'icon.png')).convert_alpha())
        pygame.mixer.init()
        self.music_playing = False

        self.fade = pygame.Surface((width, height))
        self.fade.fill((0, 0, 0))

        self.zoom_value = 0
        self.congratulations_text = pygame.image.load(os.path.join(sprites_folder, 'congrats.png')).convert_alpha()

        self.level_nb = 0
        self.level_change = True
        self.level_parsed = False
        self.level_change_duration = 50
        self.level_change_frame_count = 25
        self.loop()

    def play_music(self):
        if self.level_nb == 0 or not self.music_playing:
            pygame.mixer.music.stop()
            self.music = os.path.join(music_folder, 'Call to Adventure.ogg')
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)
            self.music_playing = True

        if self.level_nb == len(level_order) - 1:
            pygame.mixer.music.stop()
            self.music = os.path.join(music_folder, 'Happy Boy End Theme 1.ogg')
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)

    def parse_level(self, level_data):
        del walls[:], spikes[:]
        sprites.empty()

        self.play_music()

        if self.level_nb == 0:
            buttons.append(Button((60, 60), "play"))
            buttons.append(Button((540, 60), "info"))

        row, col = 0, 0
        for rows in level_data:
            for tile in rows:
                if tile == " ":
                    col += 1
                    continue
                if tile == "W":
                    Wall(col * 40, row * 40)
                elif tile in "SsZz":
                    rot = {"S": 0, "s": 180, "Z": 90, "z": -90}
                    Spike(col * 40, row * 40, rot[tile])
                elif tile in "vhbC":
                    type = {"v": "vertical_beam", "h": "horizontal_beam", "b": "center_beam", "C": "chains"}
                    Background_tile(col * 40, row * 40, type[tile])
                elif tile == "c":
                    Background_tile(col * 40, row * 40, 'chains', True)
                elif tile == "E":
                    if self.level_nb == 0:
                        self.goal = Ending(col * 40 - 20, row * 40)
                    else:
                        self.goal = Ending(col * 40, row * 40)
                elif tile == "P":
                    self.player = Player((col * 40, row * 40))
                    self.spawn_pos = (col * 40, row * 40)

                col += 1
            row += 1
            col = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.run = False

    def fade_to_black(self, frame, framecount):
        value = frame / framecount * math.pi
        self.alpha = int(math.sin(value) * 255)
        # print(value, self.alpha)
        self.fade.set_alpha(abs(self.alpha))

    def level_change_fade(self):
        self.level_change_frame_count += 1
        self.fade_to_black(self.level_change_frame_count, self.level_change_duration)

        if self.level_change_frame_count > self.level_change_duration / 2 and not self.level_parsed:
            self.parse_level(level_order[self.level_nb])
            self.level_parsed = True

        if self.level_change_frame_count > self.level_change_duration:
            self.alpha = 255
            self.fade.set_alpha(self.alpha)
            self.level_change = False
            self.level_change_frame_count = 0

    def update_player(self):
        if not self.level_change:
            if self.is_player_finished():
                self.level_nb += 1
                self.level_nb %= len(level_order)
                self.level_change = True
                self.level_parsed = False
                return

            if self.is_player_dead():
                self.player.alive = False

            if self.player.death_frame >= self.player.death_duration:
                sprites.remove(self.player)
                self.player = Player(self.spawn_pos)
                return

            self.move_player()

        self.player.gravity(0.3)

    def move_player(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.player.move_lr(-1)
        if key[pygame.K_RIGHT]:
            self.player.move_lr(1)
        if key[pygame.K_UP]:
            self.player.jump(8.5)

    def is_player_finished(self):
        return self.goal.rect.colliderect(self.player.rect)

    def is_player_dead(self):
        for spike in spikes:
            if self.player.rect.colliderect(spike.rect):
                bottomleft = self.player.rect.collidepoint((int(spike.bottoml[0]), int(spike.bottoml[1])))
                bottomright = self.player.rect.collidepoint((int(spike.bottomr[0]), int(spike.bottomr[1])))
                midtop = self.player.rect.collidepoint((int(spike.midtop[0]), int(spike.midtop[1])))
                midleft = self.player.rect.collidepoint((int(spike.midl[0]), int(spike.midl[1])))
                midright = self.player.rect.collidepoint((int(spike.midr[0]), int(spike.midr[1])))
                if bottomleft or midtop or bottomright or midleft or midright:
                    return True
        return False

    def title_screen_buttons(self):
        for button in buttons:
            if button.start_level:
                self.level_nb += 1
                self.level_change = True
                self.level_parsed = False
            if button.show_text:
                self.screen.blit(button.text, (0, 0))

    def animate_text(self):
        self.zoom = abs(math.sin(self.zoom_value))
        self.zoom_value += 0.08
        self.congratulations = pygame.transform.smoothscale(self.congratulations_text, (int(750 * self.zoom), int(80 * self.zoom)))
        self.screen.blit(self.congratulations, (400 - int(750 * self.zoom / 2), 300 - int(80 * self.zoom / 2)))

    def draw_on_screen(self):
        sprites.update()
        sprites.draw(camera)
        self.screen.blit(camera, (0, 0))

        if self.level_change:
            self.screen.blit(self.fade, (0, 0))

        if self.level_nb == 0:
            self.title_screen_buttons()

        if self.level_nb == len(level_order) - 1 and self.level_parsed:
            self.animate_text()

        pygame.display.update()

    def loop(self):
        self.parse_level(level_order[self.level_nb])
        self.run = True
        while self.run:
            self.events()

            camera.fill(background_color)

            # Update player
            self.update_player()

            if self.level_change:
                self.level_change_fade()

            # Draw all sprites on sreen
            self.draw_on_screen()

            clock.tick(65)
            pygame.display.set_caption("Impossible Mode Pixel, fps: " + str(int(clock.get_fps())))


World()
