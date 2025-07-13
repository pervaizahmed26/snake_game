import pygame
import math
from game import GameMode

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
        self.selected = False
        
    def update(self, mouse_pos):
        """Update button state and animation."""
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Smooth color transition
        target_color = self.hover_color if self.hovered or self.selected else self.color
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
        if self.hovered or self.selected:
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
        self.PURPLE = (128, 0, 255)
        self.DARK_PURPLE = (100, 0, 200)
        self.ORANGE = (255, 165, 0)
        self.DARK_ORANGE = (255, 140, 0)
        self.GOLD = (255, 215, 0)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Menu state
        self.current_menu = "main"  # "main", "mode_select", "high_scores"
        self.selected_mode = GameMode.CLASSIC
        
        # Buttons
        self.create_buttons()
        
        # Animation variables
        self.time = 0
        self.snake_segments = []
        self.init_snake_animation()
    
    def create_buttons(self):
        """Create all menu buttons."""
        button_width = 200
        button_height = 50
        center_x = self.width // 2 - button_width // 2
        
        # Main menu buttons
        self.start_button = Button(
            center_x, self.height // 2 - 50,
            button_width, button_height,
            "Start Game", self.GREEN, self.DARK_GREEN
        )
        
        self.mode_button = Button(
            center_x, self.height // 2 + 10,
            button_width, button_height,
            "Game Mode", self.PURPLE, self.DARK_PURPLE
        )
        
        self.scores_button = Button(
            center_x, self.height // 2 + 70,
            button_width, button_height,
            "High Scores", self.ORANGE, self.DARK_ORANGE
        )
        
        self.quit_button = Button(
            center_x, self.height // 2 + 130,
            button_width, button_height,
            "Quit", self.BLUE, self.DARK_BLUE
        )
        
        # Mode selection buttons
        mode_y = self.height // 2 - 60
        self.classic_button = Button(
            center_x, mode_y,
            button_width, button_height,
            "Classic", self.GREEN, self.DARK_GREEN
        )
        
        self.survival_button = Button(
            center_x, mode_y + 60,
            button_width, button_height,
            "Survival", self.PURPLE, self.DARK_PURPLE
        )
        
        self.time_attack_button = Button(
            center_x, mode_y + 120,
            button_width, button_height,
            "Time Attack", self.ORANGE, self.DARK_ORANGE
        )
        
        # Back button
        self.back_button = Button(
            center_x, mode_y + 180,
            button_width, button_height,
            "Back", self.BLUE, self.DARK_BLUE
        )
        
        # Update selected mode button
        self.update_selected_mode()
    
    def update_selected_mode(self):
        """Update which mode button is selected."""
        self.classic_button.selected = (self.selected_mode == GameMode.CLASSIC)
        self.survival_button.selected = (self.selected_mode == GameMode.SURVIVAL)
        self.time_attack_button.selected = (self.selected_mode == GameMode.TIME_ATTACK)
    
    def init_snake_animation(self):
        """Initialize animated snake for background."""
        self.snake_segments = []
        for i in range(15):
            x = (i * 30) % self.width
            y = 50 + (i * 20) % 100
            self.snake_segments.append((x, y))
    
    def update(self):
        """Update menu animations."""
        self.time += 0.05
        
        # Update mouse position for buttons
        mouse_pos = pygame.mouse.get_pos()
        
        if self.current_menu == "main":
            self.start_button.update(mouse_pos)
            self.mode_button.update(mouse_pos)
            self.scores_button.update(mouse_pos)
            self.quit_button.update(mouse_pos)
        elif self.current_menu == "mode_select":
            self.classic_button.update(mouse_pos)
            self.survival_button.update(mouse_pos)
            self.time_attack_button.update(mouse_pos)
            self.back_button.update(mouse_pos)
        elif self.current_menu == "high_scores":
            self.back_button.update(mouse_pos)
        
        # Animate background snake
        for i, (x, y) in enumerate(self.snake_segments):
            new_x = (x + 1.5) % (self.width + 50)
            new_y = y + math.sin(self.time + i * 0.3) * 3
            self.snake_segments[i] = (new_x, new_y)
    
    def render(self):
        """Render the menu."""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw animated background snake
        self.draw_background_snake()
        
        if self.current_menu == "main":
            self.render_main_menu()
        elif self.current_menu == "mode_select":
            self.render_mode_select()
        elif self.current_menu == "high_scores":
            self.render_high_scores()
    
    def render_main_menu(self):
        """Render the main menu."""
        # Draw title with glow effect
        self.draw_title()
        
        # Draw subtitle
        subtitle_text = self.subtitle_font.render("Enhanced Snake Game with Power-ups!", True, self.WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw current mode
        mode_text = self.small_font.render(f"Current Mode: {self.selected_mode.value.title()}", True, self.GOLD)
        mode_rect = mode_text.get_rect(center=(self.width // 2, 180))
        self.screen.blit(mode_text, mode_rect)
        
        # Draw buttons
        self.start_button.render(self.screen)
        self.mode_button.render(self.screen)
        self.scores_button.render(self.screen)
        self.quit_button.render(self.screen)
        
        # Draw instructions
        instructions = [
            "Controls:",
            "Arrow Keys - Move Snake",
            "ESC - Pause/Return to Menu",
            "SPACE - Restart Game",
            "",
            "Power-ups:",
            "Yellow - Speed Boost",
            "Magenta - Score Multiplier",
            "Cyan - Invincibility",
            "Gray - Ghost Mode",
            "Orange - Double Food",
            "Purple - Slow Time"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction == "":
                continue
            color = self.WHITE if instruction.endswith(":") else (200, 200, 200)
            text = self.small_font.render(instruction, True, color)
            text_rect = text.get_rect(center=(self.width // 2, self.height - 250 + i * 20))
            self.screen.blit(text, text_rect)
    
    def render_mode_select(self):
        """Render the mode selection menu."""
        # Title
        title_text = self.title_font.render("SELECT MODE", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Mode descriptions
        descriptions = {
            GameMode.CLASSIC: "Classic snake game with power-ups and levels",
            GameMode.SURVIVAL: "Survive as long as possible with increasing obstacles",
            GameMode.TIME_ATTACK: "Score as many points as possible in 60 seconds"
        }
        
        # Draw mode buttons
        self.classic_button.render(self.screen)
        self.survival_button.render(self.screen)
        self.time_attack_button.render(self.screen)
        self.back_button.render(self.screen)
        
        # Draw description for hovered mode
        mouse_pos = pygame.mouse.get_pos()
        if self.classic_button.rect.collidepoint(mouse_pos):
            desc = descriptions[GameMode.CLASSIC]
        elif self.survival_button.rect.collidepoint(mouse_pos):
            desc = descriptions[GameMode.SURVIVAL]
        elif self.time_attack_button.rect.collidepoint(mouse_pos):
            desc = descriptions[GameMode.TIME_ATTACK]
        else:
            desc = descriptions[self.selected_mode]
        
        desc_text = self.small_font.render(desc, True, self.WHITE)
        desc_rect = desc_text.get_rect(center=(self.width // 2, self.height - 100))
        self.screen.blit(desc_text, desc_rect)
    
    def render_high_scores(self):
        """Render the high scores menu."""
        # Title
        title_text = self.title_font.render("HIGH SCORES", True, self.GOLD)
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Load high scores (placeholder - would normally load from game)
        try:
            import json
            with open('high_scores.json', 'r') as f:
                high_scores = json.load(f)
        except:
            high_scores = {mode.value: [] for mode in GameMode}
        
        # Draw scores for each mode
        y_offset = 150
        for mode in GameMode:
            mode_text = self.subtitle_font.render(f"{mode.value.title()}:", True, self.WHITE)
            self.screen.blit(mode_text, (self.width // 2 - 100, y_offset))
            
            scores = high_scores.get(mode.value, [])
            if scores:
                top_score = str(scores[0])
            else:
                top_score = "0"
            
            score_text = self.subtitle_font.render(top_score, True, self.GOLD)
            self.screen.blit(score_text, (self.width // 2 + 50, y_offset))
            
            y_offset += 40
        
        # Draw back button
        self.back_button.render(self.screen)
    
    def draw_background_snake(self):
        """Draw animated snake in background."""
        for i, (x, y) in enumerate(self.snake_segments):
            color = self.GREEN if i == 0 else self.DARK_GREEN
            size = 12 if i == 0 else 8
            alpha = max(50, 255 - i * 15)
            
            # Create snake segment with transparency
            segment_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            segment_color = (*color, alpha)
            pygame.draw.circle(segment_surf, segment_color, (size, size), size)
            
            # Add glow effect
            glow_surf = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
            glow_color = (*color, alpha // 4)
            pygame.draw.circle(glow_surf, glow_color, (size * 1.5, size * 1.5), size * 1.5)
            
            self.screen.blit(glow_surf, (x - size * 1.5, y - size * 1.5))
            self.screen.blit(segment_surf, (x - size, y - size))
    
    def draw_title(self):
        """Draw title with animated glow effect."""
        title_text = self.title_font.render("SNAKE GAME", True, self.GREEN)
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        
        # Glow effect
        glow_intensity = abs(math.sin(self.time * 2)) * 0.5 + 0.5
        glow_color = (0, int(255 * glow_intensity), 0)
        
        # Draw glow
        for offset in range(3, 0, -1):
            glow_surf = pygame.Surface((title_rect.width + offset * 2, title_rect.height + offset * 2), pygame.SRCALPHA)
            glow_text = self.title_font.render("SNAKE GAME", True, (*glow_color, 100))
            glow_rect = glow_text.get_rect(center=(glow_surf.get_width() // 2, glow_surf.get_height() // 2))
            glow_surf.blit(glow_text, glow_rect)
            self.screen.blit(glow_surf, (title_rect.x - offset, title_rect.y - offset))
        
        # Draw main text
        self.screen.blit(title_text, title_rect)
    
    def handle_event(self, event):
        """Handle menu events. Returns action string or game mode."""
        if self.current_menu == "main":
            if self.start_button.is_clicked(event):
                return ("start_game", self.selected_mode)
            elif self.mode_button.is_clicked(event):
                self.current_menu = "mode_select"
            elif self.scores_button.is_clicked(event):
                self.current_menu = "high_scores"
            elif self.quit_button.is_clicked(event):
                return ("quit", None)
        
        elif self.current_menu == "mode_select":
            if self.classic_button.is_clicked(event):
                self.selected_mode = GameMode.CLASSIC
                self.update_selected_mode()
            elif self.survival_button.is_clicked(event):
                self.selected_mode = GameMode.SURVIVAL
                self.update_selected_mode()
            elif self.time_attack_button.is_clicked(event):
                self.selected_mode = GameMode.TIME_ATTACK
                self.update_selected_mode()
            elif self.back_button.is_clicked(event):
                self.current_menu = "main"
        
        elif self.current_menu == "high_scores":
            if self.back_button.is_clicked(event):
                self.current_menu = "main"
        
        return (None, None) 