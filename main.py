from game import *
from button import Button
pygame.display.set_caption("No Clue")


def draw_window():  # Game Logic and Display
   if Game.GAME_STATE == ScreenState.START:
      WINDOW.fill(BACKGROUND)


if __name__ == "__main__":
   clock = pygame.time.Clock()
   while True:
      clock.tick(FPS)
      Game.LEFT_MOUSE_RELEASED = False
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
         elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
             Game.LEFT_MOUSE_RELEASED = True
         elif event.type == BUTTON_COOLDOWN_EVENT:
             Game.BUTTONS_ENABLED = True
      draw_window()
      pygame.display.update()
