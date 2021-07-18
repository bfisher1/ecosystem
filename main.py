import pygame
from world import World
from animal import Animal
from camera import Camera
from plant import *
import time

class Ecosystem:

    def __init__(self, screen):
        """ Init the game here
        """
        animal = Animal(1, 2, 'a')
        self.camera = Camera()
        self.world = World(20, 20)
        self.world.addAnimal(animal)
        self.screen = screen
        self.seedUpdateTime = 0
        pygame.font.init()
        self.systemFont = pygame.font.SysFont('Agency FB', 20)

    def draw(self, surface):
        """ Drawing code goes here
        """

        BLACK = (0, 0, 0)

        self.screen.fill(BLACK)
        blockSize = 32
        # todo, only focus on on-camera blocks
        for x in range(self.world.width):
            for y in range(self.world.height):
                self.world.drawBlock(x, y, self.screen, self.camera, self.systemFont)

        # draw info at bottom of screen
        text = 'Ticks: ' + str(self.world.ticks)
        text_width, text_height = self.systemFont.size(text)
        text_width += 20
        textBackground = pygame.Rect(0, 0, text_width, text_height)
        image = pygame.Surface((text_width, text_height))
        image.fill((0, 0, 0))
        self.screen.blit(image, textBackground)

        textsurface = self.systemFont.render(text, False, (255, 255, 255))
        self.screen.blit(textsurface, (0, 0))


        pygame.display.update()  # Or pygame.display.flip()

    def handle_input(self):
        """ Handle pygame input events
        """
        camSpeed = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.camera.y += camSpeed
                elif event.key == pygame.K_s:
                    self.camera.y -= camSpeed
                elif event.key == pygame.K_a:
                    self.camera.x += camSpeed
                elif event.key == pygame.K_d:
                    self.camera.x -= camSpeed

    def update(self, dt):
        self.world.tick()
        self.seedUpdateTime += 1
        self.world.update()
        # if self.seedUpdateTime > 20:
        #     self.seedUpdateTime = 0
        #     self.world.spreadPlant(PlantType.GRASS, .1)
        #     self.world.spreadPlant(PlantType.OAK_TREE, .04)

    def run(self):
        """ Run the game loop
        """
        clock = pygame.time.Clock()
        fps = 60
        scale = pygame.transform.scale
        self.running = True

        try:
            while self.running:
                dt = clock.tick(fps) / 1000.
                self.handle_input()
                self.update(dt)
                self.draw(temp_surface)
                #scale(temp_surface, self.screen.get_size(), self.screen)
                #pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False
            pygame.exit()

# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    global temp_surface
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    temp_surface = pygame.Surface((width / 2, height / 2)).convert()
    return screen


def main() -> None:
    pygame.init()
    pygame.font.init()
    screen = init_screen(800, 600)
    pygame.display.set_caption('Ecosystem')

    try:
        game = Ecosystem(screen)
        game.run()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()