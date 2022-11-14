Author: Bobby Bose

Description:
This game serves as a user interface to be used for patient testing.
Sensor data is written to an external CSV file by LabVIEW, and then read in by the game for testing.
Points are earned through completing tasks in the game.
-Bonus points are earned based on how fast a task is completed

Operation:
To start the game, run ./main.py from the cmd line or terminal at the folder's level.
Patients have the option to set benchmarks for tasks manually, or use a default file.
The game consists of several test suites.
After each test suite is completed, patient will be asked whether they want to move on to the next suite or not.
Patients also have the option to reattempt test suites in order to score more points.
After all test suites are completed, the game will end.

Benchmarks:
A default benchmark file is provided and can be used for test comparison.
New benchmarks can be set within the game from the title screen.
-These are time stamped with the current date and time
To set a new default benchmark, rename the desired benchmark file to benchmarks_default.txt

Tasks:
Tasks are imported from files located under the /Tasks. 
Tasks in each file are put into their own test suite.
To add new tasks, simply edit the file or create a new one to make a new test suite.