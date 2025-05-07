from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
# Player state
player_pos = [0.0, 0.0, -3.0]
player_angle = 0.0
player_health = 3  # player have 3 health
game_over = False  # Game over 
bullets = []  # store bullets
bullet_speed = 1  # bullet speed
max_bullet_range = 10.0  #max renge
zombie_positions = [
    [3, 0, -5],
    [-3, 0, -2],
    [7, 0, 3]
]
zombie_health = [1, 1, 1]  #zombie starts with 1 health 
killed_zombies = 0
show_go_ahead_msg = False
msg_start_time = 0

obstacles = [
    (-8, -5, -5, -3),   # building 1
    (-5, -3, -10, -8),  # building 2
    (6, 8, -8, -6),     # building 3
    (0, 3, 5, 8),       # building 4
    (-3, -1, -9, -7),   # broken_car 1
    (2, 4, -3, -1),     # broken_car 2
    (-1, 1, -11, -9),   # broken_car 3
    (-3, -1, -4, -2),   # firepit 1
    (2, 4, 4, 6),       # firepit 2
    (2, 4, 0, 2),       # barricade 1
    (-6, -4, -8, -6),   # barricade 2
    (7, 9, -0.5, 2.5),  # barricade 3
]

def shoot_bullet():
    global bullets
    bullet = {
        'position': player_pos.copy(),  # start from player's position
        'direction': player_angle,  # direction of bullet
        'active': True
    }
    bullets.append(bullet)

def update_bullets():
    global bullets, zombie_positions, zombie_health, killed_zombies, show_go_ahead_msg, msg_start_time
    for bullet in bullets:
        if bullet['active']:
            bullet['position'][0] += bullet_speed * math.sin(math.radians(bullet['direction']))
            bullet['position'][2] += bullet_speed * math.cos(math.radians(bullet['direction']))
            if (bullet['position'][0]**2 + bullet['position'][2]**2) > max_bullet_range**2:
                bullet['active'] = False
            for i in range(len(zombie_positions)):
                if zombie_positions[i] is not None:
                    distance = math.sqrt((bullet['position'][0] - zombie_positions[i][0])**2 +
                                         (bullet['position'][2] - zombie_positions[i][2])**2)
                    if distance < 0.5:
                        zombie_health[i] -= 1
                        bullet['active'] = False
                        if zombie_health[i] <= 0:
                            zombie_positions[i] = None
                            killed_zombies += 1 #2 new zombies born after one die (Spawn)
                           
                            spawn_new_zombies(2)  # spawn 2 new zombies
                            break  # loop theke ber  hou 

def spawn_new_zombies(num_zombies=2):
    global zombie_positions, zombie_health
    for _ in range(num_zombies):
        new_x = random.uniform(-10, 10)
        new_z = random.uniform(-10, 10)
        zombie_positions.append([new_x, 0, new_z])
        zombie_health.append(1)

def update_zombies():
    global zombie_positions, player_pos, player_health, game_over
    zombie_speed = 0.002
    for i in range(len(zombie_positions)):
        if zombie_positions[i] is not None:
            if game_over:
                return
            direction_x = player_pos[0] - zombie_positions[i][0]
            direction_z = player_pos[2] - zombie_positions[i][2]
            distance = math.sqrt(direction_x**2 + direction_z**2)
            if distance > 0:
                zombie_positions[i][0] += (direction_x / distance) * zombie_speed
                zombie_positions[i][2] += (direction_z / distance) * zombie_speed
                if distance < 0.5:
                    player_health -= 1
                    if player_health <= 0:
                        game_over = True

def display_go_ahead_message(): 
    glColor3f(1.0, 1.0, 0.0)  
    glRasterPos3f(-0.5, 1.5, 0.0)
    message = "GO AHEAD"
    for ch in message:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

#drawing given by other
                        
def draw_building(x, y, z, w=2, h=3, d=1):
    glColor3f(0.25, 0.25, 0.25)  
    glPushMatrix()
    glTranslatef(x, y + h / 2.0, z)

    
    glBegin(GL_QUADS) 
    
    glVertex3f(-w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, h / 2, d / 2)
    glVertex3f(-w / 2, h / 2, d / 2)
   
    glVertex3f(-w / 2, -h / 2, -d / 2)
    glVertex3f(w / 2, -h / 2, -d / 2)
    glVertex3f(w / 2, h / 2, -d / 2)
    glVertex3f(-w / 2, h / 2, -d / 2)
    
    glVertex3f(-w / 2, -h / 2, -d / 2)
    glVertex3f(-w / 2, -h / 2, d / 2)
    glVertex3f(-w / 2, h / 2, d / 2)
    glVertex3f(-w / 2, h / 2, -d / 2)
    
    glVertex3f(w / 2, -h / 2, -d / 2)
    glVertex3f(w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, h / 2, d / 2)
    glVertex3f(w / 2, h / 2, -d / 2)
    
    glVertex3f(-w / 2, h / 2, -d / 2)
    glVertex3f(-w / 2, h / 2, d / 2)
    glVertex3f(w / 2, h / 2, d / 2)
    glVertex3f(w / 2, h / 2, -d / 2)
    
    glVertex3f(-w / 2, -h / 2, -d / 2)
    glVertex3f(-w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, -h / 2, -d / 2)
    glEnd()
    glPopMatrix()


def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_angle, 0, 1, 0)

    glColor3f(1.0, 0.8, 0.6) #head
    glPushMatrix()
    glTranslatef(0.0, 1.75, 0.0)
    gluSphere(gluNewQuadric(), 0.2, 10, 10)  
    glPopMatrix()


    glColor3f(1.0, 0.0, 0.0)  #torso
    glPushMatrix()
    glTranslatef(0.0, 1.1, 0.0)
    glBegin(GL_QUADS)
   
    glVertex3f(-0.3, -0.5, 0.2) #fron
    glVertex3f(0.3, -0.5, 0.2)
    glVertex3f(0.3, 0.5, 0.2)
    glVertex3f(-0.3, 0.5, 0.2)
    
    glVertex3f(-0.3, -0.5, -0.2) #back
    glVertex3f(0.3, -0.5, -0.2)
    glVertex3f(0.3, 0.5, -0.2)
    glVertex3f(-0.3, 0.5, -0.2)

    glVertex3f(-0.3, -0.5, 0.2) #left
    glVertex3f(-0.3, -0.5, -0.2)
    glVertex3f(-0.3, 0.5, -0.2)
    glVertex3f(-0.3, 0.5, 0.2)
    
    glVertex3f(0.3, -0.5, 0.2) #right
    glVertex3f(0.3, -0.5, -0.2)
    glVertex3f(0.3, 0.5, -0.2)
    glVertex3f(0.3, 0.5, 0.2)
    
    glVertex3f(-0.3, 0.5, 0.2) #top
    glVertex3f(0.3, 0.5, 0.2)
    glVertex3f(0.3, 0.5, -0.2)
    glVertex3f(-0.3, 0.5, -0.2)
    
    glVertex3f(-0.3, -0.5, 0.2) #bottom
    glVertex3f(0.3, -0.5, 0.2)
    glVertex3f(0.3, -0.5, -0.2)
    glVertex3f(-0.3, -0.5, -0.2)
    glEnd()
    glPopMatrix()

    
    glColor3f(1.0, 0.8, 0.6)  #right arm
    glPushMatrix()
    glTranslatef(0.15, 1.15, 0.25)
    glRotatef(-20, 1, 0, 0)   
    glRotatef(10, 0, 1, 0)          
    gluCylinder(gluNewQuadric(), 0.05, 0.05, 0.5, 10, 10)  
    glPopMatrix()

    
    glColor3f(0.2, 0.2, 0.2)  #gun
    glPushMatrix()
    glTranslatef(0.0, 1.25, 0.35) 
    glRotatef(0, 0, 1, 0)
    glBegin(GL_QUADS)

    glVertex3f(-0.1, -0.05, -0.2)
    glVertex3f(0.1, -0.05, -0.2)
    glVertex3f(0.1, 0.05, -0.2)
    glVertex3f(-0.1, 0.05, -0.2)
    
    glVertex3f(-0.1, -0.05, 0.2)
    glVertex3f(0.1, -0.05, 0.2)
    glVertex3f(0.1, 0.05, 0.2)
    glVertex3f(-0.1, 0.05, 0.2)
    
    glVertex3f(-0.1, -0.05, -0.2)
    glVertex3f(-0.1, 0.05, -0.2)
    glVertex3f(-0.1, 0.05, 0.2)
    glVertex3f(-0.1, -0.05, 0.2)
    
    glVertex3f(0.1, -0.05, -0.2)
    glVertex3f(0.1, 0.05, -0.2)
    glVertex3f(0.1, 0.05, 0.2)
    glVertex3f(0.1, -0.05, 0.2)
    
    glVertex3f(-0.1, 0.05, -0.2)
    glVertex3f(0.1, 0.05, -0.2)
    glVertex3f(0.1, 0.05, 0.2)
    glVertex3f(-0.1, 0.05, 0.2)
    
    glVertex3f(-0.1, -0.05, -0.2)
    glVertex3f(0.1, -0.05, -0.2)
    glVertex3f(0.1, -0.05, 0.2)
    glVertex3f(-0.1, -0.05, 0.2)
    glEnd()
    glPopMatrix()

    
    glColor3f(0.5, 0.3, 0.1)  #legs
    for dx in [-0.15, 0.15]:
        glPushMatrix()
        glTranslatef(dx, 0.4, 0.0)
        glRotatef(90, 1, 0, 0) 
        gluCylinder(gluNewQuadric(), 0.1, 0.1, 0.4, 10, 10)  
        glPopMatrix()

    
    glColor3f(1.0, 0.8, 0.6)  #leftarn
    glPushMatrix()
    glTranslatef(-0.35, 1.3, 0.0)
    gluCylinder(gluNewQuadric(), 0.05, 0.05, 0.5, 10, 10) 
    glPopMatrix()

    glPopMatrix()

def draw_zombie(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    glColor3f(0.6, 0.8, 0.6)  #head
    glPushMatrix()
    glTranslatef(0.0, 1.75, 0.0)  
    gluSphere(gluNewQuadric(), 0.25, 10, 10)  
    glPopMatrix()

   
    glColor3f(0.2, 0.4, 0.2)  #torso
    glPushMatrix()
    glTranslatef(0.0, 1.0, 0.0)  
    glBegin(GL_QUADS)
    
    glVertex3f(-0.25, -0.35, 0.15)
    glVertex3f(0.25, -0.35, 0.15)
    glVertex3f(0.25, 0.35, 0.15)
    glVertex3f(-0.25, 0.35, 0.15)

    glVertex3f(-0.25, -0.35, -0.15)
    glVertex3f(0.25, -0.35, -0.15)
    glVertex3f(0.25, 0.35, -0.15)
    glVertex3f(-0.25, 0.35, -0.15)
    
    glVertex3f(-0.25, -0.35, 0.15)
    glVertex3f(-0.25, -0.35, -0.15)
    glVertex3f(-0.25, 0.35, -0.15)
    glVertex3f(-0.25, 0.35, 0.15)
    
    glVertex3f(0.25, -0.35, 0.15)
    glVertex3f(0.25, -0.35, -0.15)
    glVertex3f(0.25, 0.35, -0.15)
    glVertex3f(0.25, 0.35, 0.15)
    
    glVertex3f(-0.25, 0.35, 0.15)
    glVertex3f(0.25, 0.35, 0.15)
    glVertex3f(0.25, 0.35, -0.15)
    glVertex3f(-0.25, 0.35, -0.15)

    glVertex3f(-0.25, -0.35, 0.15)
    glVertex3f(0.25, -0.35, 0.15)
    glVertex3f(0.25, -0.35, -0.15)
    glVertex3f(-0.25, -0.35, -0.15)
    glEnd()
    glPopMatrix()

    
    glColor3f(0.5, 0.3, 0.1)  #legs
    for dx in [-0.15, 0.15]:
        glPushMatrix()
        glTranslatef(dx, 0.4, 0.0)
        glRotatef(90, 1, 0, 0) 
        gluCylinder(gluNewQuadric(), 0.1, 0.1, 0.4, 10, 10) 
        glPopMatrix()

    
    glColor3f(0.6, 0.8, 0.6)  #arms
    for dx in [-0.35, 0.35]:
        glPushMatrix()
        glTranslatef(dx, 1.2, 0.0)
        glRotatef(20 if dx < 0 else -20, 0, 0, 1)  
        gluCylinder(gluNewQuadric(), 0.05, 0.05, 0.5, 10, 10) 
        glPopMatrix()

    glPopMatrix()

def draw_broken_car(x, y, z):
    glPushMatrix()
    glTranslatef(x, y + 0.25, z)  

    glColor3f(0.4, 0.0, 0.0) #body
    glBegin(GL_QUADS)
    
    glVertex3f(-0.5, 0.0, 0.3)
    glVertex3f(0.5, 0.0, 0.3)
    glVertex3f(0.5, 0.3, 0.3)
    glVertex3f(-0.5, 0.3, 0.3)
    
    glVertex3f(-0.5, 0.0, -0.3)
    glVertex3f(0.5, 0.0, -0.3)
    glVertex3f(0.5, 0.3, -0.3)
    glVertex3f(-0.5, 0.3, -0.3)
    
    glVertex3f(-0.5, 0.0, -0.3)
    glVertex3f(-0.5, 0.0, 0.3)
    glVertex3f(-0.5, 0.3, 0.3)
    glVertex3f(-0.5, 0.3, -0.3)
    
    glVertex3f(0.5, 0.0, -0.3)
    glVertex3f(0.5, 0.0, 0.3)
    glVertex3f(0.5, 0.3, 0.3)
    glVertex3f(0.5, 0.3, -0.3)
    
    glVertex3f(-0.5, 0.3, -0.3)
    glVertex3f(0.5, 0.3, -0.3)
    glVertex3f(0.5, 0.3, 0.3)
    glVertex3f(-0.5, 0.3, 0.3)
    
    glVertex3f(-0.5, 0.0, -0.3)
    glVertex3f(0.5, 0.0, -0.3)
    glVertex3f(0.5, 0.0, 0.3)
    glVertex3f(-0.5, 0.0, 0.3)
    glEnd()

    
    glColor3f(0.2, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.5, 0.3, 0.0)
    glVertex3f(0.5, 0.3, 0.0)
    glVertex3f(0.0, 0.5, 0.0)
    glEnd()

    glPopMatrix()

def draw_firepit(x, y, z, radius=0.5, height=0.2): 
    slices = 16  
    glColor3f(0.5, 0.5, 0.5)  #ring
    glPushMatrix()
    glTranslatef(x, y, z) 

    glBegin(GL_QUAD_STRIP) #circular
    for i in range(slices + 1):
        angle = math.radians(i * (360 / slices))
        x_offset = math.cos(angle) * radius
        z_offset = math.sin(angle) * radius
        glVertex3f(x_offset, height / 2, z_offset)
        glVertex3f(x_offset, -height / 2, z_offset)
    glEnd()

    
    glColor3f(0.0, 0.0, 0.0)  #empty space inside firepit
    glPushMatrix()
    gluCylinder(gluNewQuadric(), 0.1, 0.1, height, slices, 1)  # Small cylinder for the pit's depth
    glPopMatrix()

    
    glColor3f(1.0, 0.5, 0.0)  #fire flames
    glPushMatrix()
    glTranslatef(0, height + 0.3, 0) #fire inside pit
    glRotatef(90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 0.1, 0.4, 0.6, slices, 1)  
    glPopMatrix()

    glPopMatrix()

def draw_barricade(x, y, z, w=2, h=1, d=0.5):
    glColor3f(0.36, 0.25, 0.20) 
    glPushMatrix()
    glTranslatef(x, y + h / 2.0, z)

    
    glBegin(GL_QUADS)

    glVertex3f(-w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, h / 2, d / 2)
    glVertex3f(-w / 2, h / 2, d / 2)


    glVertex3f(-w / 2, -h / 2, -d / 2)
    glVertex3f(w / 2, -h / 2, -d / 2)
    glVertex3f(w / 2, h / 2, -d / 2)
    glVertex3f(-w / 2, h / 2, -d / 2)


    glVertex3f(-w / 2, -h / 2, -d / 2)
    glVertex3f(-w / 2, -h / 2, d / 2)
    glVertex3f(-w / 2, h / 2, d / 2)
    glVertex3f(-w / 2, h / 2, -d / 2)


    glVertex3f(w / 2, -h / 2, -d / 2)
    glVertex3f(w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, h / 2, d / 2)
    glVertex3f(w / 2, h / 2, -d / 2)


    glVertex3f(-w / 2, h / 2, -d / 2)
    glVertex3f(-w / 2, h / 2, d / 2)
    glVertex3f(w / 2, h / 2, d / 2)
    glVertex3f(w / 2, h / 2, -d / 2)


    glVertex3f(-w / 2, -h / 2, -d / 2)
    glVertex3f(-w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, -h / 2, d / 2)
    glVertex3f(w / 2, -h / 2, -d / 2)
    glEnd()

    glPopMatrix()

def is_colliding(x, z):
    buffer = 0.3  # player size or buffer zone
    for (xmin, xmax, zmin, zmax) in obstacles:
        if (xmin - buffer < x < xmax + buffer) and (zmin - buffer < z < zmax + buffer):
            return True
    return False

def keyboard(key, x, y):
    global player_pos, player_angle, game_over
    move_speed = 0.4
    rotate_speed = 15
    key = key.decode("utf-8").lower()
    new_x, new_z = player_pos[0], player_pos[2]
    
    if game_over:
        if key == 'r':
            reset_game()
            return
    
    if key == 'w': #FORWARDdddd
        new_x -= move_speed * math.sin(math.radians(player_angle))
        new_z -= move_speed * math.cos(math.radians(player_angle))
    
   
    elif key == 's': #BACKWARDdd
        new_x += move_speed * math.sin(math.radians(player_angle))
        new_z += move_speed * math.cos(math.radians(player_angle))
    
   
    elif key == 'a': #LEFT rotation
        player_angle += rotate_speed
    
 
    elif key == 'd': #RIGHT rotation
        player_angle -= rotate_speed
    
    # Shoot bullet
    elif key == ' ':
        shoot_bullet()
    
    
    elif key == 'l': # Move left 
        new_x -= move_speed  
    
   
    elif key == 'j': # Move right
        new_x += move_speed  


    if not is_colliding(new_x, new_z):
        player_pos[0], player_pos[2] = new_x, new_z



def showScreen():
    global show_go_ahead_msg, msg_start_time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10, 8, 18, 0, 0, 0, 0, 1, 0)
    # Ground
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(-20, 0, -20)
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glEnd()
    # Buildings
    draw_building(-8, 0, -5, 3, 4, 2)
    draw_building(-5, 0, -10, 2, 3, 2)
    draw_building(6, 0, -8, 2, 5, 2)
    draw_building(0, 0, 5, 3, 2, 3)
    # Broken Cars
    draw_broken_car(-2.0, 0.0, -8.0)
    draw_broken_car(3.0, 0.0, -2.0)
    draw_broken_car(0.0, 0.0, -10.0)
    # Firepits
    draw_firepit(-2, 0, -3)
    draw_firepit(3, 0, 5)
    # Barricades
    draw_barricade(3.0, 0.0, 1.0)
    draw_barricade(-5.0, 0.0, -7.0)
    draw_barricade(8.0, 0.0, 0.5)
    # Display counts
    display_counts()  # Call the display_counts function here
    # Update zombies' positions
    update_zombies()
    for i, pos in enumerate(zombie_positions):
        if pos is not None:
            draw_zombie(pos[0], pos[1], pos[2])
    
    update_bullets()
    for bullet in bullets:
        if bullet['active']:
            glPushMatrix()
            glTranslatef(bullet['position'][0], 0.1, bullet['position'][2])
            glColor3f(1.0, 1.0, 0.0)
            gluSphere(gluNewQuadric(), 0.05, 10, 10)
            glPopMatrix()
    
    draw_player()

    if show_go_ahead_msg: # display "GO AHEAD" message for 5 seconds after 10 zombies killed
        current_time = glutGet(GLUT_ELAPSED_TIME)
        if current_time - msg_start_time < 5000:  # 5000ms = 5 seconds
            display_go_ahead_message()
        else:
            show_go_ahead_msg = False  # message hariye jabe after 5 seconds
    
    if game_over:
        display_game_over()
    
    glutSwapBuffers()
def display_counts():
    global killed_zombies, player_health
    glColor3f(1.0, 1.0, 1.0)  # White color for text
    glRasterPos3f(-9.0, 9.0, 0.0)  # Position for the text
    for char in f"Zombies Killed: {killed_zombies}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glRasterPos3f(-9.0, 8.5, 0.0)  # Position for the health text
    for char in f"Player Health: {player_health}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def reset_game():
    global player_health, game_over, zombie_positions, player_pos, player_angle
    player_health = 3
    game_over = False
    player_pos = [0.0, 0.0, -3.0]  # reset player position
    player_angle = 0.0  # reset player angle
    zombie_positions = [
        [3, 0, -5],
        [-3, 0, -2],
        [7, 0, 3]
    ]
def display_game_over():
    glColor3f(1.0, 0.0, 0.0)  # Red color for game over text
    glRasterPos3f(-1.0, 1.0, 0.0)  #text position
    for char in "GAME OVER":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glRasterPos3f(-1.0, 0.5, 0.0)  # ยosition for the restart instruction
    for char in "Press 'R' to Restart":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Zombie Survival Arena")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(keyboard)
    glutMainLoop()
if __name__ == "__main__":
    main()