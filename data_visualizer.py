import pygame as pg
from pygame.locals import *
from math import cos, sin, radians

# path = "D:\data\latest.txt"
# data = r"D:\data\latest.txt"
data = r"latest.txt"
file = open(data, "r")
data = file.readlines()
file.close()

data.remove(data[0])
data.remove(data[0])
new_data = []

for line in data:
    d = []
    line = line.strip()
    line = line.split(", ")
    for num in line:
        d.append(float(num))
    new_data.append(d)

data = new_data

path = ((3551.8, 14866.6), (2959.0, 12979.0), (1663.6, 11467.9), (159.5, 10150.4), (-1285.3, 8769.8), (-2309.3, 7069.0), (-2580.1, 5110.7), (-2151.1, 3176.3), (-975.6, 1586.3), (578.7, 329.9), (2061.6, -1006.5), (3074.7, -2709.5), (3479.5, -4654.3), (3551.8, -5486.8))
# graph in mm is between (-1800, 1800) and (1800, -1800)
# width is 3600, 3600
# to 600, 600 we divide by 60

pg.init()
pg.font.init()
display_surface = pg.display.set_mode((600, 600), flags=RESIZABLE)
pg.display.set_caption("Data Visualizer 1.0")
font = pg.font.SysFont("arial", 12)

field_graphic = pg.image.load(r'field.png').convert()
field_graphic = pg.transform.scale(field_graphic, (600, 600))

running = True
current_index = 0
show_field = False
show_grid = False

def draw_data(data, row, center="topleft"):
    # centers: "topleft", "topright", "bottomleft"
    f = font.render(data, True, (255, 255, 255), (0, 0, 0))
    if center == "topleft":
        pos = (0, f.get_height()*row)
    if center == "topright":
        pos = (pg.display.get_window_size()[0] - f.get_width(), f.get_height()*row)
    if center == "bottomleft":
        pos = (0, pg.display.get_window_size()[1]-f.get_height())
    display_surface.blit(f, f.get_rect(topleft=pos))

def center_offset():
    return pg.Vector2((current_line[1]*2+300)-pg.display.get_window_size()[0]//2, (current_line[2]*2+300)-pg.display.get_window_size()[1]//2)

offset = pg.Vector2(-300, -300)
# drag = False

while running:
    display_surface.fill((0, 0, 0))
    current_line = data[current_index]
    mouse_buttons = pg.mouse.get_pressed()

    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                if event.mod == KMOD_LSHIFT:
                    offset=center_offset()
                if (current_index + 1) < len(data):
                    current_index += 1
            if event.key == K_LEFT:
                if event.mod == KMOD_LSHIFT:
                    offset=center_offset()
                if (current_index - 1) >= 0:
                    current_index -= 1
            if event.key == K_f:
                show_field = not show_field
            if event.key == K_g:
                show_grid = not show_grid
            if event.key == K_0 or event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4 or event.key == K_5 or event.key == K_6 or event.key == K_7 or event.key == K_8 or event.key == K_9 or event.key == K_0:
                num = int(event.unicode)
                current_index = int((num / 10) * len(data))
            if event.key == K_c:
                offset = center_offset()
        if event.type == MOUSEMOTION:
            if mouse_buttons[0]:
                offset -= event.rel
    
    if show_field:
        display_surface.blit(field_graphic, field_graphic.get_rect(center=(0, 0)-offset))
    if show_grid:
        for i in range(0, 7):
            i -= 3
            i*=100
            # vertical lines
            pg.draw.line(display_surface, (100, 100, 100), (i, -300)-offset, (i, 300)-offset)
        for i in range(0, 7):
            i -= 3
            i*=100
            # horizontal lines
            pg.draw.line(display_surface, (100, 100, 100), (-300, i)-offset, (300, i)-offset)

    for i, point in enumerate(path):
        if i == 0:
            color = (0, 255, 0)
        if i == len(path)-1:
            color = (255, 0, 0)
        else:
            color = (255//2, 255//2, 255//2)
        
        pg.draw.circle(display_surface, color, ((point[0]/60)-offset.x, (point[1]/60)-offset.y), 3)
    
    for i, point in enumerate(data):
        pg.draw.circle(display_surface, (255//2, 100, 100), ((point[1]*10/60)-offset.x, (point[2]*10/60)-offset.y), 3)

    pg.draw.circle(display_surface, (255, 255, 255), ((current_line[1]*10/60)-offset.x, (current_line[2]*10/60)-offset.y), 5)

    # draw heading line
    # red is for target, green is actual 
    # heading, heading_to_target is 3, 4
    # green line (actual heading)
    pointa = (current_line[1]*10/60, current_line[2]*10/60)
    pointb = (20*cos(radians(current_line[3])), 20*sin(radians(current_line[3])))
    pointb = (pointa[0]+pointb[0], pointa[1]+pointb[1])
    pg.draw.aaline(display_surface, (0, 255, 0), pointa-offset, pointb-offset)
    # red line (target heading)
    pointa = (current_line[1]*10/60, current_line[2]*10/60)
    pointb = (20*cos(radians(current_line[4])), 20*sin(radians(current_line[4])))
    pointb = (pointa[0]+pointb[0], pointa[1]+pointb[1])
    pg.draw.aaline(display_surface, (255, 0, 0), pointa-offset, pointb-offset)

    draw_data(f"Show field (F): {show_field}", 0, "topright")
    draw_data(f"Show grid (G): {show_grid}", 1, "topright")

    draw_data(f"Index: {current_index+1}/{len(data)}", 0)
    draw_data(f"Current time: {current_line[0]/1000}s", 1)
    draw_data(f"Current position: ({current_line[1]}, {current_line[2]})", 2)
    draw_data(f"Current heading: {current_line[3]}", 3)
    draw_data(f"Target heading: {current_line[4]}", 4)

    # draw_data(f"Mouse pos: {(pg.Vector2(pg.mouse.get_pos()) * 10/60) - offset}", 4, "bottomleft")
    pg.display.update()