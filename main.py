import pygame
import random
import datetime
import os

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
                "Curl Pinky Finger",
                "Move Index Finger Away From Other Fingers",
                "Move Pinky Finger Away From Other Fingers",
                "Separate Index and Middle Fingers from Pinky and Ring Fingers"
               ]
TEST_SUITE_2 = [
                "Curl Thumb and Index Fingers",
                "Curl Thumb and Middle Fingers",
                "Curl Thumb and Ring Fingers",
                "Curl Thumb and Pinky Fingers",
                "Curl Index and Middle Fingers",
                "Curl Index and Ring Fingers",
                "Curl Index and Pinky Fingers",
                "Curl Middle and Ring Fingers",
                "Curl Middle and Pinky Fingers",
                "Curl Ring and Pinky Fingers",
                "Move Index Finger Away From Other Fingers",
                "Move Pinky Finger Away From Other Fingers",
                "Separate Index and Middle Fingers from Pinky and Ring Fingers"
               ]
TEST_SUITE_3 = [
                "Make a peace sign",
                "Make a Vulcan sign",
                "Make a fist bump",
                "Make a rock and roll sign",
                "Make a thumb up sign",
                "Make a finger gun sign",
                "Make a shaka sign",
                "Make a pointer sign",
                "Move Index Finger Away From Other Fingers",
                "Move Pinky Finger Away From Other Fingers",
                "Separate Index and Middle Fingers from Pinky and Ring Fingers"
               ]

# File paths for the images for hand sign tasks
hand_signs_images = {
                     "Make a peace sign": "peace_sign.jpg",
                     "Make a Vulcan sign": "vulcan_sign.jpg",
                     "Make a fist bump": "fist_bump.png",
                     "Make a rock and roll sign": "rock_and_roll.png",
                     "Make a thumb up sign": "thumbs_up.png",
                     "Make a finger gun sign": "finger_gun.jpg",
                     "Make a shaka sign": "shaka_sign.jpg",
                     "Make a pointer sign": "pointer_sign.png"
                    }

# Test suites to use for testing
test_suites1 = [TEST_SUITE_1, TEST_SUITE_2, TEST_SUITE_3]
test_suites = []
# Dict to hold the benchmarks
benchmarks =  {}

# Light shade of button
button_color_light = (0,0,255)
# Dark shade of button
button_color_dark = (0,0,170)

# Description: Main function that controls the overall game flow
def main():
    # Initializing and setting up Pygame
    pygame.init()
    pygame.font.init()
    logo = pygame.image.load("images/DIGIT_logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("The Hand Motor Function Test")

    # Setting game display resolution
    #   Assuming computer resolution is at least 1920 x 1080
    screen = pygame.display.set_mode((1500, 800))
    
    # Import tasks from external files
    import_tasks()
    read_data()

    # Displaying the title screen
    full_quit, set_benchmarks = title_screen(screen)
    if full_quit:
        return

    # If user wants to set benchmarks
    if set_benchmarks:
        full_quit, continue_game = benchmark_screen(screen)
        if full_quit | (not continue_game):
            return
    # Otherwise, use default benchmarks
    else:
        benchmark_file = open("Benchmarks/benchmarks_default.txt", "r")
        for line in benchmark_file:
            # Doing some string parsing to get needed data
            split_line = line.split(":")
            values = split_line[1].strip().strip('][').split(', ')
            for i in range(len(values)):
                values[i] = float(values[i])
            split_line[1] = values
            benchmarks[split_line[0]] = split_line[1]
    
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
        
        # Checking if this is the test suites with hand signs
        if test_suite == TEST_SUITE_3:
            hand_signs = True
        else:
            hand_signs = False

        # Whether user wants to repeat test suite or not
        repeat = True
        while repeat == True:
            # Creating a copy of the test suite to preserve the original in case of reattempts
            test_suite_copy = test_suite.copy()
            # Running the test suite
            points_before = points
            full_quit, points = run_test_suite(screen, test_suite_copy, points, hand_signs)    
            if full_quit:
                return
            
            # Displaying the suite complete screen
            next_suite, repeat, full_quit = suite_complete_screen(screen, more_suites)
    
            if repeat:
                points = points_before

        if full_quit:
            return
        if next_suite == False:
            break
    
    # Displaying the final screen
    final_screen(screen, points)

    return


# Given: Game screen
# Returns: Whether to full quit game?, Whether to set benchmarks?
# Description: Title screen of game which user sees first 
def title_screen(screen):
    # Track if screen should be running 
    running = True

    # Position of buttons
    button_y = 425
    start_button_x = 650
    benchmark_button_x = 1000

    # Setting the background
    bg = pygame.image.load("images/hand_palm.jpg")
    screen.blit(bg, (0, 0))

    # Displaying Team DIGIT logo
    logo = pygame.image.load("images/DIGIT_logo.png")
    screen.blit(logo, (-30, -30))

    # Displaying the game title
    title_font = pygame.font.Font(None, 160)
    game_title_surface = title_font.render("The Hand Motor", 1, 'green')
    screen.blit(game_title_surface, (615, 30))
    game_title_surface = title_font.render("Function Test", 1, 'green')
    screen.blit(game_title_surface, (685, 150))

    # Keyboard presses info
    begin_font = pygame.font.Font(None, 70)
    begin_info = begin_font.render("Or Press SPACE", 1, 'green')
    screen.blit(begin_info, (605, 730))
    benchmark_info = begin_font.render("Or Press 0", 1, 'green')
    screen.blit(benchmark_info, (1090, 730))

    # Updating the full display surface
    pygame.display.flip()

    # Font for the buttons
    button_font = pygame.font.Font(None, 100)
    # Rendering text for start button
    start_button_info1 = button_font.render('Click to' , 1 , 'white')
    start_button_info2 = button_font.render('begin' , 1 , 'white')
    start_button_info3 = button_font.render('tests' , 1 , 'white')
    # Rendering text for benchmark button
    benchmark_button_info1 = button_font.render('Click to' , 1 , 'white')
    benchmark_button_info2 = button_font.render('set' , 1 , 'white')
    benchmark_button_info3 = button_font.render('benchmarks' , 1 , 'white')

    # While this screen should be running
    while running:
        # Current position of the mouse
        mouse = pygame.mouse.get_pos()

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
        
            # Checking if mouse button is being pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checking if start button is being pressed
                if start_button_x <= mouse[0] <= start_button_x+300 and button_y <= mouse[1] <= button_y+300:
                    return False, False
                # Checking if benchmark button is being pressed
                if benchmark_button_x <= mouse[0] <= benchmark_button_x+300 and button_y <= mouse[1] <= button_y+300:
                    return False, True


        # Creating start button
        if start_button_x <= mouse[0] <= start_button_x+300 and button_y <= mouse[1] <= button_y+300:
            pygame.draw.rect(screen, button_color_dark, [start_button_x,button_y,300,300])    
        else:
            pygame.draw.rect(screen, button_color_light, [start_button_x,button_y,300,300])
        
        # Creating benchmark button
        if benchmark_button_x <= mouse[0] <= benchmark_button_x+450 and button_y <= mouse[1] <= button_y+300:
            pygame.draw.rect(screen, button_color_dark, [benchmark_button_x,button_y,450,300])            
        else:
            pygame.draw.rect(screen, button_color_light, [benchmark_button_x,button_y,450,300])

        # Adding text to start button
        screen.blit(start_button_info1 , (start_button_x+25,button_y+50))
        screen.blit(start_button_info2 , (start_button_x+60,button_y+125))
        screen.blit(start_button_info3 , (start_button_x+70,button_y+200))
        
        # Adding text to benchmark button
        screen.blit(benchmark_button_info1 , (benchmark_button_x+95,button_y+50))
        screen.blit(benchmark_button_info2 , (benchmark_button_x+170,button_y+125))
        screen.blit(benchmark_button_info3 , (benchmark_button_x+10,button_y+200))

        # Updating game display
        pygame.display.update()

    # return full_quit, set_benchmarks
    return False, False


# Given: Game screen
# Returns: Whether to full quit game?, Whether to continue with game?
# Description: Title screen of game which user sees first 
def benchmark_screen(screen):
    # Track if screen should be running 
    running = True

    # Creating the initial display
    bg = pygame.image.load("images/hand_palm.jpg")
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 100)
    # Rendering instructions    
    info_surface = font.render("Each task will be displayed one by one", 1, 'white')
    screen.blit(info_surface, (105, 50))
    info_surface = font.render("Press SPACE to capture current hand data", 1, 'white')
    screen.blit(info_surface, (40, 170))

    font = pygame.font.Font(None, 150)
    info_surface = font.render("Press SPACE to start", 1, 'green')
    screen.blit(info_surface, (220, 650))

    # Updating the full display surface
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True, False
            
            # Continue in the program if space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                running = False
    
    # Create new benchmark file
    benchmark_file = open("Benchmarks/benchmarks_" + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + ".txt", "a")
    
    # Creating a dict to hold the benchmark values
    for suite_num in range(len(test_suites)):
        for task in test_suites[suite_num]:
            benchmarks[task] = []
    
    # Setting the benchmark for each task
    for task in benchmarks:
        running = True
        while running:
            screen.blit(bg, (0, 0))

            # Displaying the task
            task_word_font = pygame.font.Font(None, 150)
            task_surface = task_word_font.render("Task: ", 1, 'white')
            screen.blit(task_surface, (625, 150))

            # Determining task font size
            if len(task) < 20:
                task_font = pygame.font.Font(None, 150)    
            elif len(task) < 30:
                task_font = pygame.font.Font(None, 130)    
            elif len(task) < 60:
                task_font = pygame.font.Font(None, 90)    
            else:
                task_font = pygame.font.Font(None, 65) 
            task_surface = task_font.render(task, 1, 'white')
            screen.blit(task_surface, (20, 300))

            # Displaying how to record data
            capture_font = pygame.font.Font(None, 100)
            capture_surface = capture_font.render("Press SPACE to record data", 1, 'white')
            screen.blit(capture_surface, (300, 700))

            # Updating the full display surface
            pygame.display.flip()

            for event in pygame.event.get():
                # Quit the program if the window is closed
                if event.type == pygame.QUIT:
                    return True, False

                # Capture data by clicking SPACE
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    #data = read_data()
                    data = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
                    benchmarks[task] = data
                    benchmark_file.write("" + task + ": " + str(data) + "\n")
                    running = False
                    break
    
    # Setting the background
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 150)
    
    # Rendering font for instructions
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


# Given: None
# Returns: None 
# Description: Imports tasks from external files and creates the test suites
def import_tasks():
    # Opening all files in /Tasks folder
    for filename in os.listdir('Tasks'):
        with open(os.path.join(os.getcwd(), 'Tasks', filename), 'r') as task_file:
            suite = []
            # Adding tasks in thos file to test suites
            for task in task_file:
                suite.append(task.strip())
            test_suites.append(suite)


# Given: Game screen
# Returns: Whether to full quit game?
# Description: Help screen that displays useful instructions about game procedure
def help_screen(screen):
    # Track if screen should be running 
    running = True

    # Position of buttons
    button_y = 500
    button_x = 600
    button_wdith = 350
    button_height = 200
    
    # Setting the background
    bg = pygame.image.load("images/hand_palm.jpg")
    screen.blit(bg, (0, 0))

    # Displaying the info on how to begin
    help_font = pygame.font.Font(None, 75)
    continue_font = pygame.font.Font(None, 75)
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

    continue_info = continue_font.render("Or Press SPACE", 1, 'green')
    screen.blit(continue_info, (575, 710))

    # Updating the full display surface
    pygame.display.flip()

    # Font for button
    button_font = pygame.font.Font(None, 100)

    # Rendering text for start button
    button_info1 = button_font.render('Click to' , 1 , 'white')
    button_info2 = button_font.render('Continue' , 1 , 'white')

    while running:
        # Current position of the mouse
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True
            
            # Continue in the program is space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                running = False

             # Checking if mouse button is being pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checking if button is being pressed
                if button_x <= mouse[0] <= button_x+button_wdith and button_y <= mouse[1] <= button_y+button_height:
                    return False

        # Creating button
        if button_x <= mouse[0] <= button_x+button_wdith and button_y <= mouse[1] <= button_y+button_height:
            pygame.draw.rect(screen, button_color_dark, [button_x,button_y,button_wdith,button_height])
            
        else:
            pygame.draw.rect(screen, button_color_light, [button_x,button_y,button_wdith,button_height])

        # Adding text to start button
        screen.blit(button_info1 , (button_x+50,button_y+35))
        screen.blit(button_info2 , (button_x+20,button_y+110))

        # Updating game display
        pygame.display.update()

    # return full_quit
    return False
       

# Given: Game screen, tasks for test suite, player's current points, whether task has a hand sign
# Returns: Whether to full quit game, player's total points
# Description: Handles the running of a full test suite
def run_test_suite(screen, tests, points, hand_signs):
    # Labels for the task display screen
    for index in range(5):

        # Choosing a task at random and removing it from the list
        task = tests.pop(random.randrange(len(tests)))

        # Displaying the task countdown
        full_quit = countdown_screen(screen, index+1, task, hand_signs)
        if full_quit:
            return True, points

        # Displaying the task
        success, time_remaining, full_quit = task_screen(screen, index, task, hand_signs)    
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


# Given: Game screen, which number current task is, task to be completed, whether task has a hand sign
# Returns: Whether to full quit game?
# Description: Displays a countdown before player completes a task
def countdown_screen(screen, task_number, task, hand_signs):
    # Track if screen should be running 
    running = True
    # Current time passed
    timer = 0
    # Countdown time
    max_time = 5

    # Setting the background
    bg = pygame.image.load("images/circuit_bg.png")
    screen.blit(bg, (0, 0))

    # Variables for screen design
    if len(task) < 20:
        font = pygame.font.Font(None, 150)    
    elif len(task) < 30:
        font = pygame.font.Font(None, 130)    
    elif len(task) < 60:
        font = pygame.font.Font(None, 90)    
    else:
        font = pygame.font.Font(None, 65)   
        
    font_countdown = pygame.font.Font(None, 150)

    while running and timer < max_time:
        # Setting the background
        screen.blit(bg, (0, 0))     

        # If on test suite with hand signs, need to account for pictures
        if hand_signs and (hand_signs_images.get(task) != None):
            # Displaying task number and description
            text_surface = font.render("Task " + str(task_number) + ": " + task, 1, 'green')
            screen.blit(text_surface, (25, 25))
            # Displaying image for hand sign
            hand_sign_image = pygame.image.load("images/task_images/"+hand_signs_images.get(task))
            hand_sign_image = pygame.transform.scale(hand_sign_image, (350, 350))
            screen.blit(hand_sign_image, (575, 135))
        else:       
            # Displaying task number
            task_num_font = pygame.font.Font(None, 150)
            task_num_surface = task_num_font.render("Task " +str(task_number) + ": ", 1, 'green')
            screen.blit(task_num_surface, (615, 25))
            # Displaying task description
            text_surface = font.render(task, 1, 'green')
            screen.blit(text_surface, (25, 200))   

        # Displaying the countdown text
        text_surface = font_countdown.render("Testing beginning in " + str(max_time-int(timer)), 1, 'white')
        screen.blit(text_surface, (200, 500))

        text_surface = font_countdown.render("Get Ready", 1, 'white')
        screen.blit(text_surface, (500, 650))

        # Updating the full display surface
        pygame.display.flip()

        # Screen updates every ~100ms
        pygame.time.delay(100)
        timer += 0.1

        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True
            
            # Skip screen by clicking 9
            if pygame.key.get_pressed()[pygame.K_9]:
                return False
    
    # return full_quit
    return False


# Given: Game screen, which number current task is, task to be completed, whether task has a hand sign
# Returns: Whether task was completed successfully, time remaining when task was completed, whether to full quit game?
# Description: Displays task for patient to complete and a countdown to complete in
def task_screen(screen, task_number, task, hand_signs):
    # Track if screen should be running 
    running = True
    # Current time passed
    timer = 0
    # Countdown time
    max_time = 8

    # Loading background for screen
    bg = pygame.image.load("images/circuit_bg.png")
    # Fonts for on-screen text
    header_font = pygame.font.Font(None, 100)
    task_num_font = pygame.font.Font(None, 150)
    
    # Variables for screen design
    if len(task) < 20:
        task_font = pygame.font.Font(None, 150)    
    elif len(task) < 30:
        task_font = pygame.font.Font(None, 130)    
    elif len(task) < 60:
        task_font = pygame.font.Font(None, 90)    
    else:
        task_font = pygame.font.Font(None, 65)

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
        task_surface1 = task_num_font.render("Task: ", 1, 'green')
        task_surface2 = task_font.render(task, 1, 'white')
        
        if hand_signs and (hand_signs_images.get(task) != None):
            screen.blit(task_surface1, (650, 25))
            screen.blit(task_surface2, (25, 175))
            hand_sign_image = pygame.image.load("images/task_images/"+hand_signs_images.get(task))
            hand_sign_image = pygame.transform.scale(hand_sign_image, (350, 350))
            screen.blit(hand_sign_image, (575, 300))
        else:
            screen.blit(task_surface1, (650, 150))
            screen.blit(task_surface2, (25, 300))

        # Updating the full display surface
        pygame.display.flip()

        # Screen updates every ~100ms
        pygame.time.delay(100)
        timer += 0.1

        # Checking if current hand position data is correct
        #if benchmark_compare(task):
            #return True, time_remaining, False

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


# Given: None
# Returns: Current hand position data
# Description: Reads in the current hand position data and formats it
def read_data():
    # Read in data from file
    data_file = open("data.csv", "r")
    current_data = data_file.readlines()[-1]
    data_file.close()

    # Formatting then input data
    current_data = current_data.split(',')
    current_data.pop(0)
    for i in range(len(current_data)):
        current_data[i] = float(current_data[i])

    # Return current hand position data
    return current_data


# Given: Task to be completed
# Returns: Whether task was completed successfully
# Description: Compares current hand position data to task's benchmark
def benchmark_compare(task):
    # Read in hand position data
    data = read_data()
    # Grabbing the benchmark for this task
    benchmark = benchmarks[task]
    
    # Checking that each sensor matches benchmark
    for finger_num in range(len(benchmark)):
        # Seeing if data is within tolerance of benchmark
        if (benchmark[finger_num] - data[finger_num]) > TOLERANCE:
            return False
    
    # Return task_success
    return True


# Given: Game screen, current task number, player's total points, bonus points for completing task
# Returns: Whether to full quit game
# Description: Informs user that task was completed successfully, and how many points were earnt
def task_success(screen, task_num, points, bonus_points):
    # Track if screen should be running 
    running = True

    # Position of buttons
    button_y = 525
    button_x = 600
    button_wdith = 350
    button_height = 200

    # Setting the background
    bg = pygame.image.load("images/applause.jpg")
    screen.blit(bg, (0, -100))
    
    # Displaying task successful message
    default_font = pygame.font.Font(None, 140)
    task_success_surface = default_font.render("Task " + str(task_num) + " completed successfully!", 1, 'green')
    screen.blit(task_success_surface, (20, 30))

    # Displaying base points message
    plus_point_surface = default_font.render("+" + str(BASE_POINTS) + " points for completing task!", 1, 'blue')
    screen.blit(plus_point_surface, (20, 150))

    # Displaying bonus points message
    plus_point_surface = default_font.render("You earned +" + str(bonus_points) + " bonus points!", 1, 'blue')
    if bonus_points == 10:
        screen.blit(plus_point_surface, (50, 250))
    elif bonus_points > 0:
        screen.blit(plus_point_surface, (70, 250))


    # Displaying total points
    total_points_surface = default_font.render("Total Points: " + str(points), 1, 'blue')
    screen.blit(total_points_surface, (375, 375))

    # Displaying the info on how to continue
    continue_font = pygame.font.Font(None, 75)
    continue_info = continue_font.render("Or Press SPACE", 1, 'blue')
    screen.blit(continue_info, (575, 735))

    # Updating the full display surface
    pygame.display.flip()

    # Font for button
    button_font = pygame.font.Font(None, 100)

    # Rendering text for start button
    button_info1 = button_font.render('Click to' , 1 , 'white')
    button_info2 = button_font.render('Continue' , 1 , 'white')

    while running:
        # Current position of the mouse
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return True
            
            # Continue in the program is space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                running = False

            # Checking if mouse button is being pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checking if button is being pressed
                if button_x <= mouse[0] <= button_x+button_wdith and button_y <= mouse[1] <= button_y+button_height:
                    return False

        # Creating start button
        if button_x <= mouse[0] <= button_x+button_wdith and button_y <= mouse[1] <= button_y+button_height:
            pygame.draw.rect(screen, button_color_dark, [button_x,button_y,button_wdith,button_height])
            
        else:
            pygame.draw.rect(screen, button_color_light, [button_x,button_y,button_wdith,button_height])

        # Adding text to start button
        screen.blit(button_info1 , (button_x+50,button_y+35))
        screen.blit(button_info2 , (button_x+20,button_y+110))

        # Updating game display
        pygame.display.update()

    # Return full_quit
    return False


# Given: Game screen, whether there are more suites to complete
# Returns: Whether to move on to next suite, Whether to repeat test suite, Whether to full quit game
# Description: Informs user that suite was completed successfully, and how many points they have
def suite_complete_screen(screen, more_suites):
    # Track if screen should be running 
    running = True

    # Position of buttons
    button_x = 100
    next_suite_button_y = 150
    button_width = 1300
    button_height = 125

    # Defining positions of buttons
    if more_suites:
        repeat_suite_button_y = 370
        quit_tests_button_y = 590
    else:
        repeat_suite_button_y = 250
        quit_tests_button_y = 550
    
    # Setting the background
    bg = pygame.image.load("images/applause.jpg")
    screen.blit(bg, (0, -100))
    
    # Displaying test suite complete message
    default_font = pygame.font.Font(None, 140)
    suite_complete_surface = default_font.render("Good job! Test suite complete!", 1, 'green')
    screen.blit(suite_complete_surface, (35, 25))

    # If there are more test suites
    if more_suites:
        press_font = pygame.font.Font(None, 70)
        next_suite_info = press_font.render("Or Press SPACE", 1, 'blue')
        screen.blit(next_suite_info, (560, next_suite_button_y+button_height+10))

    # Keyboard presses info
    press_font = pygame.font.Font(None, 70)
    repeat_info = press_font.render("Or Press 9", 1, 'blue')
    screen.blit(repeat_info, (625, repeat_suite_button_y+button_height+10))
    quit_info = press_font.render("Or Press 0", 1, 'blue')
    screen.blit(quit_info, (625, quit_tests_button_y+button_height+10))

    # Updating the full display surface
    pygame.display.flip()
    
    # Rendering text for buttons
    button_font = pygame.font.Font(None, 100)
    button_info1 = button_font.render('Click to move onto next suite' , 1 , 'white')
    button_info2 = button_font.render('Click to attempt test suite again' , 1 , 'white')
    button_info3 = button_font.render('Otherwise, click here' , 1 , 'white')

    while running:
        # Current position of the mouse
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                return False, False, True
            
            # Continue in the program is space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                return True, False, False

            # Repeat test suite if 9 is pressed
            if pygame.key.get_pressed()[pygame.K_9]:
                return False, True, False

            # Move on to final screen if 0 is pressed
            if pygame.key.get_pressed()[pygame.K_0]:
                return False, False, False
            
            # Checking if mouse button is being pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if more_suites:
                    # Checking if next suite button is being pressed
                    if button_x <= mouse[0] <= button_x+button_width and next_suite_button_y <= mouse[1] <= next_suite_button_y+button_height:
                        return True, False, False
                # Checking if repeat suite button is being pressed
                if button_x <= mouse[0] <= button_x+button_width and repeat_suite_button_y <= mouse[1] <= repeat_suite_button_y+button_height:
                    return False, True, False
                # Checking if quit tests button is being pressed
                if button_x <= mouse[0] <= button_x+button_width and quit_tests_button_y <= mouse[1] <= quit_tests_button_y+button_height:
                    return False, False, False

        if more_suites:
            # Creating next suite button
            if button_x <= mouse[0] <= button_x+button_width and next_suite_button_y <= mouse[1] <= next_suite_button_y+button_height:
                pygame.draw.rect(screen, button_color_dark, [button_x,next_suite_button_y,button_width,button_height])
            else:
                pygame.draw.rect(screen, button_color_light, [button_x,next_suite_button_y,button_width,button_height])

            # Adding text to buttons
            screen.blit(button_info1 , (button_x+155,next_suite_button_y+30))

        # Creating repeat suite button
        if button_x <= mouse[0] <= button_x+button_width and repeat_suite_button_y <= mouse[1] <= repeat_suite_button_y+button_height:
            pygame.draw.rect(screen, button_color_dark, [button_x,repeat_suite_button_y,button_width,button_height])
        else:
            pygame.draw.rect(screen, button_color_light, [button_x,repeat_suite_button_y,button_width,button_height])

        # Creating quit tests button
        if button_x <= mouse[0] <= button_x+button_width and quit_tests_button_y <= mouse[1] <= quit_tests_button_y+button_height:
            pygame.draw.rect(screen, button_color_dark, [button_x,quit_tests_button_y,button_width,button_height])
        else:
            pygame.draw.rect(screen, button_color_light, [button_x,quit_tests_button_y,button_width,button_height])

        # Displaying button text
        screen.blit(button_info2 , (button_x+115,repeat_suite_button_y+30))
        screen.blit(button_info3 , (button_x+300,quit_tests_button_y+30))

        # Updating game display
        pygame.display.update()    

    # return continue_next_suite, repeat, full_quit
    return False, False, False


# Given: Game screen, player's points
# Returns: Whether to full quit game?
# Description: Final screen of the game that displays point total for player
def final_screen(screen, points):
    # Track if screen should be running 
    running = True

    # Position of buttons
    button_y = 500
    button_x = 600
    button_wdith = 350
    button_height = 200

    # Setting the background
    bg = pygame.image.load("images/fist.jpg")
    screen.blit(bg, (0, 0))

    # Displaying tasks completed message
    tasks_completed_font = pygame.font.Font(None, 250)
    tasks_completed_surface = tasks_completed_font.render("Tasks completed", 1, 'green')
    screen.blit(tasks_completed_surface, (50, 30))

    # Displaying total points
    points_font = pygame.font.Font(None, 250)
    points_surface = points_font.render("Total Points: " + str(points), 1, 'green')
    screen.blit(points_surface, (50, 250))
    
    # Displaying how to quit
    quit_font = pygame.font.Font(None, 75)
    quit_info = quit_font.render("Or Press SPACE", 1, 'blue')
    screen.blit(quit_info, (575, 710))

    # Updating the full display surface
    pygame.display.flip()

    # Font for the button
    button_font = pygame.font.Font(None, 100)

    # Rendering text for start button
    button_info1 = button_font.render('Click to' , 1 , 'white')
    button_info2 = button_font.render('Quit' , 1 , 'white')

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # Quit the program if the window is closed
            if event.type == pygame.QUIT:
                running = False
            
            # Continue in the program is space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                running = False

            # Checking if mouse button is being pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checking if button is being pressed
                if button_x <= mouse[0] <= button_x+button_wdith and button_y <= mouse[1] <= button_y+button_height:
                    return False
            
        # Creating button
        if button_x <= mouse[0] <= button_x+button_wdith and button_y <= mouse[1] <= button_y+button_height:
            pygame.draw.rect(screen, button_color_dark, [button_x,button_y,button_wdith,button_height])
            
        else:
            pygame.draw.rect(screen, button_color_light, [button_x,button_y,button_wdith,button_height])

        # Adding text to start button
        screen.blit(button_info1 , (button_x+50,button_y+35))
        screen.blit(button_info2 , (button_x+100,button_y+110))

        # Updating game display
        pygame.display.update()

    # Return full_quit
    return False


main()
