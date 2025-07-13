# Enhanced Snake Game 🐍

An advanced Snake game built with Python and Pygame, featuring power-ups, multiple game modes, particle effects, sound effects, and much more!

## Features

### 🎮 Multiple Game Modes
- **Classic Mode**: Traditional snake gameplay with power-ups and progressive levels
- **Survival Mode**: Survive as long as possible with increasing obstacles
- **Time Attack**: Score as many points as possible in 60 seconds

### ⚡ Power-ups System
- **Speed Boost** (Yellow): Temporarily increases snake speed
- **Score Multiplier** (Magenta): Doubles points for a limited time
- **Invincibility** (Cyan): Become immune to collisions
- **Ghost Mode** (Gray): Pass through walls and obstacles
- **Double Food** (Orange): Get double points from food
- **Slow Time** (Purple): Temporarily slow down the game

### 🎨 Visual Effects
- **Particle Effects**: Explosive particles when eating food or collecting power-ups
- **Animated Menus**: Smooth transitions and hover effects
- **Glowing Effects**: Power-ups and UI elements have attractive glow effects
- **Color-coded Snake**: Snake changes color based on active power-ups

### 🔊 Audio System
- **Sound Effects**: Eating, power-ups, level progression, and game over sounds
- **Procedural Audio**: Sounds are generated programmatically using sine waves
- **Musical Chords**: Level up plays triumphant chord progressions

### 🏆 Game Progression
- **Dynamic Levels**: Obstacles and difficulty increase with progression
- **High Score System**: Persistent high scores for each game mode
- **Speed Scaling**: Game speed increases as you progress
- **Adaptive Obstacles**: Different obstacle patterns for each game mode

### 🎯 Advanced Gameplay
- **Collision System**: Smart collision detection with power-up exceptions
- **Obstacle Generation**: Procedural obstacle placement
- **Food Spawning**: Intelligent food placement avoiding obstacles
- **Power-up Spawning**: Random power-up generation with balanced timing

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. **Main Menu Controls**:
   - Click "Start Game" to begin with the selected mode
   - Click "Game Mode" to choose between Classic, Survival, or Time Attack
   - Click "High Scores" to view your best scores
   - Click "Quit" to exit

3. **In-Game Controls**:
   - **Arrow Keys**: Move the snake
   - **ESC**: Return to main menu
   - **SPACE**: Restart game (when game over)

## Game Modes Explained

### Classic Mode
- Traditional snake gameplay with modern enhancements
- Collect food to grow and increase your score
- Avoid walls, obstacles, and your own tail
- Power-ups spawn randomly to help you
- Obstacles increase with each level

### Survival Mode
- Focus on surviving as long as possible
- Obstacles continuously increase based on your score
- More challenging than Classic mode
- Perfect for testing your endurance

### Time Attack
- Race against the clock to get the highest score
- 60-second time limit
- Fewer obstacles but faster pace
- Great for quick gaming sessions

## Power-ups Guide

| Power-up | Color | Effect | Duration |
|----------|-------|--------|----------|
| Speed Boost | Yellow | +5 speed | 5 seconds |
| Score Multiplier | Magenta | 2x points | 10 seconds |
| Invincibility | Cyan | Immune to collisions | 5 seconds |
| Ghost Mode | Gray | Pass through walls | 5 seconds |
| Double Food | Orange | 2x food points | 10 seconds |
| Slow Time | Purple | -3 speed | 5 seconds |

## Scoring System

- **Basic Food**: 10 points
- **With Score Multiplier**: 20 points
- **With Double Food**: 20 points
- **Both Active**: 40 points
- **Level Progression**: Every 100 points increases level
- **Speed Increase**: Speed increases with each level

## Technical Features

- **Particle System**: Dynamic particle effects for visual feedback
- **State Management**: Clean separation between menu, game, and game-over states
- **Persistent Storage**: High scores saved to JSON file
- **Modular Design**: Separate classes for game logic, menu, and effects
- **Error Handling**: Graceful handling of audio and file system errors

## File Structure

```
snake_game/
├── main.py          # Main game loop and state management
├── game.py          # Core game logic, classes, and mechanics
├── menu.py          # Menu system and UI components
├── requirements.txt # Python dependencies
├── README.md        # This documentation
└── high_scores.json # Persistent high score storage (created automatically)
```

## Development

The game is built with a modular architecture:

- **SnakeGame Class**: Handles all game logic, physics, and rendering
- **Menu Class**: Manages menu navigation and UI
- **Particle Class**: Handles particle effects
- **PowerUp Class**: Manages power-up behavior and rendering
- **Obstacle Class**: Handles obstacle generation and collision

## Future Enhancements

Potential features for future versions:
- Multiplayer support
- Custom themes and skins
- More power-up types
- Achievement system
- Leaderboards
- Mobile controls support

## Contributing

Feel free to contribute to this project! Some areas where help would be appreciated:
- Additional power-up types
- New game modes
- Visual improvements
- Performance optimizations
- Bug fixes

## License

This project is open source and available under the MIT License.

---

Enjoy playing the Enhanced Snake Game! 🐍✨ 