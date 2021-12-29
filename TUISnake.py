import os
from curses import *
import sys
import socket
import random
import time
import json

menu = ["PLAY", "PLAY MULTIPLAYER", "OPTIONS", "EXIT"]  # Menu for start
menu2 = ["PLAY AGAIN", "EXIT"]  # Menu for loses
menu3 = ["Char of snake: ", "Char of apple: ", "Color of snake: ", "Color of apple: ", "Back"]  # Menu for options
char_of_snake = '#'
char_of_apple = '8'
color_of_snake = 5  # Green color
color_of_apple = 1  # Red color
SnakeParts = []  # Snake`s parts
client_name = "Snake_game_client"


# Making start menu
def start_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        global y
        global x
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(color_pair(8))
            stdscr.addstr(y, x, row)
            stdscr.attroff(color_pair(8))
        else:
            stdscr.addstr(y, x, row)
        stdscr.refresh()
    y -= 8
    x = w // 2 - len('TUI_SNAKE') // 2
    stdscr.addstr(y, x, 'TUI_SNAKE', color_pair(5))


def options_menu(stdscr, selected_row_idx):
    stdscr.clear()
    for idx, row in enumerate(menu3):
        global y
        global x
        x = len(row) // 2
        y = len(menu3) // 2 + idx
        if idx == selected_row_idx:
            stdscr.addstr(y, x, row, color_pair(8))
        else:
            stdscr.addstr(y, x, row)
        stdscr.addstr(len(menu3) // 2, len('Char of snake: ') + 7, '{}'.format(char_of_snake))
        stdscr.addstr(len(menu3) // 2 + 1, len('Char of apple: ') + 7, '{}'.format(char_of_apple))
        stdscr.addstr(len(menu3) // 2 + 2, len('Color of snake: ') + 7, '{}'.format(color_of_snake))
        stdscr.addstr(len(menu3) // 2 + 3, len('Color of apple: ') + 7, '{}'.format(color_of_apple))
        stdscr.refresh()


def losing_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w, = stdscr.getmaxyx()
    for idx, row in enumerate(menu2):
        global lose_y
        global lose_x
        lose_x = w // 2 - len(row) // 2
        lose_y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(color_pair(8))
            stdscr.addstr(lose_y, lose_x, row)
            stdscr.attroff(color_pair(8))
        else:
            stdscr.addstr(lose_y, lose_x, row)
        stdscr.refresh()
    lose_y -= 8
    x = w // 2 - len('YOU ARE DEAD!') // 2
    stdscr.addstr(lose_y, x, 'YOU ARE DEAD!', color_pair(1))
    stdscr.addstr(lose_y + 2, x + 2, 'Score: {}'.format(len(SnakeParts) - 1))


def using_lose_menu(stdscr):
    global SnakeParts
    current_row_idx = 0
    while True:
        losing_menu(stdscr, current_row_idx)
        lose_key = stdscr.getch()
        if lose_key == KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif lose_key == KEY_DOWN and current_row_idx < len(menu2) - 1:
            current_row_idx += 1
        elif lose_key in [10, 13]:
            if menu2[current_row_idx] == 'PLAY AGAIN':
                SnakeParts = []
                stdscr.clear()
                mainfunc(stdscr)
            else:
                endwin()
                sys.exit()


# Generates a new apple
def eating_apples(stdscr):
    global apple_y
    global apple_x
    h, w, = stdscr.getmaxyx()
    apple_y = random.randint(2, h - 3)
    apple_x = random.randint(2, w - 3)
    square_for_steps(stdscr)
    stdscr.addstr(apple_y, apple_x, '{}'.format(char_of_apple), color_pair(color_of_apple))
    stdscr.refresh()


def make_square(stdscr):
    h, w = stdscr.getmaxyx()
    square_x = 1
    square_y = 1
    while square_x != w:
        stdscr.attron(color_pair(1))
        stdscr.addstr(square_y, square_x, '-')
        time.sleep(0.01)
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        square_x += 1
    square_x -= 1
    while square_y != h - 1:
        stdscr.attron(color_pair(1))
        stdscr.addstr(square_y, square_x, '|')
        time.sleep(0.02)
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        square_y += 1
    square_y -= 1
    while square_x != 1:
        stdscr.attron(color_pair(1))
        stdscr.addstr(square_y, square_x - 1, '-')
        time.sleep(0.01)
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        square_x -= 1
    while square_y != 0:
        stdscr.attron(color_pair(1))
        stdscr.addstr(square_y, square_x, '|')
        time.sleep(0.02)
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        square_y -= 1


def square_for_steps(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    square_x = 1
    square_y = 1
    while square_x != w:
        stdscr.attron(color_pair(1))
        stdscr.addstr(square_y, square_x, '-')
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        square_x += 1
    square_x -= 1
    while square_y != h - 1:
        stdscr.attron(color_pair(1))
        stdscr.addstr(square_y, square_x, '|')
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        square_y += 1
    square_y -= 1
    while square_x != 1:
        stdscr.attron(color_pair(1))
        stdscr.addstr(square_y, square_x - 1, '-')
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        square_x -= 1
    while square_y != 0:
        stdscr.attron(color_pair(1))
        stdscr.addstr(square_y, square_x, '|')
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        square_y -= 1


def drawing_first_element(stdscr, apple_y, apple_x):
    stdscr.addstr(SnakeParts[0][0], SnakeParts[0][1], '{}'.format(char_of_snake), color_pair(color_of_snake))
    stdscr.addstr(apple_y, apple_x, '{}'.format(char_of_apple), color_pair(color_of_apple))
    stdscr.addstr(2, 3, 'Score : {}'.format(len(SnakeParts) - 1))
    stdscr.refresh()


# Creates json string for the server, q means quotes
def writing_json(type):
    if type != "connect" and type != "disconnect" and type != "get_grid":
        json_string = """
                    [
                        qclientq: q{0}q,
                        qkindq: [
                            qchange_directionq: q{1}q
                        ]
                    ]
        """.format(client_name, type)
    else:
        json_string = """
                    [
                        qclientq: q{0}q,
                        qkindq: q{1}q
                    ]
                    """.format(client_name, type)
    json_string = json_string.replace("[", "{")
    json_string = json_string.replace("]", "}")
    json_string = json_string.replace("q", "\"")
    binary_json_string = bytes(json_string, 'utf-8')
    return binary_json_string


# Connecting to the server using TCP
def connecting_to_server(stdscr):
    global client_name
    global ip_address
    global port
    global server_socket
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x_ip = w // 2 - len("Enter an ip address of the server:") // 2
    stdscr.addstr(8, x_ip, "Enter an ip address of the server:")
    stdscr.refresh()
    echo()
    stdscr.move(9, x_ip)
    ip_address = stdscr.getstr().decode("utf-8")
    stdscr.clear()
    stdscr.addstr(8, x_ip, "Enter a port of the server:")
    stdscr.refresh()
    stdscr.move(9, x_ip)
    port = stdscr.getstr().decode("utf-8")
    noecho()
    stdscr.refresh()
    # Creates a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connects socket with the server
    code_of_operation = server_socket.connect_ex((ip_address, int(port)))
    if code_of_operation != 0:
        stdscr.clear()
        stdscr.addstr(h // 2, w // 2, "Unable to connect to the server: {}".format(os.strerror(code_of_operation)))
        stdscr.refresh()
        time.sleep(2)
        mainfunc(stdscr)
    stdscr.clear()
    stdscr.addstr(h // 2, w // 2, "Connecting to the server...")
    stdscr.refresh()
    binary_json_string = writing_json("connect")
    endwin()
    send_to_a_server(server_socket, binary_json_string)
    # Gets a new name(to make all names unique)
    client_name = server_socket.recv(1024**3).decode("utf-8")
    # Deletes quotes
    client_name = client_name[1:len(client_name) - 1]
    binary_json_string = writing_json("get_grid")
    # Delay
    time.sleep(0.08)
    send_to_a_server(server_socket, binary_json_string)
    server_json_string = server_socket.recv(1024**3).decode("utf-8")
    endwin()
    print(server_json_string)
    loaded_json_string = json.loads(server_json_string)
    endwin()
    # Return json string from the server
    return loaded_json_string


# Sends json string to a server
def send_to_a_server(server_socket, binary_json_string):
    totalsent = 0
    while totalsent < len(binary_json_string):
        sent = server_socket.send(binary_json_string)
        if sent == 0:
            endwin()
            raise RuntimeError("Socket connection is broken")
        totalsent += sent


def draw_field_multiplayer(stdscr, x, y):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    # If window is too small for a field then say about it to a user and exit
    if w < x or h < y:
        stdscr.addstr(h // 2, 0, "Make your window bigger: {0}x{1}".format(x + 2, y + 2))
        stdscr.refresh()
        time.sleep(3)
        sys.exit()
    field_x = 0
    field_y = 0
    while field_x != x:
        stdscr.attron(color_pair(1))
        stdscr.addstr(field_y, field_x, '-')
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        field_x += 1
    field_x -= 1
    while field_y != y:
        stdscr.attron(color_pair(1))
        stdscr.addstr(field_y, field_x, '|')
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        field_y += 1
    field_y -= 1
    while field_x != 0:
        stdscr.attron(color_pair(1))
        stdscr.addstr(field_y, field_x - 1, '-')
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        field_x -= 1
    while field_y != 0:
        stdscr.attron(color_pair(1))
        stdscr.addstr(field_y, field_x, '|')
        stdscr.refresh()
        stdscr.attroff(color_pair(1))
        field_y -= 1


def draw_objects(stdscr, snakeparts, apples):
    endwin()
    h, w = stdscr.getmaxyx()
    for i in range(len(snakeparts)):
        x = ""
        y_snake = ""
        y_is_passed = 0
        for m in range(len(str(snakeparts[i]))):
            if snakeparts[i][m] == ':':
                y_is_passed = 1
                continue
            elif y_is_passed == 1:
                x = x + snakeparts[i][m]
                continue
            else:
                y_snake = y_snake + snakeparts[i][m]
                continue
        y_snake = y_size - int(y_snake)
        stdscr.addstr(int(y_snake), int(x), '{}'.format(char_of_snake), color_pair(color_of_snake))
        endwin()
        print("Y and X of a snake: {0}, {1}".format(y_snake, int(x)))
        print("Snake: {}".format(snakeparts[i]))
    # y_size variable is a size of a field by y axe
    # We need to subtract y_snake from maximum size because ncurses's (0;0) coordinate located in the upper left corner
    # But server's (0;0) coordinate located in the lower left corner. We need to do an inversion
    x = ""
    y = ""
    y_is_passed = 0
    for i in range(len(apples)):
        x = ""
        y = ""
        y_is_passed = 0
        for m in range(len(str(apples[i]))):
            if apples[i][m] == ':':
                y_is_passed = 1
                continue
            elif y_is_passed == 1:
                x = x + apples[i][m]
                continue
            else:
                y = y + apples[i][m]
                continue
        stdscr.addstr(int(y), int(x), '{}'.format(char_of_apple), color_pair(color_of_apple))
        stdscr.refresh()


def json_parse(loaded_json_string):
    global snakeparts
    global apples
    global x_size
    global y_size
    snakeparts = []
    apples = []
    is_it_a_snake = 0 # This variable indicates whether the object in a string a snake
    # If this variable equals 1 then the object is a snake, if the variable equals 2 then the object is an apple
    # Parsing json string
    for number in range(0, len(loaded_json_string["data"])):
        endwin()
        print("Here is {} part: {}".format(number, loaded_json_string["data"][number]))
        for parameter in loaded_json_string["data"][number]:
            # If it's color then client skips it
            if parameter == "color":
                continue
            # If it's a snake part, then client prints "Snake"
            if loaded_json_string["data"][number][parameter] == "snake_part":
                print("Snake")
                is_it_a_snake = 1
                continue
            # If it's an apple, then client prints "Apple"
            elif loaded_json_string["data"][number][parameter] == "Apple":
                print("Apple")
                is_it_a_snake = 2
                continue
            # if it's coordinates, then client prints them
            if parameter == "coordinates":
                if is_it_a_snake == 1:
                    snakeparts.append("{0}:{1}".format(loaded_json_string["data"][number][parameter]["y"], loaded_json_string["data"][number][parameter]["x"]))
                    endwin()
                    print("y_snake: {}".format(loaded_json_string["data"][number][parameter]["y"]))
                    print("x_snake: {}".format(loaded_json_string["data"][number][parameter]["x"]))
                else:
                    apples.append("{0}:{1}".format(loaded_json_string["data"][number][parameter]["y"], loaded_json_string["data"][number][parameter]["x"]))
                    print("x: {}".format(loaded_json_string["data"][number][parameter]["x"]))
                    print("y: {}".format(loaded_json_string["data"][number][parameter]["y"]))
            else:
                endwin()
                print("New: {}".format(loaded_json_string["data"][number][parameter]))
    x_size = loaded_json_string["size"][0]
    y_size = loaded_json_string["size"][1]
    print("x_size: {0}, y_size : {1}".format(x, y))
    print("Snakeparts: {}".format(snakeparts))


def multiplayer_gameplay(stdscr):
    loaded_json_string = connecting_to_server(stdscr)
    json_parse(loaded_json_string)
    draw_field_multiplayer(stdscr, x_size, y_size)
    draw_objects(stdscr, snakeparts, apples)
    while True:
        while True:
            halfdelay(1)
            step = stdscr.getch()
            if step == KEY_UP:
                binary_json_string = writing_json("up")
                send_to_a_server(server_socket, binary_json_string)
                binary_json_string = writing_json("get_grid")
                time.sleep(0.01)
                send_to_a_server(server_socket, binary_json_string)
                time.sleep(0.01)
                server_json_string = server_socket.recv(1024**3).decode("utf-8")
                loaded_json_string = json.loads(server_json_string)
                break
            elif step == KEY_DOWN:
                binary_json_string = writing_json("down")
                send_to_a_server(server_socket, binary_json_string)
                binary_json_string = writing_json("get_grid")
                time.sleep(0.01)
                send_to_a_server(server_socket, binary_json_string)
                time.sleep(0.01)
                server_json_string = server_socket.recv(1024**3).decode("utf-8")
                loaded_json_string = json.loads(server_json_string)
                break
            elif step == KEY_LEFT:
                binary_json_string = writing_json("left")
                send_to_a_server(server_socket, binary_json_string)
                binary_json_string = writing_json("get_grid")
                time.sleep(0.01)
                send_to_a_server(server_socket, binary_json_string)
                time.sleep(0.01)
                server_json_string = server_socket.recv(1024**3).decode("utf-8")
                loaded_json_string = json.loads(server_json_string)
                break
            elif step == KEY_RIGHT:
                binary_json_string = writing_json("right")
                send_to_a_server(server_socket, binary_json_string)
                binary_json_string = writing_json("get_grid")
                time.sleep(0.01)
                send_to_a_server(server_socket, binary_json_string)
                time.sleep(0.01)
                server_json_string = server_socket.recv(1024**3).decode("utf-8")
                loaded_json_string = json.loads(server_json_string)
                break
            else:
                pass
            binary_json_string = writing_json("get_grid")
            send_to_a_server(server_socket, binary_json_string)
            time.sleep(0.01)
            server_json_string = server_socket.recv(1024**3).decode("utf-8")
            loaded_json_string = json.loads(server_json_string)
            break
        json_parse(loaded_json_string)
        endwin()
        print(snakeparts)
        print(apples)
        draw_field_multiplayer(stdscr, x_size, y_size)
        draw_objects(stdscr, snakeparts, apples)
        continue


# All singleplayer gameplay
def gameplay(stdscr):
    global do_i_need_to_ask_the_step
    global SnakeParts
    h, w = stdscr.getmaxyx()
    apple_y = random.randint(2, h - 3)
    apple_x = random.randint(2, w - 3)
    stdscr.addstr(apple_y, apple_x, '{}'.format(char_of_apple), color_pair(color_of_apple))
    do_i_need_to_ask_the_step = 0
    snake_y = random.randint(2, h - 3)
    snake_x = random.randint(2, w - 3)
    stdscr.addstr(snake_y, snake_x, '{}'.format(char_of_snake), color_pair(color_of_snake))
    SnakeParts.append([snake_y, snake_x, ''])
    while True:
        global step
        if do_i_need_to_ask_the_step == 0:
            step = stdscr.getch()
        if step == KEY_UP:
            SnakeParts[0] = [SnakeParts[0][0], SnakeParts[0][1], 'Up']
        elif step == KEY_DOWN:
            SnakeParts[0] = [SnakeParts[0][0], SnakeParts[0][1], 'Down']
        elif step == KEY_RIGHT:
            SnakeParts[0] = [SnakeParts[0][0], SnakeParts[0][1], 'Right']
        elif step == KEY_LEFT:
            SnakeParts[0] = [SnakeParts[0][0], SnakeParts[0][1], "Left"]
        else:
            continue
        drawing_first_element(stdscr, apple_y, apple_x)
        while True:
            halfdelay(1)
            step = stdscr.getch()
            if SnakeParts[0][2] == 'Up':
                if step == KEY_RIGHT or step == KEY_LEFT:
                    do_i_need_to_ask_the_step = 1
                    break
            elif SnakeParts[0][2] == 'Down':
                if step == KEY_RIGHT or step == KEY_LEFT:
                    do_i_need_to_ask_the_step = 1
                    break
            elif SnakeParts[0][2] == 'Right':
                if step == KEY_UP or step == KEY_DOWN:
                    do_i_need_to_ask_the_step = 1
                    break
            elif SnakeParts[0][2] == "Left":
                if step == KEY_UP or step == KEY_DOWN:
                    do_i_need_to_ask_the_step = 1
                    break
            if len(SnakeParts) == 1:
                if SnakeParts[0][0] == apple_y and SnakeParts[0][1] == apple_x:
                    SnakeParts.append([SnakeParts[0][0], SnakeParts[0][1]])
                    h, w = stdscr.getmaxyx()
                    apple_y = random.randint(2, h - 3)
                    apple_x = random.randint(2, w - 3)
                    stdscr.addstr(apple_y, apple_x, '{}'.format(char_of_apple), color_pair(color_of_apple))
                    stdscr.addstr(SnakeParts[0][0], SnakeParts[0][1], '{}'.format(char_of_snake),
                                  color_pair(color_of_snake))
                    stdscr.addstr(2, 3, 'Score : {}'.format(len(SnakeParts) - 1))
                    stdscr.refresh()
                if SnakeParts[0][2] == 'Up':
                    SnakeParts[0][0] -= 1
                    if SnakeParts[0][0] == 1:
                        using_lose_menu(stdscr)
                elif SnakeParts[0][2] == 'Down':
                    SnakeParts[0][0] += 1
                    if SnakeParts[0][0] == h - 2:
                        using_lose_menu(stdscr)
                elif SnakeParts[0][2] == 'Right':
                    SnakeParts[0][1] += 1
                    if SnakeParts[0][1] == w - 1:
                        using_lose_menu(stdscr)
                else:
                    SnakeParts[0][1] -= 1
                    if SnakeParts[0][1] == 1:
                        using_lose_menu(stdscr)
                square_for_steps(stdscr)
                stdscr.addstr(SnakeParts[0][0], SnakeParts[0][1], '{}'.format(char_of_snake),
                              color_pair(color_of_snake))
                stdscr.addstr(apple_y, apple_x, '{}'.format(char_of_apple), color_pair(color_of_apple))
                stdscr.addstr(2, 3, 'Score : {}'.format(len(SnakeParts) - 1))
                stdscr.refresh()
                continue
            else:
                i = len(SnakeParts) - 1
                suicide = {}
                for i in range(1, len(SnakeParts)):
                    suicide[SnakeParts[i][0]] = SnakeParts[i][1]
                if SnakeParts[0][0] == apple_y and SnakeParts[0][1] == apple_x:
                    SnakeParts.append([SnakeParts[0][0], SnakeParts[0][1]])
                    h, w = stdscr.getmaxyx()
                    apple_y = random.randint(2, h - 3)
                    apple_x = random.randint(2, w - 3)
                    stdscr.addstr(apple_y, apple_x, '{}'.format(char_of_apple), color_pair(color_of_apple))
                    stdscr.addstr(SnakeParts[0][0], SnakeParts[0][1], '{}'.format(char_of_snake),
                                  color_pair(color_of_snake))
                    stdscr.addstr(2, 3, 'Score : {}'.format(len(SnakeParts) - 1))
                    stdscr.refresh()
                square_for_steps(stdscr)
                while i != 0:
                    SnakeParts[i][0] = SnakeParts[i - 1][0]
                    SnakeParts[i][1] = SnakeParts[i - 1][1]
                    stdscr.addstr(SnakeParts[i][0], SnakeParts[i][1], '{}'.format(char_of_snake),
                                  color_pair(color_of_snake))
                    i -= 1
                    continue
                if SnakeParts[0][2] == 'Up':
                    SnakeParts[0][0] -= 1
                    if SnakeParts[0][0] == 1:
                        using_lose_menu(stdscr)
                elif SnakeParts[0][2] == 'Down':
                    SnakeParts[0][0] += 1
                    if SnakeParts[0][0] == h - 2:
                        using_lose_menu(stdscr)
                elif SnakeParts[0][2] == 'Right':
                    SnakeParts[0][1] += 1
                    if SnakeParts[0][1] == w - 1:
                        using_lose_menu(stdscr)
                else:
                    SnakeParts[0][1] -= 1
                    if SnakeParts[0][1] == 1:
                        using_lose_menu(stdscr)
                if SnakeParts[0][0] in suicide.keys() and SnakeParts[0][1] in suicide.values():
                    using_lose_menu(stdscr)
                stdscr.addstr(SnakeParts[0][0], SnakeParts[0][1], '{}'.format(char_of_snake),
                              color_pair(color_of_snake))
                stdscr.addstr(apple_y, apple_x, '{}'.format(char_of_apple), color_pair(color_of_apple))
                stdscr.addstr(2, 3, 'Score : {}'.format(len(SnakeParts) - 1))
                stdscr.refresh()
                continue
        continue


def mainfunc(stdscr):
    use_default_colors()
    init_pair(1, COLOR_RED, COLOR_BLACK)
    init_pair(2, COLOR_WHITE, COLOR_BLACK)
    init_pair(3, COLOR_CYAN, COLOR_BLACK)
    init_pair(4, COLOR_MAGENTA, COLOR_BLACK)
    init_pair(5, COLOR_GREEN, COLOR_BLACK)
    init_pair(6, COLOR_YELLOW, COLOR_BLACK)
    init_pair(7, COLOR_BLUE, COLOR_BLACK)
    init_pair(8, COLOR_BLACK, COLOR_WHITE)
    curs_set(False)
    current_row_idx = 0
    while True:
        start_menu(stdscr, current_row_idx)
        key = stdscr.getch()
        if key == KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key in [10, 13]:
            if menu[current_row_idx] == "PLAY":
                stdscr.clear()
                make_square(stdscr)
                gameplay(stdscr)
                endwin()
                sys.exit()
            if menu[current_row_idx] == "PLAY MULTIPLAYER":
                multiplayer_gameplay(stdscr)
            elif menu[current_row_idx] == "OPTIONS":
                current_row_idx = 0
                while True:
                    global char_of_snake
                    global char_of_apple
                    global color_of_snake
                    global color_of_apple
                    stdscr.clear()
                    options_menu(stdscr, current_row_idx)
                    key = stdscr.getch()
                    if key == KEY_UP and current_row_idx > 0:
                        current_row_idx -= 1
                    elif key == KEY_DOWN and current_row_idx < len(menu3) - 1:
                        current_row_idx += 1
                    elif key in [10, 13]:
                        if menu3[current_row_idx] == "Back":
                            current_row_idx = 0
                            break
                        elif menu3[current_row_idx] == "Char of snake: ":
                            options_menu(stdscr, current_row_idx)
                            stdscr.addstr(y - 4, x + 25,
                                          "(Enter a char what do you want to use, if you don`t want to change a char just press enter)")
                            char = stdscr.getch()
                            if char in [10, 13]:
                                pass
                            else:
                                char_of_snake = chr(char)
                        elif menu3[current_row_idx] == "Char of apple: ":
                            options_menu(stdscr, current_row_idx)
                            stdscr.addstr(y - 3, x + 25,
                                          "(Enter a char what do you want to use, if you don`t want to change a char just press enter)")
                            char = stdscr.getch()
                            if char in [10, 13]:
                                pass
                            else:
                                char_of_apple = chr(char)
                        elif menu3[current_row_idx] == "Color of snake: ":
                            options_menu(stdscr, current_row_idx)
                            stdscr.addstr(y - 1, x + 25,
                                          "Choose one of the option(enter a number of color), if you don`t want to change color just press enter\n"
                                          "1. Red\n"
                                          "2. White\n"
                                          "3. Cyan\n"
                                          "4. Magenta\n"
                                          "5. Green\n"
                                          "6. Yellow\n"
                                          "7. Blue")
                            color = stdscr.getch()
                            if color in [10, 13]:
                                pass
                            elif int(chr(color)) > 7 or int(chr(color)) < 1:
                                pass
                            else:
                                color_of_snake = chr(color)
                                color_of_snake = int(color_of_snake)
                        elif menu3[current_row_idx] == "Color of apple: ":
                            options_menu(stdscr, current_row_idx)
                            stdscr.addstr(y - 1, x + 25,
                                          "Choose one of the option(enter a number of color), if you don`t want to change color just press enter\n"
                                          "1. Red\n"
                                          "2. White\n"
                                          "3. Cyan\n"
                                          "4. Magenta\n"
                                          "5. Green\n"
                                          "6. Yellow\n"
                                          "7. Blue")
                            color = stdscr.getch()
                            if color in [10, 13]:
                                pass
                            elif int(chr(color)) > 7 or int(chr(color)) < 1:
                                pass
                            else:
                                color_of_apple = chr(color)
                                color_of_apple = int(color_of_apple)
                    stdscr.refresh()
                    continue
                continue
            else:
                endwin()
                sys.exit()
        stdscr.refresh()


wrapper(mainfunc)
