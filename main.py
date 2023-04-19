# import dependencies
import pygame

import time
import numpy as np

# create currency format for numbers
import locale
locale.setlocale(locale.LC_ALL, 'en_US')


# class for the 6 different stocks
class Stocks:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.shares = 0

    def buy_stock(self, amount):
        global liquid_cash, networth, year
        # check if the amount inputted can be purchased
        if self.data[year - 1] * amount <= liquid_cash:
            self.shares += amount
            liquid_cash -= self.data[year - 1] * amount
            return True
        # if the amount exceeds the amount you can buy, buy the max amount
        else:
            max_amount = int(liquid_cash // self.data[year - 1])
            self.shares += max_amount
            liquid_cash -= self.data[year - 1] * max_amount
            return False

    def sell_stock(self, amount):
        global liquid_cash, networth, year
        # check if the amount inputted can be sold
        if amount <= self.shares:
            self.shares -= amount
            liquid_cash += self.data[year - 1] * amount
        # if the amount exceeds the amount you can sell, sell the max amount
        else:
            max_amount = self.shares
            self.shares -= max_amount
            liquid_cash += self.data[year - 1] * max_amount

    # return the amount a stock contributes to your net worth
    def stock_value(self):
        return self.data[year - 1] * self.shares


class Button:
    # action represents the function called on click
    def __init__(self, text, x, y, width, height, color, color_on_click, hover_color, stock, input_box, action):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.color_on_click = color_on_click
        self.hover_color = hover_color
        self.stock = stock
        self.input_box = input_box
        self.action = action

    def draw_button(self):
        global input_active
        pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # check if button is clicked
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                # call assigned function if button is clicked
                # clicked color
                pygame.draw.rect(WINDOW, self.color_on_click, button_rect)
                self.action(self.stock, self.input_box)
            # hover color
            else:
                pygame.draw.rect(WINDOW, self.hover_color, button_rect)
        # default color
        else:
            pygame.draw.rect(WINDOW, self.color, button_rect)

        # button outline
        pygame.draw.line(WINDOW, WHITE, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(WINDOW, WHITE, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(WINDOW, BLACK, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(WINDOW, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # button text
        text = font3.render(self.text, True, BLACK)
        text_len = text.get_width()
        WINDOW.blit(text, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 5))


class InputBox:
    def __init__(self, x, y, width, height, color, color_on_click):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.color_on_click = color_on_click
        self.active = False
        self.text = ""

    # key is a boolean value which indicates if a number or backspace key is pressed
    def draw_input_box(self, key):
        global bool_array, input_active
        pos = pygame.mouse.get_pos()
        input_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # check if input box is clicked
        if pygame.mouse.get_pressed()[0] == 1:
            if input_rect.collidepoint(pos):
                self.active = True
                input_active = True
            else:
                self.active = False

        # only backspace and number keys are accepted
        # if backspace is pressed
        if self.active and key:
            if key == "BACK":
                self.text = self.text[:-1]

            # limit the number of characters stored in the input box to 8
            elif len(self.text) < 8:
                self.text += key

        # on click color
        if self.active:
            pygame.draw.rect(WINDOW, self.color_on_click, input_rect)
        # default color
        else:
            pygame.draw.rect(WINDOW, self.color, input_rect)

        # display text stored in input box
        text = font3.render(self.text, True, BLACK)
        text_len = text.get_width()
        WINDOW.blit(text, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 5))

    # returns value present within the input box
    def get_value(self):
        if self.text:
            return int(self.text)
        # if the input box is empty the default value is 1
        else:
            return 1


# function called when buy button is clicked
def buy_stock(stock, input_box):
    global input_active
    input_active = True
    stock.buy_stock(input_box.get_value())
    # reset value in input box
    input_box.text = ""


# function called when sell button is clicked
def sell_stock(stock, input_box):
    global input_active
    input_active = True
    stock.sell_stock(input_box.get_value())
    # reset value in input box
    input_box.text = ""


# function called when info button is clicked
# dummy parameters are used, parameters are only place holders as other button functions require parameters
def info_click(dummy1, dummy2):
    global info_active, start_time, time_elapsed
    info_active = True
    time_elapsed = time.time() - start_time


# function called when close button is clicked
# dummy parameters are used, parameters are only place holders as other button functions require parameters
def close_click(dummy1, dummy2):
    global info_active, start_time, time_elapsed
    info_active = False
    start_time = time.time() - time_elapsed


# function called when play again button is pressed
def play_again(dummy1, dummy2):
    global start_time, year, liquid_cash, networth, game_over
    # reset values to initial amount
    start_time = time.time()
    year = 1
    liquid_cash = 1000
    networth = 1000
    game_over = False


# predicted value based on previous year stock prices
def computer_predictions(year, row, col):
    # goes back a maximum of 5 years
    start = None
    for i in range(year - 1, -1, -1):
        if stock_list[row][col].data[i] != 0:
            start = i
        elif stock_list[row][col].data[i] == 0 or i == year - 6:
            break

    total = 0
    num_years = year - start
    # no prediction can be made during the stocks first year
    if num_years == 1 or start is None:
        return False

    # find the percent growth over the past 5 years
    growth_list = []
    for i in range(start + 1, start + num_years):
        growth = (stock_list[row][col].data[i] - stock_list[row][col].data[i - 1]) / stock_list[row][col].data[i - 1]
        total += growth
        growth_list.append(growth)

    # prediction is the average % growth over the past 5 years
    # return the prediction and error, error is calculated using numpy's standard deviation
    return [round(total / (num_years - 1), 2), round(np.std(growth_list), 2)]


# initialize pygame
pygame.init()

# initialize constants
WIDTH = 1000
HEIGHT = 600
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)
BROWN = (230, 227, 188)
GREEN = (150, 153, 129)
LIGHT_GREEN = (175, 209, 65)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BORDER = 25
font = pygame.font.SysFont('freesansbold.ttf', 48)
font2 = pygame.font.SysFont('freesansbold.ttf', 30)
font3 = pygame.font.SysFont('freesansbold.ttf', 21)
font4 = pygame.font.SysFont('freesansbold.ttf', 18)

# game constants
FPS = 60
time_per_year = 45
max_years = 20

# all lists have a shape of (2, 3) representing 2 rows and 3 stocks in each row
# file path for assets
logo_file_path = [["Nikola_logo.png", "waterfox_logo.png", "big_dollar_logo.png"],
                  ["game_store_logo.png", "national_bank_logo.png", "games_for_fun_logo.png"]]

# list of stocks names
stock_names = [["Nikola", "Waterfox", "Big Dollar"], ["GameStart", "National Bank", "Games For Fun"]]

# list of stock instances
stock_list = [[Stocks("Nikola",
                      [0, 0, 0, 0, 0, 0, 0, 1.56, 1.78, 2.08, 6.96, 14.89, 15.34, 13.98, 20.95, 21.15, 18.23, 96.67,
                       260.00, 263.09, 123.18]),
               Stocks("Waterfox",
                      [0, 3.81, 6.97, 10.31, 13.51, 11.66, 11.02, 13.43, 14.27, 16.12, 22.17, 28.42, 31.00, 38.16,
                       46.99, 56.10, 59.56, 73.95, 124.22, 114.76, 88.73]),
               Stocks("Big Dollar",
                      [0, 0, 0, 0, 0, 0, 0, 0.09, 0.30, 5.28, 13.30, 754.22, 314.25, 434.33, 998.33, 13657.20, 3843.52,
                       7200.17, 29374.15, 47686.81, 16547.50])],
              [Stocks("GameStart",
                      [1.61, 1.14, 1.49, 2.43, 3.80, 7.00, 7.03, 4.20, 3.45, 3.95, 3.72, 7.11, 7.23, 7.65, 5.52, 4.51,
                       3.38, 1.87, 1.79, 42.42, 29.64, 18.46]),
               Stocks("National Bank",
                      [8.54, 10.82, 12.21, 16.66, 22.80, 28, 44, 25.00, 24.41, 32.89, 33.80, 36.17, 42.78, 49.28, 44.11,
                       46.02, 59.40, 64.14, 67.51, 64.69, 92.20, 98.33, 93.95]),
               Stocks("Games For Fun",
                      [11.01, 11.62, 10.52, 10.83, 11.33, 15.49, 12.06, 11.34, 15.49, 12.06, 11.36, 16.27, 19.85, 26.40,
                       34.82, 30.30, 22.29, 29.29, 29.35, 20.41, 15.00, 12.09, 11.80, 20.43, 21.74, 20.81])]]

# list of stock descriptions
stock_description = [["An electric car company", "A major tech company", "A digital currency company"],
                     ["A video game store", "A major bank", "A toy store"]]

# list of events over the 20 year period
events = [
    ["After terrorist attacks the stock market", "has reached the lowest point it has", "been in the past 5 years"],
    ["New tax cuts were proposed in hopes of", "revitalizaing the slumping economy"],
    ["The net captital rule was loosened", "allowing many companies to make much", "bigger investments using borrowed",
     "money"],
    ["The economic powers of the east began", "rapidly growing, and many decided to",
     "outsource labort to eastern countries", "in order to cut costs"],
    ["No new major events this year"],
    ["A major crash in the housing market", "is occuring, and house sales is at the", "lowest point it has been in",
     "2 decades"],
    ["Due to the economic ruin, major", "investment banks have filed for", "bankruptcy"],
    ["A rescue plan has been announced", "where 700 billion $ of tax payer", "money is being used to help",
     "stabilize markets"],
    ["A financial reform bill was signed", "giving government more control", "over investent banks in hopes",
     "of preventing a future crash"],
    ["Major protests are breaking out due", "to wealth inequalities plaguing",
     "the country after the financial crisis"],
    ["No new major events this year"],
    ["A new legislation has been passed to", "prevent banks from making risky", "investments using customer deposits"],
    ["Rescue plan inforced a few years", "prior ends"],
    ["No new major events this year"],
    ["No new major events this year"],
    ["No new major events this year"],
    ["A new bill was passed where now only", "banks with assests greater than $250", "billion are subject to increased",
     "government oversight"],
    ["A new unknown virus has been", "discovered at the end of the", "year"],
    ["Many businesses close due to the", "virus, and many are forced to", "quarantine"],
    ["The effects of the virus continue,", "however, businesses start to reopen as", "the pandemic starts to ease up"]
]

# initialize button and input box list
button_list = []
input_box_list = []
# boolean array which represents which stock screen to display
# True represents buying screen and False represents info screen
bool_array = []

# add instances into respective list with a shape of (2, 3)
for i in range(2):
    button_row = []
    input_row = []
    bool_row = []
    for j in range(3):
        # add input box
        curr_input_box = [InputBox(WIDTH / 3 + BORDER + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j + BORDER + 65,
                                   BORDER + HEIGHT / 3.5 + (HEIGHT / 2 - BORDER) * i, 100, 20, WHITE, LIGHT_GRAY),
                          InputBox(WIDTH / 3 + BORDER + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j + BORDER + 65,
                                   BORDER + HEIGHT / 3.5 + (HEIGHT / 2 - BORDER) * i + 35, 100, 20, WHITE, LIGHT_GRAY)]
        # add buy and sell buttons
        curr_button = [Button("Buy", WIDTH / 3 + BORDER + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j + BORDER,
                              BORDER + HEIGHT / 3.5 + (HEIGHT / 2 - BORDER) * i, 50, 20, GRAY, WHITE, GRAY,
                              stock_list[i][j], curr_input_box[0], buy_stock),
                       Button("Sell", WIDTH / 3 + BORDER + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j + BORDER,
                              BORDER + HEIGHT / 3.5 + (HEIGHT / 2 - BORDER) * i + 35, 50, 20, GRAY, WHITE, GRAY,
                              stock_list[i][j], curr_input_box[1], sell_stock)]

        input_row.append(curr_input_box)
        button_row.append(curr_button)
        # bool_array is initialize to all True
        bool_row.append(True)

    input_box_list.append(input_row)
    button_list.append(button_row)
    bool_array.append(bool_row)

# create single buttons
info_button = Button("Info", BORDER, HEIGHT/1.075, 50, 20, WHITE, WHITE, GRAY, None, None, info_click)
info_close_button = Button("Close", WIDTH - 50 - BORDER, 10, 50, 20, WHITE, WHITE, GRAY, None, None, close_click)
play_again_button = Button("Play Again", WIDTH / 2 - 50, HEIGHT / 2 + 70, 100, 25, WHITE, WHITE, GRAY, None, None,
                           play_again)

# initialize variables
liquid_cash = 1000
networth = 1000
money_per_year = 1000
game_over = False
start_time = time.time()
cooldown = time.time()
time_elapsed = 0
# input active represents if another button or input box is currently being clicked
input_active = None
info_active = False
# year one is equivalent to 2002 in real world
year = 1

# initalize game window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quant Simulator")


# helper function which updates display
def draw_items(key):
    global input_active, cooldown
    # draw background textures
    texture2_img = pygame.image.load('Texture2.png').convert_alpha()
    texture2_img = pygame.transform.smoothscale(texture2_img, (WIDTH, HEIGHT))
    WINDOW.blit(texture2_img, (0, 0))

    texture1_img = pygame.image.load('Texture1.png').convert_alpha()
    texture1_img = pygame.transform.smoothscale(texture1_img,
                                                (WIDTH - 2 * BORDER - int(WIDTH / 3), HEIGHT - 2 * BORDER))
    WINDOW.blit(texture1_img, (int(WIDTH / 3) + BORDER, BORDER))

    bg_img = pygame.image.load('Texture3.png').convert_alpha()
    bg_img = pygame.transform.smoothscale(bg_img, (int(WIDTH / 3), HEIGHT))
    WINDOW.blit(bg_img, (0, 0))

    # black lines
    pygame.draw.rect(WINDOW, BLACK,
                     pygame.Rect(int(WIDTH / 3) + BORDER, HEIGHT / 2, WIDTH - 2 * BORDER - int(WIDTH / 3), 2))
    pygame.draw.rect(WINDOW, BLACK,
                     pygame.Rect(int(WIDTH / 3) + BORDER + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3, BORDER, 2,
                                 HEIGHT - 2 * BORDER))
    pygame.draw.rect(WINDOW, BLACK,
                     pygame.Rect(int(WIDTH / 3) + BORDER + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * 2, BORDER, 2,
                                 HEIGHT - 2 * BORDER))

    text = font.render('Quant Simulator', True, WHITE)
    WINDOW.blit(text, (BORDER, BORDER))

    # timer
    text = font2.render(f"Year {year} of {max_years}", True, WHITE)
    WINDOW.blit(text, (BORDER, HEIGHT / 8))

    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(BORDER, HEIGHT / 6, WIDTH / 3 - 2 * BORDER, 25))
    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(BORDER + 2.5, HEIGHT / 6 + 2.5, WIDTH / 3 - 2 * BORDER - 2.5, 20))

    pygame.draw.rect(WINDOW, LIGHT_GREEN, pygame.Rect(BORDER + 2.5, HEIGHT / 6 + 2.5,
                                                      (WIDTH / 3 - 2 * BORDER) - (WIDTH / 3 - 2 * BORDER) * (
                                                                  time.time() - start_time) / time_per_year, 20))

    # quant simulator logo
    logo_img = pygame.image.load('quant_simulator_logo.png').convert_alpha()
    logo_img = pygame.transform.smoothscale(logo_img, (WIDTH / 5, HEIGHT / 5))
    WINDOW.blit(logo_img, (WIDTH / 16, HEIGHT / 3.5))

    text = font2.render(f"Networth: {locale.currency(networth, grouping = True)}", True, WHITE)
    WINDOW.blit(text, (BORDER, HEIGHT / 1.8))
    text = font2.render(f"Liquid Capital: {locale.currency(liquid_cash, grouping = True)}", True, WHITE)
    WINDOW.blit(text, (BORDER, HEIGHT / 1.6))

    # current events text box
    text = font2.render("Current Events:", True, WHITE)
    WINDOW.blit(text, (BORDER, HEIGHT / 1.4))

    # separates current event text onto multiple lines
    for line in range(0, len(events[year - 1])):
        text = font3.render(events[year - 1][line], True, WHITE)
        WINDOW.blit(text, (BORDER, HEIGHT / (1.3 - 0.05 * line)))

    # draw info button
    info_button.draw_button()

    # draw individual stocks
    for i in range(2):
        for j in range(3):
            # replace stock image with a unavailiable image if stock has not been released
            if stock_list[i][j].data[year - 1] == 0:
                stock_logo_img = pygame.image.load("unavailable.png").convert_alpha()
                stock_logo_img = pygame.transform.smoothscale(stock_logo_img, (WIDTH / 5, HEIGHT / 5))
                WINDOW.blit(stock_logo_img, (WIDTH / 3 + BORDER + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                                             BORDER + HEIGHT / 12 + (HEIGHT / 2 - BORDER) * i))
            else:
                # stock name
                text = font2.render(stock_names[i][j], True, BLACK)
                textRect = text.get_rect(center=(
                (2 * (WIDTH / 3 + BORDER) + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3) / 2 + (
                            WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                (BORDER + HEIGHT / 8) / 2 + (HEIGHT / 2 - BORDER) * i))
                WINDOW.blit(text, textRect)

                # stock image
                stock_logo_img = pygame.image.load(logo_file_path[i][j]).convert_alpha()
                stock_logo_img = pygame.transform.smoothscale(stock_logo_img, (WIDTH / 10, HEIGHT / 10))
                WINDOW.blit(stock_logo_img, (
                WIDTH / 3 + BORDER + WIDTH / 20 + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                BORDER + HEIGHT / 12 + (HEIGHT / 2 - BORDER) * i))

                # if the user is on the stock buy screen
                if bool_array[i][j]:
                    # display value of stock
                    text = font3.render(f"Value: {locale.currency(stock_list[i][j].data[year - 1], grouping = True)}", True, BLACK)
                    textRect = text.get_rect(center=(
                    (2 * (WIDTH / 3 + BORDER) + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3) / 2 + (
                                WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                    (HEIGHT / 4) + (HEIGHT / 2 - BORDER) * i))
                    WINDOW.blit(text, textRect)

                    # display number of shares owned
                    text = font3.render(f"Shares: {stock_list[i][j].shares}", True, BLACK)
                    textRect = text.get_rect(center=(
                    (2 * (WIDTH / 3 + BORDER) + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3) / 2 + (
                                WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                    (HEIGHT / 4) + 20 + (HEIGHT / 2 - BORDER) * i))
                    WINDOW.blit(text, textRect)

                    # display input box and buy and sell button
                    for x in range(2):
                        button_list[i][j][x].draw_button()
                        input_box_list[i][j][x].draw_input_box(key)

                # if the user is on the stock information screen
                else:
                    # get computer predictions
                    computer = computer_predictions(year, i, j)
                    # if no predictions display N/A, N/A
                    if not computer:
                        computer = ["N/A", "N/A"]
                    else:
                        computer[0], computer[1] = round(computer[0] * 100, 2), round(computer[1] * 100, 2)

                    # display predictions
                    text = font3.render(f"Predicted Increase: {computer[0]}%", True, BLACK)
                    textRect = text.get_rect(center=(
                    (2 * (WIDTH / 3 + BORDER) + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3) / 2 + (
                                WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                    (HEIGHT / 4) + 10 + (HEIGHT / 2 - BORDER) * i))
                    WINDOW.blit(text, textRect)

                    # display error
                    text = font3.render(f"Error: {computer[1]}%", True, BLACK)
                    textRect = text.get_rect(center=(
                    (2 * (WIDTH / 3 + BORDER) + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3) / 2 + (
                                WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                    (HEIGHT / 4) + 30 + (HEIGHT / 2 - BORDER) * i))
                    WINDOW.blit(text, textRect)

                    # get stock growth
                    if stock_list[i][j].data[year - 2] != 0 and year != 1:
                        text = font3.render(f"Stock Growth: {round((stock_list[i][j].data[year - 1] - stock_list[i][j].data[year - 2]) / stock_list[i][j].data[year - 2] * 100, 2)}%", True, BLACK)
                    # display N/A if its the first year of the stock
                    else:
                        text = font3.render(f"Stock Growth: N/A%", True, BLACK)

                    # display stock growth
                    textRect = text.get_rect(center=(
                    (2 * (WIDTH / 3 + BORDER) + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3) / 2 + (
                                WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                    (HEIGHT / 4) + 60 + (HEIGHT / 2 - BORDER) * i))
                    WINDOW.blit(text, textRect)

                    # display stock description
                    text = font3.render(f"Description:", True, BLACK)
                    textRect = text.get_rect(center=(
                    (2 * (WIDTH / 3 + BORDER) + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3) / 2 + (
                                WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                    (HEIGHT / 4) + 90 + (HEIGHT / 2 - BORDER) * i))
                    WINDOW.blit(text, textRect)

                    text = font4.render(stock_description[i][j], True, BLACK)
                    textRect = text.get_rect(center=(
                    (2 * (WIDTH / 3 + BORDER) + (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3) / 2 + (
                                WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3 * j,
                    (HEIGHT / 4) + 110 + (HEIGHT / 2 - BORDER) * i))
                    WINDOW.blit(text, textRect)

    # check if the stock is clicked prompting the switch to the stock information screen
    # input active represents if another button or input box is currently being clicked
    if not input_active and pygame.mouse.get_pressed()[0] == 1 and time.time() - cooldown >= 0.1:
        # loop through all stocks
        for i in range(2):
            for j in range(3):
                stock_width = (WIDTH - 2 * BORDER - int(WIDTH / 3)) / 3
                stock_height = (HEIGHT / 2 - BORDER)
                stockRect = pygame.Rect(WIDTH / 3 + BORDER + stock_width * j, BORDER + stock_height * i, stock_width,
                                        stock_height)
                pos = pygame.mouse.get_pos()
                # check if mouse collides with a stock
                if stockRect.collidepoint(pos):
                    # updates boolean array if stock is being clicked
                    # cooldown makes sure that a stock screen can only be changed every 0.1 seconds
                    cooldown = time.time()
                    if bool_array[i][j]:
                        bool_array[i][j] = False
                    else:
                        bool_array[i][j] = True

    # display the instructions screen if the info button is pressed
    if info_active:
        instruction_img = pygame.image.load("Instructions.png").convert_alpha()
        stock_logo_img = pygame.transform.smoothscale(instruction_img, (WIDTH, HEIGHT))
        WINDOW.blit(stock_logo_img, (0, 0))

        # display the info close button
        info_close_button.draw_button()

    pygame.display.update()


# screen displayed after the 20 year period
def game_over_screen():
    # display background
    texture2_img = pygame.image.load('Texture2.png').convert_alpha()
    texture2_img = pygame.transform.smoothscale(texture2_img, (WIDTH, HEIGHT))
    WINDOW.blit(texture2_img, (0, 0))

    # display game over text
    text = font.render('Game Over', True, WHITE)
    textRect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 35))
    WINDOW.blit(text, textRect)

    # display net worth
    text = font.render(f"Networth: {locale.currency(networth, grouping = True)}", True, WHITE)
    textRect = text.get_rect(center=(WIDTH / 2, (HEIGHT + 50) / 2))
    WINDOW.blit(text, textRect)

    # display play again button
    play_again_button.draw_button()

    # update display
    pygame.display.update()


def main():
    global year, game_over, start_time, money_per_year, liquid_cash, networth, input_active
    running = True
    while running:
        key = None
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            clock.tick(FPS)
            # exit program if x button is clicked
            if event.type == pygame.QUIT:
                running = False

            # if a key is pressed
            if event.type == pygame.KEYDOWN:
                # check if ket is pressed is numeric or a backspace
                if event.key == pygame.K_BACKSPACE:
                    key = "BACK"
                elif event.unicode.isnumeric():
                    key = event.unicode

            # update input active if mouse is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = False
            else:
                input_active = True

        # display game over screen after the 20 year period
        if game_over:
            game_over_screen()
        else:
            draw_items(key)
            # increment year after timer expires
            if time.time() - start_time >= time_per_year and not info_active:
                year += 1
                # set game over to True after 20 year period
                if year > max_years:
                    game_over = True
                    # update net worth
                    networth = liquid_cash
                    for i in range(2):
                        for j in range(3):
                            networth += stock_list[i][j].stock_value()

                # update net worth
                if not game_over:
                    # add more liquid cash
                    # liquid cash is adjusted for inflation each year
                    money_per_year = round(money_per_year * 1.038, 2)
                    liquid_cash += money_per_year
                    networth = liquid_cash
                    for i in range(2):
                        for j in range(3):
                            networth += stock_list[i][j].stock_value()
                    start_time = time.time()

    pygame.quit()


main()
