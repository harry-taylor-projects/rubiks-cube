import pygame
import math


def rotate_square(x_theta, y_theta):
    for vertex in range(8):
        # y rotation
        x = math.cos(y_theta) * (vertices[vertex][0] - 300) + math.sin(y_theta) * (vertices[vertex][2] - 300) + 300
        vertices[vertex][2] = math.cos(y_theta) * (vertices[vertex][2] - 300) - math.sin(y_theta) * (vertices[vertex][0] - 300) + 300

        # x rotation
        y = math.cos(x_theta) * (vertices[vertex][1] - 300) + math.sin(x_theta) * (vertices[vertex][2] - 300) + 300
        z = math.cos(x_theta) * (vertices[vertex][2] - 300) - math.sin(x_theta) * (vertices[vertex][1] - 300) + 300

        vertices[vertex] = [x, y, z]


def draw_line(start, end):
    length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    jump_distance = pixel / 2
    if length != 0:
        iterations = length / jump_distance
        x_change = (end[0] - start[0]) / iterations
        y_change = (end[1] - start[1]) / iterations
        for count in range(math.floor(iterations)):
            pygame.draw.rect(screen, [0, 0, 0], (pixel * ((start[0] + (count * x_change)) // pixel), pixel * ((start[1] + (count * y_change)) // pixel), pixel, pixel))


def draw_face(start, end, shift, colour):
    length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    shift_length = math.sqrt((shift[0] - start[0]) ** 2 + (shift[1] - start[1]) ** 2)
    jump_distance = pixel / 2
    if shift_length != 0:
        shift_iterations = shift_length / jump_distance
        shift_change = (shift[0] - start[0]) / shift_iterations, (shift[1] - start[1]) / shift_iterations
        for count in range(1, math.floor(shift_iterations)):
            if length != 0:
                iterations = length / jump_distance
                change = (end[0] - start[0]) / iterations, (end[1] - start[1]) / iterations
                for step in range(1, math.floor(iterations)):
                    x = pixel * ((start[0] + (step * change[0]) + (count * shift_change[0])) // pixel)
                    y = pixel * ((start[1] + (step * change[1]) + + (count * shift_change[1])) // pixel)
                    pygame.draw.rect(screen, colour, (x, y, pixel, pixel))


# initialise game
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

vertices = [[150, 150, 150], [450, 150, 150], [150, 450, 150], [450, 450, 150],
            [150, 150, 450], [450, 150, 450], [150, 450, 450], [450, 450, 450]]
adjacency = [[False, True, True, False, True, False, False, False],
             [True, False, False, True, False, True, False, False],
             [True, False, False, True, False, False, True, False],
             [False, True, True, False, False, False, False, True],
             [True, False, False, False, False, True, True, False],
             [False, True, False, False, True, False, False, True],
             [False, False, True, False, True, False, False, True],
             [False, False, False, True, False, True, True, False]]

on_face = [[True, True, True, True, False, False, False, False],
           [True, True, False, False, True, True, False, False],
           [True, False, True, False, True, False, True, False],
           [False, False, False, False, True, True, True, True],
           [False, False, True, True, False, False, True, True],
           [False, True, False, True, False, True, False, True]]

# green, yellow, red, blue, white, orange
faces = [[0, 1, 2], [0, 1, 4], [0, 2, 4], [4, 5, 6], [2, 3, 6], [1, 3, 5]]
face_colour = [[0, 255, 0], [255, 255, 0], [255, 0, 0], [0, 0, 255], [255, 255, 255], [255, 120, 0]]

# pixel size
pixel = 4

# dimension is 3 for 3x3 Rubik's Cube
dimension = 3

# rotation
x_angle = 0
y_angle = 0

# mouse info
down = False
last_pos = None

# run the game
run = True
while run:
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 600, 600))

    # furthest vertex isn't visible
    furthest_vertex = 0
    distance = 0
    for i in range(8):
        if vertices[i][2] > distance:
            furthest_vertex = i
            distance = vertices[i][2]

    # draw faces
    for face in range(6):
        if not on_face[face][furthest_vertex]:
            first, second, third = vertices[faces[face][0]], vertices[faces[face][1]], vertices[faces[face][2]]
            draw_face(first, second, third, face_colour[face])

            # drawing inner lines
            axis = [[0, 0], [0, 0]]
            for i, horizontal, vertical in zip([0, 1], [third, second], [second, third]):
                axis[i][0] = (horizontal[0] - first[0]) / dimension
                axis[i][1] = (horizontal[1] - first[1]) / dimension
                for multiplier in range(1, dimension):
                    begin = [first[0] + multiplier * axis[i][0], first[1] + multiplier * axis[i][1]]
                    final = [vertical[0] + multiplier * axis[i][0], vertical[1] + multiplier * axis[i][1]]
                    draw_line(begin, final)

    # draw edges
    for first in range(8):
        for second in range(8):
            if adjacency[first][second] and first > second and furthest_vertex not in (first, second):
                draw_line(vertices[first], vertices[second])

    for event in pygame.event.get():
        # user clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            last_pos = pygame.mouse.get_pos()
            down = True

        # user releases click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            down = False

        # stops the game if user closes the window
        if event.type == pygame.QUIT:
            run = False

    # rotate cube if user drags mouse
    if down:
        current_pos = pygame.mouse.get_pos()
        dx = current_pos[0] - last_pos[0]
        dy = current_pos[1] - last_pos[1]
        x_angle = -dy / 200
        y_angle = -dx / 200
        last_pos = current_pos
    else:
        # rotation dampening
        x_angle *= 0.99
        y_angle *= 0.99

    rotate_square(x_angle, y_angle)
    pygame.display.update()

pygame.quit()
