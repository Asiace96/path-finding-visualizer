import pygame, sys, os
from settings import FPS
from algorithms import BreadthFirstSearch
from algorithms import DepthFirstSearch
from algorithms import AStarSearch
from algorithms import GreedyBestFirstSearch
from algorithms import BiDirectionalBFS
from algorithms import BiDirectionalDFS

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, pos, groups, draw_in_center=False, font=None):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.pos = pos
        self.draw_in_center = draw_in_center
        self.set(text)
    
    def set(self, text):
        self.image = self.font.render(str(text), True, self.color)
        if self.draw_in_center:
            self.rect = self.image.get_rect(center=self.pos)
        else:
            self.rect = self.image.get_rect(topleft=self.pos)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, groups, font=None, font_size=0, text=''):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.outline = pygame.Rect(x-2, y-2, width+4, height+4)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(font, font_size)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def draw_text(self, text_color):
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def update(self):
        button_color = self.color if self.is_hovered() else 'black'
        pygame.draw.rect(self.screen, 'black', self.outline, border_radius = 15)
        pygame.draw.rect(self.screen, button_color, self.rect, border_radius = 13)
        
        if not self.text == '':
            text_color = 'black' if self.is_hovered() else 'white'
            self.draw_text(text_color)


class Menu:
    def __init__(self, clock):
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.main_image = pygame.image.load(os.path.join('assets', 'main_icon.png')).convert_alpha()
        self.font_path = os.path.join('assets', 'Ubuntu-Bold.ttf')
        self.clock = clock
        self.running = True
        self.action = None
        self.state = None

        self.text_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()


    def run(self):
        while self.running:
            self.action = None
            self.screen.fill('grey30')
            self.screen.blit(self.main_image, (self.screen_width//2,self.screen_height//3))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(1)
                
                self.run_menu(event)


            self.text_sprites.draw(self.screen)
            self.button_sprites.update()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    # Does nothing - hook for child classes to be run and implemented by
    def run_menu(self, event):
        pass



class MainMenu(Menu):
    def __init__(self, clock, num_cols):
        super().__init__(clock)
        self.buttons = [
                        Button(50,self.screen_height*0.05, 260,50, 'red', self.button_sprites, font_size=25, text='Controls'),
                        Button(50,self.screen_height*0.15, 260,50, 'red', self.button_sprites, font_size=25, text='Settings'),
                        Button(50,self.screen_height*0.7, 260,50, 'green', self.button_sprites, font_size=25, text='Breadth First Search'),
                        Button(50,self.screen_height*0.8, 260,50, 'green', self.button_sprites, font_size=25, text='Depth First Search'),
                        Button(50,self.screen_height*0.9, 260,50, 'green', self.button_sprites, font_size=25, text='A* Search'),
                        Button(400,self.screen_height*0.7, 260,50, 'green', self.button_sprites, font_size=25, text='Greedy Best First Search'),
                        Button(400,self.screen_height*0.8, 260,50, 'green', self.button_sprites, font_size=25, text='Bi-directional BFS'),
                        Button(400,self.screen_height*0.9, 260,50, 'green', self.button_sprites, font_size=25, text='Bi-directional DFS')
                        ]
        self.texts = [
                      Text('Path Finding Visualizer', 50, 'white', (self.screen_width//3,self.screen_height//3), self.text_sprites, font=self.font_path),
                      Text('By Asaf Brandwain', 30, 'white', (self.screen_width//3,self.screen_height//3 + 60), self.text_sprites, font=self.font_path)
                    ]
        
        self.num_cols = num_cols

    def run_menu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                pygame.quit()
                sys.exit(1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_hovered():
                    self.action = button.text
            if self.action == 'Controls':
                self.state = ControlMenu(self.clock)
                self.state.run()
            if self.action == 'Settings':
                self.state = SettingsMenu(self.clock)
                self.state.run()
            if self.action == 'Breadth First Search':
                self.state = BreadthFirstSearch(self.clock, self.num_cols)
                self.state.run()
            if self.action == 'Depth First Search':
                self.state = DepthFirstSearch(self.clock, self.num_cols)
                self.state.run()
            if self.action == 'A* Search':
                self.state = AStarSearch(self.clock, self.num_cols)
                self.state.run()
            if self.action == 'Greedy Best First Search':
                self.state = GreedyBestFirstSearch(self.clock, self.num_cols)
                self.state.run()
            if self.action == 'Bi-directional BFS':
                self.state = BiDirectionalBFS(self.clock, self.num_cols)
                self.state.run()
            if self.action == 'Bi-directional DFS':
                self.state = BiDirectionalDFS(self.clock, self.num_cols)
                self.state.run()
            


class ControlMenu(Menu):
    def __init__(self, clock):
        super().__init__(clock)
        self.texts = [
                    Text('Esc -      Go back / Cancel run', 22, 'white', (100,self.screen_height*0.05), self.text_sprites, draw_in_center=False, font=self.font_path),
                    Text('Enter -      Run algorithm', 22, 'white', (100,self.screen_height*0.15), self.text_sprites, draw_in_center=False, font=self.font_path),
                    Text('R -      Random barriers', 22, 'white', (100,self.screen_height*0.25), self.text_sprites, draw_in_center=False, font=self.font_path),
                    Text('C -      Clear grid', 22, 'white', (100,self.screen_height*0.35), self.text_sprites, draw_in_center=False, font=self.font_path),
                    Text('Left click -      Add start/target/barrier', 22, 'white', (100,self.screen_height*0.45), self.text_sprites, draw_in_center=False, font=self.font_path),
                    Text('Right click -      Remove start/target/barrier', 22, 'white', (100,self.screen_height*0.55), self.text_sprites, draw_in_center=False, font=self.font_path),
                    Text('Q -      Generate Maze (Recursive Division)', 22, 'white', (100,self.screen_height*0.65), self.text_sprites, draw_in_center=False, font=self.font_path),
                    Text('W -      Generate Maze (Randomized DFS)', 22, 'white', (100,self.screen_height*0.75), self.text_sprites, draw_in_center=False, font=self.font_path),
                    Text('E -      Generate Maze (Aldous Border, not recommended..)', 22, 'white', (100,self.screen_height*0.85), self.text_sprites, draw_in_center=False, font=self.font_path),
                    ]
    
    def run_menu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False


class SettingsMenu(Menu):
    def __init__(self, clock):
        super().__init__(clock)
        self.texts = [
                    Text('Resolution:', 22, 'white', (100,self.screen_height*0.05), self.text_sprites, draw_in_center=False, font=self.font_path)
                    ]


        self.buttons = [
                        Button(50,self.screen_height*0.15, 260,50, 'red', self.button_sprites, font_size=25, text='1280x720'),
                        Button(50,self.screen_height*0.25, 260,50, 'red', self.button_sprites, font_size=25, text='1400x840'),
                        Button(50,self.screen_height*0.35, 260,50, 'red', self.button_sprites, font_size=25, text='1500x900')
                        ]
        
    def run_menu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_hovered():
                    self.action = button.text
            if self.action == '1280x720':
                pygame.display.set_mode((1280,720))
                self.state = MainMenu(self.clock, 80)
                self.state.run()
            if self.action == '1400x840':
                pygame.display.set_mode((1400,840))
                self.state = MainMenu(self.clock, 100)
                self.state.run()
            if self.action == '1500x900':
                pygame.display.set_mode((1500,900))
                self.state = MainMenu(self.clock, 150)
                self.state.run()