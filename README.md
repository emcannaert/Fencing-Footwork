# Fencing Footwork: Randomized Drill Generator Application for Android

## Overview
Fencing Footwork is a mobile application for Android developed using the Kivy framework and Python. It is designed to assist fencers in practicing footwork drills by providing randomized, voice-guided instructions. The app mimics a coach calling out actions, allowing the athlete to practice reaction speeds and technique without a partner.

## Key Features
* Variable Drill Duration: Users can set the length of a training session (e.g., 30, 60, or 90 seconds).
* Adjustable Intensity: Controls for the frequency of commands, ranging from beginner speeds to high-intensity competitive intervals.
* Audio Command Synthesis: Utilizes the Plyer library and Android's Text-to-Speech (TTS) engine to announce actions in real-time.
* Dynamic Command Set: Randomizes standard fencing actions including:
    * Advance / Double Advance
    * Retreat / Double Retreat
    * Lunge
    * Advance-Lunge
    * Redouble
    * Flèche
    * Duck
* Visual Countdown: High-contrast timer display for easy viewing during active movement.

## Technical Requirements
* Python 3.10+
* Kivy 2.3.0 (Cross-platform GUI framework)
* Plyer (Hardware abstraction for Text-to-Speech)
* Buildozer (For Android deployment)

## Installation
To run the application in a local development environment:

1. Clone the repository:
   git clone [repository-url]

2. Install dependencies:
   pip install kivy plyer

3. Execute the script:
   python app/footwork_app.py

## Project Structure
* app/footwork_app.py: Contains the core application logic, timer threading, and randomized command engine.