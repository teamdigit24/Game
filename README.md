## Author Info
- Game developed for University of Kentucky's Fall 2022 EE/CPE 491's TEAM DIGIT 
- Code developed by Bobby Bose

## Description:
- This game serves as a user interface to be used for patient testing.
- Sensor data is written to an external CSV file by LabVIEW, and then read in by the game for testing.
- Points are earned through completing tasks in the game.
    - Bonus points are earned based on how fast a task is completed
- A set of tests have been provided in Game_tests.docx, that test that each screen functions as intended

## Operation:
- To start the game, run ./main.py from the cmd line or terminal at the folder's level.
- Patients have the option to set benchmarks for tasks manually, or use a default file.
- The game consists of several test suites.
- After each test suite is completed, patient will be asked whether they want to move on to the next suite or not.
- Patients also have the option to reattempt test suites in order to score more points.
- After all test suites are completed, the game will end.

## Data Reading:
- Sensor data is read in from a file written to by LabVIEW in real-time
- File path for data file should be edited in read_data() function

## Benchmarks:
- A default benchmark file is provided and can be used for test comparison.
- New benchmarks can be set within the game from the title screen.
    - These are time stamped with the current date and time
- To set a new default benchmark, rename the desired benchmark file to benchmarks_default.txt

## Tasks:
- Tasks are imported from files located under /Tasks. 
- Tasks in each file are put into their own test suite.
- To add new tasks, simply edit the file or create a new one to make a new test suite.
- If you want to add an image for a new or existing task, follow procedure listed under Images section

## Images:
- Sources for images used can be found under image_sources.txt
- To add an image for a new task:
    1. Add image to images/task_images/ folder
    2. In main.py, add the exact task name and image name to the hand_sign_images dict on line 16