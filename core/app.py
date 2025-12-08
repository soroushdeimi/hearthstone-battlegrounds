import pygame

class GameManager:

    def __init__(self, width: int, height: int, caption: str, fps: int) -> None:
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            # If mixer errors to init (continue without sound)
            pass

        self.width = width
        self.height = height
        self.caption = caption
        self.fps = fps

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.running = False
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
                return

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def run(self) -> None:
        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            self.update()

            self.screen.fill((0, 0, 0))
            self.draw()

            pygame.display.flip()

        try:
            pygame.quit()
        except Exception:
            pass

    def stop(self) -> None:
        self.running = False
