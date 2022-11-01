import pygame
import random
import datetime

# circuit bg = https://wallpaperaccess.com/full/85814.jpg
# hand palm = https://images.hdqwalls.com/wallpapers/hand-scan-blue-flames-digital-art-cn.jpg
# applause = https://static.vecteezy.com/system/resources/previews/004/652/787/large_2x/clapping-hands-different-people-applaud-isolated-on-blue-background-female-and-male-arms-congratulation-illustration-in-flat-style-vector.jpg
# fist = https://cdn.wallpaperjam.com/content/images/c0/d2/c0d27111b434a74cc0bd6d10072600ce7eab97a4.jpg 

# peace sign = https://media.istockphoto.com/vectors/sign-of-victory-or-peace-hand-gesture-of-human-black-line-icon-two-vector-id1179573132?k=20&m=1179573132&s=170667a&w=0&h=0Hmfy1BRJlmmuHO29nOD9HkQ7x5uuig7Xzman9ZIPqI=
# fist bump = https://i.pinimg.com/736x/a2/dd/16/a2dd16571d41e81475ee6a1b7a8ad01e.jpg
# vulcan sign = https://i.pinimg.com/originals/f1/8d/53/f18d5349d2848bcacb9f57b7984d0a9b.jpg
# rock and roll sign = https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREhr7L8TSfBPg0h3rIGL7SG9J6yEEV_J2irCKC29wr0RW2vL7TuUjtIAyVcywHq3OunPs&usqp=CAU
# thumbs up sign = https://www.pngfind.com/pngs/m/5-58540_thumb-signal-computer-icons-encapsulated-postscript-thumbs-up.png
# finger gun sign = https://media.istockphoto.com/vectors/hand-gun-or-pistol-gesture-line-hand-drawn-sketch-vector-vector-id1328882923?k=20&m=1328882923&s=612x612&w=0&h=e17PmB7FwDByqQknHBAmV38MLHua-SC4Ij86CwREoIk=
# shaka sign = https://t3.ftcdn.net/jpg/04/05/44/82/360_F_405448249_tubHlutVfL1m0J3tNzJlomTbMLBBLnY4.jpg
# pointer sign = https://www.nicepng.com/png/detail/12-125119_sign-language-d-finger-index-finger-clipart-black.png

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

test_suites = [TEST_SUITE_1, TEST_SUITE_2, TEST_SUITE_3]
benchmarks =  {}

# Light shade of button
button_color_light = (0,0,255)
# Dark shade of button
button_color_dark = (0,0,170)
# Font for button

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

        repeat = True
        while repeat == True:
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

    button_font = pygame.font.Font(None, 100)
    
    # Rendering text for start button
    start_button_info1 = button_font.render('Click to' , 1 , 'white')
    start_button_info2 = button_font.render('begin' , 1 , 'white')
    start_button_info3 = button_font.render('tests' , 1 , 'white')
    
    # Rendering text for benchmark button
    benchmark_button_info1 = button_font.render('Click to' , 1 , 'white')
    benchmark_button_info2 = button_font.render('set' , 1 , 'white')
    benchmark_button_info3 = button_font.render('benchmarks' , 1 , 'white')

    while running:
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
   
    benchmark_file = open("Benchmarks/benchmarks_" + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + ".txt", "a")
    
    # Going through every test suite
    for suite_num in range(len(test_suites)):
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
                        data = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
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

    return False
       

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


def countdown_screen(screen, task_number, task, hand_signs):
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


def task_screen(screen, task_number, task, hand_signs):
    running = True
    timer = 0
    max_time = 8

    bg = pygame.image.load("images/circuit_bg.png")
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
    
    for finger_num in range(8):
        if (benchmark[finger_num] - data[finger_num]) > TOLERANCE:
            success=False
            return success
    
    return success


def task_success(screen, task_num, points, points_earned_for_task, bonus_points):
    running = True

    # Position of buttons
    button_y = 525
    button_x = 600
    button_wdith = 350
    button_height = 200

    # Setting the background
    bg = pygame.image.load("images/applause.jpg")
    screen.blit(bg, (0, -100))
    
    default_font = pygame.font.Font(None, 140)

    # Displaying task successful message
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

    return False


def suite_complete_screen(screen, more_suites):
    # Track if screen should be running 
    running = True

    # Position of buttons
    button_x = 100
    next_suite_button_y = 150
    button_width = 1300
    button_height = 125

    if more_suites:
        repeat_suite_button_y = 370
        quit_tests_button_y = 590
    else:
        repeat_suite_button_y = 250
        quit_tests_button_y = 550
    
    # Setting the background
    bg = pygame.image.load("images/applause.jpg")
    screen.blit(bg, (0, -100))

    default_font = pygame.font.Font(None, 140)

    # Displaying test suite complete message
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

    button_font = pygame.font.Font(None, 100)

    # Rendering text for buttons
    button_info1 = button_font.render('Click to move onto next suite' , 1 , 'white')
    button_info2 = button_font.render('Click to attempt test suite again' , 1 , 'white')
    button_info3 = button_font.render('Otherwise, click here' , 1 , 'white')

    while running:
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

        screen.blit(button_info2 , (button_x+115,repeat_suite_button_y+30))
        screen.blit(button_info3 , (button_x+300,quit_tests_button_y+30))

        # Updating game display
        pygame.display.update()    

    # return continue_next_suite, repeat, full_quit
    return False, False, False


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

    return False


main()
