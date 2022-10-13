from cgi import test
from string import whitespace
import pygame
import random
import datetime

from setuptools import sic

# circuit bg = https://wallpaperaccess.com/full/85814.jpg
# hand palm = https://images.hdqwalls.com/wallpapers/hand-scan-blue-flames-digital-art-cn.jpg
# applause = https://static.vecteezy.com/system/resources/previews/004/652/787/large_2x/clapping-hands-different-people-applaud-isolated-on-blue-background-female-and-male-arms-congratulation-illustration-in-flat-style-vector.jpg
# fist = https://cdn.wallpaperjam.com/content/images/c0/d2/c0d27111b434a74cc0bd6d10072600ce7eab97a4.jpg 

# Base points earned for successfully completing a test
BASE_POINTS = 10

# Bonus points earned per second that the patient has left in a test
BONUS_POINTS_PER_SECOND = 1

# Tolerance for comparing to benchmark
TOLERANCE = 10

# Test suites
TEST_SUITE_1 = [
                "Curl Thumb",
                "Curl Index Finger",
                "Curl Middle Finger",
                "Curl Ring Finger",
                "Curl Pinky Finger"
               ]
TEST_SUITE_2 = [
                "Curl Thumb and Index Fingers",
                "Curl Middle and Ring Fingers",
                "Curl Index and Middle Fingers",
                "Curl Thumb and Pinky Fingers",
                "Curl Ring and Pinky Fingers"
               ]
TEST_SUITE_3 = [
                "Curl All Fingers",
                "Curl All Fingers Except for Thumb",
                "Curl Middle, Ring, and Pinky Fingers",
                "Curl Thumb, Index, and Middle Fingers",
                "Curl Index, Middle, and Ring Fingers"
               ]

SUITE_1_BENCHMARKS = {"Curl Thumb": [],
                      "Curl Index Finger": [],
                      "Curl Middle Finger": [],
                      "Curl Ring Finger": [],
                      "Curl Pinky Finger": []
                     }
SUITE_2_BENCHMARKS = {"Curl Thumb and Index Fingers": [],
                      "Curl Middle and Ring Fingers": [],
                      "Curl Index and Middle Fingers": [],
                      "Curl Thumb and Pinky Ring Fingers": [],
                      "Curl Ring and Pinky Fingers": []
                     } 

test_suites = [TEST_SUITE_2, TEST_SUITE_3]

benchmarks =  {}

def main():
    # Initializing and setting up Pygame
    pygame.init()
    pygame.font.init()
    logo = pygame.image.load("images/DIGIT_logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("The Hand Motor Function Test")

    # Setting game display resolution
    # Assuming computer resolution is at least 1920 x 1080
    screen = pygame.display.set_mode((1500, 800))

    # Displaying the title screen
    full_quit, set_benchmarks = title_screen(screen)
    if full_quit:
        return

    if set_benchmarks:
        full_quit, continue_game = benchmark_screen(screen)
        if full_quit | (not continue_game):
            return
    else:
        benchmark_file = open("Benchmarks/benchmarks_default.txt", "r")
        for line in benchmark_file:
            split_line = line.split(":")
            
            
            values = split_line[1].strip().strip('][').split(', ')

            for i in range(len(values)):
                values[i] = float(values[i])

            split_line[1] = values
            
            benchmarks[split_line[0]] = split_line[1]
    
    print(benchmarks)

    # Displaying the help screen
    full_quit = help_screen(screen)
    if full_quit:
        return

    # Total points counter
    points = 0

    # Cycling through all the test suites
    for test_suite in test_suites:
        # Checking if there are more test suites remaining
        if test_suite != test_suites[-1]:
            more_suites = True
        else:
            more_suites = False
        
        # Running the test suite
        full_quit, points = run_test_suite(screen, test_suite, points)    
        if full_quit:
            return
        
        # Displaying the suite complete screen
        next_suite, full_quit = suite_complete_screen(screen, more_suites)

        if full_quit:
            return

        if next_suite == False:
            break
    
    # Displaying the final screen
    final_screen(screen, points)

    return


def title_screen(screen):
    # Track if screen should be running 
    running = True

    # Setting the background
    bg = pygame.image.load("images/hand_palm.jpg")
    screen.blit(bg, (0, 0))

    logo = pygame.image.load("images/DIGIT_logo.png")
    screen.blit(logo, (-30, -30))

    # Displaying the game title
    title_font = pygame.font.Font(None, 160)
    game_title_surface = title_font.render("The Hand Motor", 1, 'green')
    screen.blit(game_title_surface, (615, 30))
    game_title_surface = title_font.render("Function Test", 1, 'green')
    screen.blit(game_title_surface, (685, 150))

    # Displaying the info on how to begin
    begin_font = pygame.font.Font(None, 100)
    begin_info = begin_font.render("Press space to begin tests", 1, 'white')
    screen.blit(begin_info, (320, 600))
    benchmark_info = begin_font.render("Press 0 to set new benchmarks", 1, 'white')
    screen.blit(benchmark_info, (240, 700))

    # Updating the full display surface
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True, False
            
            # Continue in the program if space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                return False, False
    
            # Set benchmarks if 0 is pressed
            if pygame.key.get_pressed()[pygame.K_0]:
                return False, True

    #return full_quit, set_benchmarks
    return False, False


def benchmark_screen(screen):
    running = True

    # Creating the initial display
    bg = pygame.image.load("images/hand_palm.jpg")
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 100)
        
    info_surface = font.render("Each task will be displayed one by one", 1, 'white')
    screen.blit(info_surface, (105, 50))
    info_surface = font.render("Press SPACE to capture current hand data", 1, 'white')
    screen.blit(info_surface, (40, 170))
    
    font = pygame.font.Font(None, 150)
    info_surface = font.render("Press SPACE to start", 1, 'green')
    screen.blit(info_surface, (220, 650))

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True, False
            
            # Continue in the program if space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                running = False
   
    benchmark_file = open("Benchmarks/benchmarks.txt" + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')), "a")
    
    # Going through every test suite
    for suite_num in range(2):
        # Going through every task in the suite
        for task in test_suites[suite_num]:
            running = True
            while running:
                screen.blit(bg, (0, 0))

                # Displaying the task
                font = pygame.font.Font(None, 100)
                task_surface = font.render("Task: ", 1, 'white')
                screen.blit(task_surface, (650, 150))
                task_surface = font.render(task, 1, 'white')
                screen.blit(task_surface, (20, 300))

                # Displaying how to record data
                capture_surface = font.render("Press SPACE to record data", 1, 'white')
                screen.blit(capture_surface, (300, 700))

                # Updating the full display surface
                pygame.display.flip()

                for event in pygame.event.get():
                    # Quit the program if the window is closed
                    if event.type == pygame.QUIT:
                        return True, False

                    # Capture data by clicking SPACE
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        data = [0.0, 1.0, 2.0, 3.0, 4.0]
                        benchmarks[task] = data
                        benchmark_file.write("" + task + ": " + str(data) + "\n")
                        running = False
                        break
    
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 150)
        
    continue_surface = font.render("Press SPACE to", 1, 'white')
    screen.blit(continue_surface, (350, 100))
    continue_surface = font.render("proceed with testing", 1, 'white')
    screen.blit(continue_surface, (250, 250))

    quit_surface = font.render("Otherwise, press", 1, 'white')
    screen.blit(quit_surface, (300, 450))
    quit_surface = font.render("0 to exit game", 1, 'white')
    screen.blit(quit_surface, (375, 600))

    # Updating the full display surface
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True, False

            # Proceed to game by clicking SPACE
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                return False, True
            
            # Quit game by clicking SPACE
            if pygame.key.get_pressed()[pygame.K_0]:
                return False, False
                
    # return full_quit, continue_game
    return False, True


def help_screen(screen):
    # Track if screen should be running 
    running = True
    
    # Setting the background
    bg = pygame.image.load("images/hand_palm.jpg")
    screen.blit(bg, (0, 0))

    # Displaying the info on how to begin
    help_font = pygame.font.Font(None, 75)
    continue_font = pygame.font.Font(None, 150)
    game_info1 = "This game is divided into multiple test suites."
    game_info2 = "After each suite, you'll be asked whether you'd like to"
    game_info3 = "move on or quit."
    game_info4 = "Points are earned through successfully completing tests."
    game_info5 = "Bonus points are earned by completing tests faster."
    
    help_info = help_font.render(game_info1, 1, 'white')
    screen.blit(help_info, (170, 50))

    help_info = help_font.render(game_info2, 1, 'white')
    screen.blit(help_info, (100, 150))

    help_info = help_font.render(game_info3, 1, 'white')
    screen.blit(help_info, (550, 210))

    help_info = help_font.render(game_info4, 1, 'white')
    screen.blit(help_info, (40, 310))

    help_info = help_font.render(game_info5, 1, 'white')
    screen.blit(help_info, (110, 410))

    continue_info = continue_font.render("Press space to continue", 1, 'green')
    screen.blit(continue_info, (150, 650))

    # Updating the full display surface
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True
            
            # Continue in the program is space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                running = False
    
    return False
       

def run_test_suite(screen, tests, points):
    # Labels for the task display screen
    for index in range(5):

        # Choosing a task at random and removing it from the list
        task = tests.pop(random.randrange(len(tests)))

        # Displaying the task countdown
        full_quit = countdown_screen(screen, index+1, task)
        if full_quit:
            return True, points

        # Displaying the task
        success, time_remaining, full_quit = task_screen(screen, index, task)    
        if full_quit:
            return True, points
        
        # If task was completed successfully, displaying the screen
        if success:
            bonus_points = int(time_remaining) *  BONUS_POINTS_PER_SECOND
            points_earned_for_task = BASE_POINTS + bonus_points
            points += points_earned_for_task
            full_quit = task_success(screen, index+1, points, points_earned_for_task, bonus_points)
            if full_quit:
                return True, points

    # Return full_quit, points
    return False, points


def countdown_screen(screen, task_number, task):
    running = True
    timer = 0
    max_time = 5

    # Setting the background
    bg = pygame.image.load("images/circuit_bg.png")
    screen.blit(bg, (0, 0))

    # Variables for screen design
    if len(task) < 20:
        font = pygame.font.Font(None, 150)    
    elif len(task) < 30:
        font = pygame.font.Font(None, 110)    
    else:
        font = pygame.font.Font(None, 90)    
        
    print(len(task))
    font_b = pygame.font.Font(None, 150)

    while running and timer < max_time:
        # Setting the background
        screen.blit(bg, (0, 0))     

        # Displaying the task
        text_surface = font.render("Task " + str(task_number) + ": " + task, 1, 'green')
        screen.blit(text_surface, (25, 150))   

        # Displaying the countdown text
        text_surface = font_b.render("Testing beginning in " + str(max_time-int(timer)), 1, 'white')
        screen.blit(text_surface, (200, 500))

        text_surface = font_b.render("Get Ready", 1, 'white')
        screen.blit(text_surface, (500, 650))

        # Updating the full display surface
        pygame.display.flip()

        pygame.time.delay(100)
        timer += 0.1

        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True
            
            # Skip screen by clicking 9
            if pygame.key.get_pressed()[pygame.K_9]:
                return False

    return False


def task_screen(screen, task_number, task):
    running = True
    timer = 0
    max_time = 8

    bg = pygame.image.load("images/circuit_bg.png")
    header_font = pygame.font.Font(None, 100)
    
    # Variables for screen design
    if len(task) < 20:
        task_font = pygame.font.Font(None, 150)    
    elif len(task) < 30:
        task_font = pygame.font.Font(None, 130)    
    else:
        task_font = pygame.font.Font(None, 110)    

    while running and timer < max_time:
        # Setting the background
        screen.blit(bg, (0, 0))

        # Displaying the task number
        task_number_surface = header_font.render("Task " + str(task_number+1), 1, 'green')
        screen.blit(task_number_surface, (20, 725))
        
        # Displaying the time remaining
        time_remaining_surface = header_font.render("Time Remaining: " + str(max_time-int(timer)), 1, 'green')
        screen.blit(time_remaining_surface, (800, 725))
        

        # Displaying the task
        task_surface = task_font.render("Task: ", 1, 'green')
        screen.blit(task_surface, (650, 150))
        
        task_surface = task_font.render(task, 1, 'white')
        screen.blit(task_surface, (25, 300))

        # Updating the full display surface
        pygame.display.flip()

        pygame.time.delay(100)
        timer += 0.1

        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return False, 0, True

            # Simulate success by clicking 0
            if pygame.key.get_pressed()[pygame.K_0]:
                time_remaining = str(max_time-int(timer))
                return True, time_remaining, False

    # Return success, time_remaining, full_quit
    return False, 0, False


def benchmark_compare(screen, data, suite_number, task):
    benchmark = []
    success = True

    if suite_number == 1:
        benchmark = TEST_SUITE_1[task]
    elif suite_number ==2:
        benchmark = TEST_SUITE_2[task]
    else:
        benchmark = TEST_SUITE_3[task]
    
    for finger_num in range(5):
        if (benchmark[finger_num] - data[finger_num]) > TOLERANCE:
            success=False
            return success
    
    return success


def task_success(screen, task_num, points, points_earned_for_task, bonus_points):
    running = True
    bg = pygame.image.load("images/applause.jpg")
    screen.blit(bg, (0, -100))
    
    default_font = pygame.font.Font(None, 140)

    # Displaying task successful message
    task_success_surface = default_font.render("Task " + str(task_num) + " completed successfully!", 1, 'green')
    screen.blit(task_success_surface, (20, 30))

    # Displaying +points message
    #plus_point_surface = default_font.render("+" + str(points_earned_for_task) + " Points!", 1, 'blue')
    #screen.blit(plus_point_surface, (500, 250))

    # Displaying base points message
    plus_point_surface = default_font.render("+" + str(BASE_POINTS) + " points for completing task!", 1, 'blue')
    screen.blit(plus_point_surface, (20, 250))

    # Displaying bonus points message
    plus_point_surface = default_font.render("You earned +" + str(bonus_points) + " bonus points!", 1, 'blue')
    if bonus_points == 10:
        screen.blit(plus_point_surface, (50, 350))
    elif bonus_points > 0:
        screen.blit(plus_point_surface, (70, 350))


    # Displaying total points
    total_points_surface = default_font.render("Total Points: " + str(points), 1, 'blue')
    screen.blit(total_points_surface, (375, 500))

    # Displaying the info on how to continue
    space_info = default_font.render("Press space to continue", 1, 'green')
    screen.blit(space_info, (200, 675))

    # Updating the full display surface
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True
            
            # Continue in the program is space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                running = False
    
    return False


def suite_complete_screen(screen, more_suites):
    # Track if screen should be running 
    running = True
    
    # Setting the background
    bg = pygame.image.load("images/applause.jpg")
    screen.blit(bg, (0, -100))

    default_font = pygame.font.Font(None, 140)

    # Displaying test suite complete message
    suite_complete_surface = default_font.render("Good job! Test suite complete!", 1, 'green')
    screen.blit(suite_complete_surface, (35, 50))

    # If there are more test suites
    if more_suites:
        # Displaying test suite complete message
        next_suite_1 = default_font.render("If you would like to move on to", 1, 'blue')
        next_suite_2 = default_font.render("the next suite, press SPACE", 1, 'blue')
        next_suite_3 = default_font.render("Otherwise, press 0", 1, 'blue')
        screen.blit(next_suite_1, (40, 325))    
        screen.blit(next_suite_2, (90, 425))    
        screen.blit(next_suite_3, (300, 625))

    # If this is the last test suite
    else:
        continue_surface = default_font.render("Press 0 to continue", 1, 'blue')
        screen.blit(continue_surface, (300, 500))    

    # Updating the full display surface
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return False, True
            
            # Continue in the program is space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                return True, False

            if pygame.key.get_pressed()[pygame.K_0]:
                return False, False

    # return continue_next_suite, full_quit
    return False, False


def final_screen(screen, points):
    running = True

    bg = pygame.image.load("images/fist.jpg")
    screen.blit(bg, (0, 0))

    # Displaying tasks completed message
    tasks_completed_font = pygame.font.Font(None, 250)
    tasks_completed_surface = tasks_completed_font.render("Tasks completed", 1, 'green')
    screen.blit(tasks_completed_surface, (50, 30))

    # Displaying total points
    points_font = pygame.font.Font(None, 250)
    points_surface = points_font.render("Total Points: " + str(points), 1, 'green')
    screen.blit(points_surface, (50, 350))

    # Displaying how to quit
    space_font = pygame.font.Font(None, 125)
    space_info = space_font.render("Press space to quit", 1, 'white')
    screen.blit(space_info, (325, 700))

    # Updating the full display surface
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                running = False
            
            # Continue in the program is space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                running = False

    return False


main()
