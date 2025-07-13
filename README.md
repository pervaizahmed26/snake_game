# Snake Game

A modern, feature-rich Snake game built with Python and Pygame. Features smooth animations, beautiful UI, and engaging gameplay mechanics.

## Features

- 🎮 **Smooth Gameplay**: Responsive controls with 60 FPS gameplay
- 🎨 **Modern UI**: Beautiful animated menu with hover effects and glow animations
- 📈 **Progressive Difficulty**: Speed increases as you score more points
- 🏆 **Score System**: Track your progress with real-time scoring
- 🎯 **Collision Detection**: Precise wall and self-collision detection
- 🔄 **Game States**: Seamless transitions between menu, game, and game over screens
- ⚡ **Performance Optimized**: Efficient rendering and update loops

## Installation

1. **Clone or download the project files**
2. **Install Python** (version 3.7 or higher)
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

### Controls
- **Arrow Keys**: Move the snake
- **ESC**: Pause game and return to menu
- **SPACE**: Restart game (from game over screen)
- **ENTER**: Return to menu (from game over screen)

### Game Rules
1. Control the snake to eat the red food
2. Avoid hitting the walls or your own tail
3. Each food eaten increases your score by 10 points
4. Speed increases every 50 points
5. Try to achieve the highest score possible!

## Project Structure

```
snake_game/
├── main.py          # Main entry point and game loop
├── game.py          # Core game logic and rendering
├── menu.py          # Menu system with animations
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Running the Game

```bash
python main.py
```

## Game Features

### Menu System
- Animated background with moving snake segments
- Glowing title with dynamic effects
- Interactive buttons with hover animations
- Clear instructions and controls display

### Game Engine
- Grid-based movement system
- Random food generation
- Progressive speed scaling
- Smooth snake movement with direction buffering

### Visual Effects
- Glow effects on UI elements
- Smooth color transitions
- Animated button interactions
- Professional game over screen

## Technical Details

- **Framework**: Pygame 2.5.2
- **Resolution**: 800x600 pixels
- **Grid Size**: 20x20 pixels per cell
- **Target FPS**: 60
- **Initial Speed**: 10 moves per second
- **Max Speed**: 20 moves per second

## Customization

You can easily modify the game by editing the constants in the code:

- **Window size**: Modify `WINDOW_WIDTH` and `WINDOW_HEIGHT` in `main.py`
- **Grid size**: Change `grid_size` in the `SnakeGame` class
- **Colors**: Update color values in the respective classes
- **Speed**: Adjust `speed` and speed increment values in `game.py`

## Troubleshooting

### Common Issues

1. **"pygame module not found"**
   - Run: `pip install pygame`

2. **Game runs too fast/slow**
   - Adjust the `clock.tick(60)` value in `main.py`

3. **Window doesn't appear**
   - Make sure you're running the script from the correct directory
   - Check that all files are present

## Contributing

Feel free to enhance the game with additional features:
- Sound effects
- High score system
- Different difficulty levels
- Power-ups
- Multiplayer support

## License

This project is open source and available under the MIT License. 