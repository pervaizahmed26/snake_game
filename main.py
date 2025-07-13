import pygame
import sys
from game import SnakeGame, GameMode
from menu import Menu

def main():
    """Main function to run the snake game."""
    pygame.init()
    
    # Set up display
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Enhanced Snake Game")
    
    # Initialize game objects
    game = SnakeGame(screen)
    menu = Menu(screen)
    
    # Game state
    current_state = "menu"  # "menu", "game", "game_over"
    
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if current_state == "menu":
                action, mode = menu.handle_event(event)
                if action == "start_game":
                    current_state = "game"
                    game.set_game_mode(mode)
                    game.reset()
                elif action == "quit":
                    running = False
            
            elif current_state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = "menu"
                    else:
                        game.handle_event(event)
            
            elif current_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        current_state = "menu"
                    elif event.key == pygame.K_SPACE:
                        current_state = "game"
                        game.reset()
        
        # Update and render based on current state
        if current_state == "menu":
            menu.update()
            menu.render()
        
        elif current_state == "game":
            game_over = game.update()
            game.render()
            if game_over:
                current_state = "game_over"
        
        elif current_state == "game_over":
            game.render()
            game.render_game_over()
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 