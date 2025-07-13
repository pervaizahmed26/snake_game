import pygame
import random
import math
import json
import os
from enum import Enum
import numpy as np

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class PowerUpType(Enum):
    SPEED_BOOST = "speed_boost"
    SCORE_MULTIPLIER = "score_multiplier"
    INVINCIBILITY = "invincibility"
    GHOST_MODE = "ghost_mode"
    DOUBLE_FOOD = "double_food"
    SLOW_TIME = "slow_time"

class GameMode(Enum):
    CLASSIC = "classic"
    SURVIVAL = "survival"
    TIME_ATTACK = "time_attack"

class Particle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifetime -= 1
        self.velocity = (self.velocity[0] * 0.95, self.velocity[1] * 0.95)
        return self.lifetime > 0
    
    def render(self, screen):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color, alpha)
        size = int(self.size * (self.lifetime / self.max_lifetime))
        if size > 0:
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (size, size), size)
            screen.blit(surf, (self.x - size, self.y - size))

class PowerUp:
    def __init__(self, pos, power_type):
        self.pos = pos
        self.type = power_type
        self.animation_time = 0
        self.lifetime = 300  # 5 seconds at 60 FPS
        
        # Power-up colors
        self.colors = {
            PowerUpType.SPEED_BOOST: (255, 255, 0),      # Yellow
            PowerUpType.SCORE_MULTIPLIER: (255, 0, 255),  # Magenta
            PowerUpType.INVINCIBILITY: (0, 255, 255),     # Cyan
            PowerUpType.GHOST_MODE: (128, 128, 128),      # Gray
            PowerUpType.DOUBLE_FOOD: (255, 128, 0),       # Orange
            PowerUpType.SLOW_TIME: (128, 0, 255)          # Purple
        }
    
    def update(self):
        self.animation_time += 0.2
        self.lifetime -= 1
        return self.lifetime > 0
    
    def render(self, screen, grid_size):
        x, y = self.pos
        color = self.colors[self.type]
        
        # Pulsing effect
        pulse = abs(math.sin(self.animation_time)) * 0.3 + 0.7
        size = int(grid_size * pulse)
        
        # Draw power-up
        rect = pygame.Rect(
            x * grid_size + (grid_size - size) // 2,
            y * grid_size + (grid_size - size) // 2,
            size, size
        )
        pygame.draw.rect(screen, color, rect, border_radius=size // 4)
        
        # Draw glow effect
        glow_size = int(size * 1.5)
        glow_rect = pygame.Rect(
            x * grid_size + (grid_size - glow_size) // 2,
            y * grid_size + (grid_size - glow_size) // 2,
            glow_size, glow_size
        )
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_color = (*color, 50)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=glow_size // 4)
        screen.blit(glow_surf, glow_rect)

class Obstacle:
    def __init__(self, pos):
        self.pos = pos
        self.color = (139, 69, 19)  # Brown
    
    def render(self, screen, grid_size):
        x, y = self.pos
        rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (101, 67, 33), rect, 2)  # Darker border

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
        self.GOLD = (255, 215, 0)
        
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        
        # Load sounds (create placeholder sounds if files don't exist)
        self.sounds = {}
        self.load_sounds()
        
        # Game state
        self.game_mode = GameMode.CLASSIC
        self.level = 1
        self.time_left = 60  # For time attack mode
        self.particles = []
        self.power_ups = []
        self.obstacles = []
        self.active_power_ups = {}
        self.high_scores = self.load_high_scores()
        
        self.reset()
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
    
    def load_sounds(self):
        """Load sound effects (create if they don't exist)."""
        # Create simple sound effects using pygame
        self.sounds = {}
        
        # Create eat sound (short beep)
        self.sounds['eat'] = self.create_beep_sound(440, 0.1)  # A4 note
        
        # Create power-up sound (ascending notes)
        self.sounds['power_up'] = self.create_power_up_sound()
        
        # Create game over sound (descending notes)
        self.sounds['game_over'] = self.create_game_over_sound()
        
        # Create level up sound (triumphant chord)
        self.sounds['level_up'] = self.create_level_up_sound()
    
    def create_beep_sound(self, frequency, duration):
        """Create a simple beep sound."""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2), dtype=np.int16)
            for i in range(frames):
                wave = int(4096 * math.sin(2 * math.pi * frequency * i / sample_rate))
                arr[i] = [wave, wave]
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except:
            return None
    
    def create_power_up_sound(self):
        """Create a power-up sound effect."""
        try:
            sample_rate = 22050
            duration = 0.3
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2), dtype=np.int16)
            
            # Ascending notes
            frequencies = [440, 554, 659, 880]  # A4, C#5, E5, A5
            frames_per_note = frames // len(frequencies)
            
            for freq_idx, frequency in enumerate(frequencies):
                for i in range(frames_per_note):
                    progress = i / frames_per_note
                    amplitude = 2048 * (1 - progress)  # Fade out
                    wave = int(amplitude * math.sin(2 * math.pi * frequency * (freq_idx * frames_per_note + i) / sample_rate))
                    if freq_idx * frames_per_note + i < frames:
                        arr[freq_idx * frames_per_note + i] = [wave, wave]
            
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except:
            return None
    
    def create_game_over_sound(self):
        """Create a game over sound effect."""
        try:
            sample_rate = 22050
            duration = 0.5
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2), dtype=np.int16)
            
            # Descending notes
            frequencies = [440, 370, 294, 220]  # A4, F#4, D4, A3
            frames_per_note = frames // len(frequencies)
            
            for freq_idx, frequency in enumerate(frequencies):
                for i in range(frames_per_note):
                    progress = i / frames_per_note
                    amplitude = 3072 * (1 - progress * 0.5)  # Gradual fade
                    wave = int(amplitude * math.sin(2 * math.pi * frequency * (freq_idx * frames_per_note + i) / sample_rate))
                    if freq_idx * frames_per_note + i < frames:
                        arr[freq_idx * frames_per_note + i] = [wave, wave]
            
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except:
            return None
    
    def create_level_up_sound(self):
        """Create a level up sound effect."""
        try:
            sample_rate = 22050
            duration = 0.4
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2), dtype=np.int16)
            
            # Triumphant chord progression
            chord1 = [262, 330, 392]  # C major
            chord2 = [294, 370, 440]  # D major
            
            for i in range(frames):
                progress = i / frames
                if progress < 0.5:
                    # First chord
                    wave = 0
                    for freq in chord1:
                        wave += 1024 * math.sin(2 * math.pi * freq * i / sample_rate)
                else:
                    # Second chord
                    wave = 0
                    for freq in chord2:
                        wave += 1024 * math.sin(2 * math.pi * freq * i / sample_rate)
                
                arr[i] = [int(wave), int(wave)]
            
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except:
            return None
    
    def play_sound(self, sound_name):
        """Play a sound effect."""
        try:
            if sound_name in self.sounds and self.sounds[sound_name]:
                self.sounds[sound_name].play()
        except pygame.error:
            # Ignore sound errors if audio system is not available
            pass
    
    def load_high_scores(self):
        """Load high scores from file."""
        try:
            with open('high_scores.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {mode.value: [] for mode in GameMode}
    
    def save_high_scores(self):
        """Save high scores to file."""
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)
    
    def add_high_score(self, score):
        """Add a new high score."""
        mode_scores = self.high_scores[self.game_mode.value]
        mode_scores.append(score)
        mode_scores.sort(reverse=True)
        self.high_scores[self.game_mode.value] = mode_scores[:10]  # Keep top 10
        self.save_high_scores()
    
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
        self.speed = 8  # Initial speed
        self.last_update = 0
        self.score_multiplier = 1
        
        # Clear effects
        self.particles = []
        self.power_ups = []
        self.active_power_ups = {}
        
        # Generate level obstacles
        self.generate_obstacles()
        
        # Reset time for time attack mode
        if self.game_mode == GameMode.TIME_ATTACK:
            self.time_left = 60
    
    def generate_obstacles(self):
        """Generate obstacles based on current level and game mode."""
        self.obstacles = []
        
        if self.game_mode == GameMode.SURVIVAL:
            # In survival mode, add more obstacles as score increases
            num_obstacles = min(self.score // 50, 15)
        elif self.game_mode == GameMode.CLASSIC:
            # In classic mode, add obstacles based on level
            num_obstacles = min(self.level - 1, 10) if self.level > 1 else 0
        else:
            # Time attack mode has fewer obstacles
            num_obstacles = min(self.level // 2, 5) if self.level > 2 else 0
        
        for _ in range(num_obstacles):
            attempts = 0
            while attempts < 50:  # Prevent infinite loop
                pos = (random.randint(1, self.grid_width - 2), 
                       random.randint(1, self.grid_height - 2))
                if (pos not in self.snake and pos != self.food and 
                    pos not in [obs.pos for obs in self.obstacles]):
                    self.obstacles.append(Obstacle(pos))
                    break
                attempts += 1
    
    def generate_food(self):
        """Generate food at a random position."""
        while True:
            food_pos = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            if (food_pos not in self.snake and 
                food_pos not in [obs.pos for obs in self.obstacles]):
                return food_pos
    
    def spawn_power_up(self):
        """Randomly spawn a power-up."""
        if random.random() < 0.1:  # 10% chance
            power_type = random.choice(list(PowerUpType))
            while True:
                pos = (random.randint(0, self.grid_width - 1),
                       random.randint(0, self.grid_height - 1))
                if (pos not in self.snake and pos != self.food and
                    pos not in [obs.pos for obs in self.obstacles] and
                    pos not in [pu.pos for pu in self.power_ups]):
                    self.power_ups.append(PowerUp(pos, power_type))
                    break
    
    def apply_power_up(self, power_type):
        """Apply a power-up effect."""
        self.play_sound('power_up')
        
        if power_type == PowerUpType.SPEED_BOOST:
            self.active_power_ups[power_type] = 300  # 5 seconds
            self.speed = min(self.speed + 5, 25)
        elif power_type == PowerUpType.SCORE_MULTIPLIER:
            self.active_power_ups[power_type] = 600  # 10 seconds
            self.score_multiplier = 2
        elif power_type == PowerUpType.INVINCIBILITY:
            self.active_power_ups[power_type] = 300  # 5 seconds
        elif power_type == PowerUpType.GHOST_MODE:
            self.active_power_ups[power_type] = 300  # 5 seconds
        elif power_type == PowerUpType.DOUBLE_FOOD:
            self.active_power_ups[power_type] = 600  # 10 seconds
        elif power_type == PowerUpType.SLOW_TIME:
            self.active_power_ups[power_type] = 300  # 5 seconds
            self.speed = max(self.speed - 3, 3)
    
    def update_power_ups(self):
        """Update active power-ups."""
        expired = []
        for power_type, duration in self.active_power_ups.items():
            duration -= 1
            if duration <= 0:
                expired.append(power_type)
                # Remove effects
                if power_type == PowerUpType.SPEED_BOOST:
                    self.speed = max(self.speed - 5, 8)
                elif power_type == PowerUpType.SCORE_MULTIPLIER:
                    self.score_multiplier = 1
                elif power_type == PowerUpType.SLOW_TIME:
                    self.speed = min(self.speed + 3, 20)
            else:
                self.active_power_ups[power_type] = duration
        
        for power_type in expired:
            del self.active_power_ups[power_type]
    
    def create_particles(self, pos, color, count=10):
        """Create particle effects."""
        x, y = pos
        center_x = x * self.grid_size + self.grid_size // 2
        center_y = y * self.grid_size + self.grid_size // 2
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            lifetime = random.randint(15, 30)
            self.particles.append(Particle(center_x, center_y, color, velocity, lifetime))
    
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
        
        # Update time for time attack mode
        if self.game_mode == GameMode.TIME_ATTACK:
            self.time_left -= 1/60  # Assuming 60 FPS
            if self.time_left <= 0:
                self.game_over = True
                return True
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update < 1000 // self.speed:
            # Update particles and power-ups even when snake isn't moving
            self.particles = [p for p in self.particles if p.update()]
            self.power_ups = [pu for pu in self.power_ups if pu.update()]
            self.update_power_ups()
            return False
        
        self.last_update = current_time
        
        # Update direction
        self.direction = self.next_direction
        
        # Get new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check for wall collisions (unless in ghost mode)
        if PowerUpType.GHOST_MODE not in self.active_power_ups:
            if (new_head[0] < 0 or new_head[0] >= self.grid_width or
                new_head[1] < 0 or new_head[1] >= self.grid_height):
                self.game_over = True
                self.play_sound('game_over')
                self.add_high_score(self.score)
                return True
        else:
            # Wrap around in ghost mode
            new_head = (new_head[0] % self.grid_width, new_head[1] % self.grid_height)
        
        # Check for self collision (unless invincible)
        if (PowerUpType.INVINCIBILITY not in self.active_power_ups and 
            new_head in self.snake):
            self.game_over = True
            self.play_sound('game_over')
            self.add_high_score(self.score)
            return True
        
        # Check for obstacle collision (unless invincible)
        if (PowerUpType.INVINCIBILITY not in self.active_power_ups and
            any(new_head == obs.pos for obs in self.obstacles)):
            self.game_over = True
            self.play_sound('game_over')
            self.add_high_score(self.score)
            return True
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            points = 10 * self.score_multiplier
            if PowerUpType.DOUBLE_FOOD in self.active_power_ups:
                points *= 2
            self.score += points
            self.create_particles(self.food, self.RED, 15)
            self.play_sound('eat')
            self.food = self.generate_food()
            
            # Increase speed and level
            if self.score % 100 == 0:
                self.speed = min(self.speed + 1, 25)
                self.level += 1
                self.generate_obstacles()
                self.play_sound('level_up')
            
            # Spawn power-up occasionally
            self.spawn_power_up()
        else:
            self.snake.pop()
        
        # Check for power-up collection
        for power_up in self.power_ups[:]:
            if new_head == power_up.pos:
                self.power_ups.remove(power_up)
                self.apply_power_up(power_up.type)
                self.create_particles(power_up.pos, power_up.colors[power_up.type], 20)
        
        # Update particles and power-ups
        self.particles = [p for p in self.particles if p.update()]
        self.power_ups = [pu for pu in self.power_ups if pu.update()]
        self.update_power_ups()
        
        return False
    
    def render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.render(self.screen, self.grid_size)
        
        # Draw snake with special effects
        for i, segment in enumerate(self.snake):
            if i == 0:  # Head
                color = self.GREEN
                if PowerUpType.INVINCIBILITY in self.active_power_ups:
                    color = (0, 255, 255)  # Cyan when invincible
                elif PowerUpType.GHOST_MODE in self.active_power_ups:
                    color = (128, 128, 128)  # Gray when in ghost mode
            else:  # Body
                color = self.DARK_GREEN
                if PowerUpType.INVINCIBILITY in self.active_power_ups:
                    color = (0, 200, 200)
                elif PowerUpType.GHOST_MODE in self.active_power_ups:
                    color = (100, 100, 100)
            
            self.draw_rect(segment, color)
        
        # Draw food
        self.draw_rect(self.food, self.RED)
        
        # Draw power-ups
        for power_up in self.power_ups:
            power_up.render(self.screen, self.grid_size)
        
        # Draw particles
        for particle in self.particles:
            particle.render(self.screen)
        
        # Draw HUD
        self.draw_hud()
    
    def draw_rect(self, pos, color):
        """Draw a rectangle at grid position."""
        x, y = pos
        rect = pygame.Rect(
            x * self.grid_size,
            y * self.grid_size,
            self.grid_size,
            self.grid_size
        )
        pygame.draw.rect(self.screen, color, rect, border_radius=3)
        pygame.draw.rect(self.screen, self.BLACK, rect, 1)  # Border
    
    def draw_hud(self):
        """Draw the heads-up display."""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Level
        level_text = self.font.render(f"Level: {self.level}", True, self.WHITE)
        self.screen.blit(level_text, (10, 50))
        
        # Speed
        speed_text = self.small_font.render(f"Speed: {self.speed}", True, self.WHITE)
        self.screen.blit(speed_text, (10, 90))
        
        # Game mode
        mode_text = self.small_font.render(f"Mode: {self.game_mode.value.title()}", True, self.WHITE)
        self.screen.blit(mode_text, (10, 110))
        
        # Time left for time attack mode
        if self.game_mode == GameMode.TIME_ATTACK:
            time_text = self.font.render(f"Time: {int(self.time_left)}s", True, self.WHITE)
            self.screen.blit(time_text, (self.width - 150, 10))
        
        # Score multiplier
        if self.score_multiplier > 1:
            mult_text = self.font.render(f"x{self.score_multiplier}", True, self.GOLD)
            self.screen.blit(mult_text, (self.width - 100, 50))
        
        # Active power-ups
        y_offset = 130
        for power_type in self.active_power_ups:
            duration = self.active_power_ups[power_type]
            power_text = self.small_font.render(f"{power_type.value.replace('_', ' ').title()}: {duration//60}s", True, self.WHITE)
            self.screen.blit(power_text, (10, y_offset))
            y_offset += 20
    
    def render_game_over(self):
        """Render game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.large_font.render("GAME OVER", True, self.RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, self.WHITE)
        level_text = self.font.render(f"Level Reached: {self.level}", True, self.WHITE)
        
        # High score
        mode_scores = self.high_scores[self.game_mode.value]
        if mode_scores:
            high_score_text = self.font.render(f"High Score: {mode_scores[0]}", True, self.GOLD)
        else:
            high_score_text = self.font.render("High Score: 0", True, self.GOLD)
        
        restart_text = self.small_font.render("Press SPACE to restart or ENTER for menu", True, self.WHITE)
        
        # Center text
        y_center = self.height // 2
        texts = [
            (game_over_text, y_center - 80),
            (score_text, y_center - 20),
            (level_text, y_center + 20),
            (high_score_text, y_center + 60),
            (restart_text, y_center + 120)
        ]
        
        for text, y in texts:
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
    
    def set_game_mode(self, mode):
        """Set the game mode."""
        self.game_mode = mode
        self.reset() 