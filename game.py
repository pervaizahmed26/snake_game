import pygame
import random
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Game settings
        self.grid_size = 20
        self.grid_width = self.width // self.grid_size
        self.grid_height = self.height // self.grid_size
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.DARK_GREEN = (0, 200, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        
        # Game state
        self.reset()
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def reset(self):
        """Reset the game to initial state."""
        # Snake starts in the middle
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        
        # Food
        self.food = self.generate_food()
        
        # Game state
        self.score = 0
        self.game_over = False
        self.speed = 10  # Initial speed
        self.last_update = 0
    
    def generate_food(self):
        """Generate food at a random position."""
        while True:
            food_pos = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            if food_pos not in self.snake:
                return food_pos
    
    def handle_event(self, event):
        """Handle keyboard events for snake direction."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                self.next_direction = Direction.UP
            elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                self.next_direction = Direction.DOWN
            elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                self.next_direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                self.next_direction = Direction.RIGHT
    
    def update(self):
        """Update game state. Returns True if game over."""
        if self.game_over:
            return True
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update < 1000 // self.speed:
            return False
        
        self.last_update = current_time
        
        # Update direction
        self.direction = self.next_direction
        
        # Get new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height or
            new_head in self.snake):
            self.game_over = True
            return True
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # Increase speed every 50 points
            if self.score % 50 == 0:
                self.speed = min(self.speed + 2, 20)
        else:
            self.snake.pop()
        
        return False
    
    def render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw grid (optional - for debugging)
        # self.draw_grid()
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            color = self.GREEN if i == 0 else self.DARK_GREEN
            self.draw_rect(segment, color)
        
        # Draw food
        self.draw_rect(self.food, self.RED)
        
        # Draw score
        self.draw_score()
    
    def draw_rect(self, pos, color):
        """Draw a rectangle at grid position."""
        x, y = pos
        rect = pygame.Rect(
            x * self.grid_size,
            y * self.grid_size,
            self.grid_size,
            self.grid_size
        )
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.BLACK, rect, 1)  # Border
    
    def draw_grid(self):
        """Draw grid lines (for debugging)."""
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.screen, self.GRAY, (0, y), (self.width, y))
    
    def draw_score(self):
        """Draw the score on screen."""
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def render_game_over(self):
        """Render game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font.render("GAME OVER", True, self.RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, self.WHITE)
        restart_text = self.small_font.render("Press SPACE to restart or ENTER for menu", True, self.WHITE)
        
        # Center text
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect) 