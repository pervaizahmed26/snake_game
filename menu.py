import pygame
import math

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 36)
        self.hovered = False
        self.animation_time = 0
        
    def update(self, mouse_pos):
        """Update button state and animation."""
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Smooth color transition
        target_color = self.hover_color if self.hovered else self.color
        self.current_color = self.lerp_color(self.current_color, target_color, 0.1)
        
        # Animation
        if self.hovered:
            self.animation_time += 0.1
        else:
            self.animation_time = 0
    
    def lerp_color(self, color1, color2, factor):
        """Linear interpolation between two colors."""
        return tuple(int(a + (b - a) * factor) for a, b in zip(color1, color2))
    
    def render(self, screen):
        """Render the button with animation."""
        # Draw button with rounded corners effect
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        
        # Add hover effect
        if self.hovered:
            # Glow effect
            glow_rect = self.rect.inflate(10, 10)
            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            glow_color = (*self.current_color[:3], 50)
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=15)
            screen.blit(glow_surface, glow_rect)
        
        # Draw text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Add slight bounce animation on hover
        if self.hovered:
            bounce_offset = math.sin(self.animation_time * 10) * 2
            text_rect.y += bounce_offset
        
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        """Check if button was clicked."""
        return (event.type == pygame.MOUSEBUTTONDOWN and 
                event.button == 1 and 
                self.rect.collidepoint(event.pos))

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 200, 0)
        self.BLUE = (0, 100, 255)
        self.DARK_BLUE = (0, 80, 200)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 24)
        
        # Buttons
        button_width = 200
        button_height = 50
        center_x = self.width // 2 - button_width // 2
        
        self.start_button = Button(
            center_x, self.height // 2,
            button_width, button_height,
            "Start Game", self.GREEN, self.DARK_GREEN
        )
        
        self.quit_button = Button(
            center_x, self.height // 2 + 80,
            button_width, button_height,
            "Quit", self.BLUE, self.DARK_BLUE
        )
        
        # Animation variables
        self.time = 0
        self.snake_segments = []
        self.init_snake_animation()
    
    def init_snake_animation(self):
        """Initialize animated snake for background."""
        self.snake_segments = []
        for i in range(10):
            x = (i * 30) % self.width
            y = 50 + (i * 20) % 100
            self.snake_segments.append((x, y))
    
    def update(self):
        """Update menu animations."""
        self.time += 0.05
        
        # Update mouse position for buttons
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        
        # Animate background snake
        for i, (x, y) in enumerate(self.snake_segments):
            new_x = (x + 2) % (self.width + 50)
            new_y = y + math.sin(self.time + i * 0.5) * 5
            self.snake_segments[i] = (new_x, new_y)
    
    def render(self):
        """Render the menu."""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw animated background snake
        self.draw_background_snake()
        
        # Draw title with glow effect
        self.draw_title()
        
        # Draw subtitle
        subtitle_text = self.subtitle_font.render("Use arrow keys to control the snake", True, self.WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        self.start_button.render(self.screen)
        self.quit_button.render(self.screen)
        
        # Draw instructions
        instructions = [
            "Controls:",
            "Arrow Keys - Move Snake",
            "ESC - Pause/Return to Menu",
            "SPACE - Restart Game"
        ]
        
        instruction_font = pygame.font.Font(None, 20)
        for i, instruction in enumerate(instructions):
            color = self.WHITE if i == 0 else (200, 200, 200)
            text = instruction_font.render(instruction, True, color)
            text_rect = text.get_rect(center=(self.width // 2, self.height - 150 + i * 25))
            self.screen.blit(text, text_rect)
    
    def draw_background_snake(self):
        """Draw animated snake in background."""
        for i, (x, y) in enumerate(self.snake_segments):
            color = self.GREEN if i == 0 else self.DARK_GREEN
            size = 15 if i == 0 else 10
            
            # Create snake segment
            segment_rect = pygame.Rect(x - size//2, y - size//2, size, size)
            pygame.draw.rect(self.screen, color, segment_rect, border_radius=5)
            
            # Add glow effect
            glow_rect = segment_rect.inflate(4, 4)
            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            glow_color = (*color[:3], 100)
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=7)
            self.screen.blit(glow_surface, glow_rect)
    
    def draw_title(self):
        """Draw title with animated glow effect."""
        title_text = self.title_font.render("SNAKE GAME", True, self.GREEN)
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        
        # Glow effect
        glow_intensity = abs(math.sin(self.time * 2)) * 0.5 + 0.5
        glow_color = (0, int(255 * glow_intensity), 0)
        
        # Draw glow
        for offset in range(3, 0, -1):
            glow_text = self.title_font.render("SNAKE GAME", True, (*glow_color, 50))
            glow_rect = glow_text.get_rect(center=(self.width // 2 + offset, 100 + offset))
            self.screen.blit(glow_text, glow_rect)
        
        # Draw main text
        self.screen.blit(title_text, title_rect)
    
    def handle_event(self, event):
        """Handle menu events. Returns action string."""
        if self.start_button.is_clicked(event):
            return "start_game"
        elif self.quit_button.is_clicked(event):
            return "quit"
        return None 