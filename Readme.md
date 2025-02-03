# Hungry Snake Game

## Overview
Hungry Snake Game is a computer vision-based interactive game where the player controls a snake using hand gestures. The snake follows the movement of the index finger detected via a webcam. The objective is to eat randomly appearing food items, growing longer with each bite while avoiding self-collision.

## Features
- **Hand Gesture Control**: Uses OpenCV and Mediapipe to detect hand gestures.
- **Random Food Items**: The game randomly selects one of six food images to display each time the snake eats.
- **Score Tracking**: Keeps track of the current and best score.
- **Game Over Detection**: Ends the game if the snake collides with itself.
- **Real-Time Interaction**: The game updates in real-time using webcam input.

## Game Mechanics
- Move your index finger to control the snake.
- Eat the food to grow longer.
- Avoid touching your own body.
- Press 'R' to restart the game.
- Press 'Q' to quit the game.

## Installation & Setup
### Prerequisites
Ensure you have Python installed and the following dependencies:
```bash
pip install opencv-python numpy cvzone mediapipe
```

### Running the Game
Clone this repository and execute the following command:
```bash
python snake_game.py
```

## Gameplay Demonstration
Here is a demo video showcasing the gameplay:

##  Gameplay Demo
[Click here to watch the gameplay](https://github.com/Amin-mastori/Hungry-Snake-Game/raw/main/Gameplay/HungrySnake_Gameplay.mp4)

## Code Explanation
### 1. **SnakeGameClass**
- Initializes game settings, loads food images, and sets initial positions.
- Handles food spawning, movement, and collision detection.

### 2. **Game Loop**
- Captures video from the webcam.
- Detects hand and extracts the index finger position.
- Updates and renders the game state in real-time.

## Contributing
Feel free to fork this repository and submit pull requests for improvements!