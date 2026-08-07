# Universal Programming Kit (UPK)

## Overview

Universal Programming Kit (UPK) is a Python desktop application that provides a virtual programming environment for Arduino boards. It allows users to write, simulate, and execute Arduino programs without requiring physical hardware.

The project was developed to simplify embedded programming by providing an interactive code editor, virtual execution environment, and hardware simulation using a modern graphical interface.

---

## Features

- Arduino Virtual Programming Environment
- Code Editor with Syntax-Friendly Interface
- Virtual Board Selection
- Arduino Code Simulation
- LED State Simulation
- Execution Console
- User Login System
- SQLite Database Integration
- Modern GUI built using Tkinter

---

## Technologies Used

- Python
- Tkinter
- SQLite
- Pillow (PIL)
- PySerial

---

## Project Structure

```
Universal-Programming-Kit/
│
├── ui.py
├── arduino.py
├── database.py
├── firewall.py
├── ide_database.db
├── abc.jpg
└── def.jpg
```

---

## How It Works

1. Launch the application.
2. Login to the system.
3. Select the Arduino board.
4. Choose Virtual mode.
5. Connect to the virtual environment.
6. Write or paste Arduino code.
7. Click **Run**.
8. The simulator interprets supported Arduino functions and displays execution results in the output console.

---

## Example Supported Functions

- `pinMode()`
- `digitalWrite()`
- `delay()`
- `Serial.begin()`

The simulator displays the execution process and updates the virtual LED state accordingly.

---

## Screenshots

### Login Screen
(Add Screenshot Here)

### Dashboard
(Add Screenshot Here)

### Arduino Compiler
(Add Screenshot Here)

### Simulation Output
(Add Screenshot Here)

---

## Future Enhancements

- Support for additional Arduino libraries
- Multiple virtual boards
- Real Arduino hardware upload
- Enhanced syntax highlighting
- Integrated serial monitor
- Project save/load functionality

---
## Screenshots

### Login Screen
![Login](screenshots/login.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Arduino Compiler
![Compiler](screenshots/compiler.png)

### Simulation Output
![Simulation](screenshots/simulation.png)
## Author

**Alson Debbarma**

Computer Science Undergraduate

GitHub: https://github.com/alson123-bot

---

## License

This project is developed for educational and learning purposes.
