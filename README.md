## README: Fencing Footwork Generator and Coach

This Python-based utility generates randomized fencing footwork lessons and uses text-to-speech (TTS) to act as an automated coach. It calculates movement distances based on fencer profiles and ensures all actions remain within the physical boundaries of a standard fencing piste.

---

### Features

* **Profile-Based Scaling:** Adjusts movement lengths (advance, retreat, lunge) based on fencer type (Child, Normal, Athletic).
* **Piste Boundary Logic:** Tracks fencer position in real-time to ensure the generated drill does not move the fencer off the end of the piste.
* **Customizable Intensity:** Supports five levels of pace to control the speed of actions and the frequency of commands.
* **Text-to-Speech Integration:** Utilizes the `pyttsx3` library to announce moves and handle timed pauses automatically.
* **Session Persistence:** Optionally saves generated lessons to a timestamped text file for future use.

---

### Prerequisites

* Python 3.x
* `pyttsx3` library

Install the required library via pip:
```bash
pip install pyttsx3
```

### Usage

The script is executed via the command line. You must provide the fencer type and the piste length.

#### Command Line Arguments

| Argument | Requirement | Description |
| :--- | :--- | :--- |
| --fencerType | Required | Options: child, normal, athletic. |
| --pisteLength | Required | Total length of the piste in feet. |
| --infile | Optional | Path to an existing lesson file to read. |
| --duration | Optional | Exercise length in seconds (Default: 60). |
| --pace | Optional | Speed multiplier from 1 to 5 (Default: 2). |
| --endMargin | Optional | Buffer distance from the back line in feet (Default: 8). |
| --saveExercise | Optional | Flag to save the generated drill to a text file. |
| --voice | Optional | Index of the system TTS voice to use. |

#### Example Command

To generate and run a 2-minute drill for a normal fencer on a 42-foot piste:
```
python fencing_footwork.py --fencerType normal --pisteLength 42 --duration 120 --pace 3
```
---

### File Structure

1. get_fencer_pars: Defines the physical reach of the fencer.
2. get_action_tempi: Sets the timing/rhythm of moves based on the pace setting.
3. create_lesson: Generates a randomized sequence of moves and writes them to a file.
4. read_lesson: Parses the lesson file and executes the TTS commands and time.sleep intervals.

---

### Implementation Notes

* Pace Management: Higher pace settings (4 or 5) significantly reduce the time between commands. Ensure you have adequate space.
* Voice Configuration: On macOS, higher index numbers usually correspond to more realistic, modern Siri-era voices.
* Boundary Safety: The isValidAction function prevents the generator from calling a lunge or advance if the fencer is too close to the end of the piste.
