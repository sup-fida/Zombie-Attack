from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
import time
start_time = time.time()
camera_pos = (0, 500, 500)  # Camera position for third-person view
field_ofview = 120  # Field of view for perspective
camera_last_target = [0, 0, 0]  
fixedpo = "third"  
cheat_mode = False
# Player state
player_pos = [0.0, 0.0, -3.0]
player_angle = 0.0
player_health = 3  #player 3 health point starting
game_over = False  
bullets = []  #store bullet list
bullet_speed = 1  #bulllet speed
max_bullet_range = 10.0  #range max

zombie_positions = [
    [3, 0, -5],
    [-3, 0, -2],
    [7, 0, 3]
]
zombie_health = [1, 1, 1]  #zombie health point starting with 1

killed_zombies = 0
show_go_ahead_msg = False
msg_start_time = 0

#crate
crates_collected = 0  #count
crate_pos = [0.0, 5.0, 0.0]  # Start above the ground
crate_falling = True  # Flag to indicate if the crate is falling
crate_collected = False  # Flag to indicate if crate is collected

obstacles= [
    (-13.5, -10.5, -8, -6),     # xmin,ymin,zmin,zmax
    (-10, -8, -14, -12),        
    (5, 7, -9, -7),             
    (-7.5, -4.5, 4, 6),         
    (2, 4, 8, 10),              
    (-3.5, -0.5, 5.5, 7.5),     
    (5.0, 7.0, -6.0, -4.0),     
    (-1, 1, -11, -9),           
    (-7, -4, -5, -3),           
    (3, 5, 4, 6),               
    (5.0, 7.0, 2.0, 4.0),       
    (-7.0, -5.0, -11.0, -9.0),  
    (7.0, 9.0, -0.5, 1.5),      
]

def shoot_bullet():
    global bullets
    bullet = {
        'position': player_pos.copy(),  # Start at player's position
        'direction': player_angle,  # Direction of the bullet
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
                        if cheat_mode:
                            zombie_health[i]=0
                        else:
                            zombie_health[i] -= 1
                            bullet['active'] = False
                            if zombie_health[i] <= 0:
                                zombie_positions[i] = None
                                killed_zombies += 1
                                if killed_zombies == 10:
                                    global show_go_ahead_msg, msg_start_time
                                    show_go_ahead_msg = True
                                    msg_start_time = glutGet(GLUT_ELAPSED_TIME)
                                spawn_new_zombies(2)
                                break

def spawn_new_zombies(num_zombies=2):
    global zombie_positions, zombie_health
    for _ in range(num_zombies):
        new_x = random.uniform(-10, 10)
        new_z = random.uniform(-10, 10)
        zombie_positions.append([new_x, 0, new_z])
        zombie_health.append(1)

def update_zombies():
    global zombie_positions, player_pos, player_health, game_over  # Must be first line
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
            if distance < 0.5:
                if not cheat_mode:  # Don't lose health in cheat mode
                    player_health -= 1
                    if player_health <= 0:
                        game_over = True


def display_go_ahead_message():
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    glRasterPos3f(-0.5, 1.5, 0.0)
    message = "GO AHEAD"
    for ch in message:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

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
    buffer = 0.3  # Player size 
    for (xmin, xmax, zmin, zmax) in obstacles:
        if (xmin - buffer < x < xmax + buffer) and (zmin - buffer < z < zmax + buffer):
            return True
    return False

def check_crate_collection():
    global crate_collected, crate_pos, crates_collected
    if crate_collected or crate_falling:
        return
    distance = math.sqrt(
        (player_pos[0] - crate_pos[0]) ** 2 +
        (player_pos[2] - crate_pos[2]) ** 2
    )
    collect_distance_threshold = 1.0
    if distance < collect_distance_threshold:
        crate_collected = True
        crates_collected += 1
        print(f"Crate collected! Total crates: {crates_collected}")

def setupCamera(fixedpo, player_pos, player_angle):
    """
    Sets up the camera based on the fixed position and player state.
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10, 8, 18, 0, 0, 0, 0, 1, 0)



def keyboard(key, x, y):
    global player_pos, player_angle, game_over, cheat_mode
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

    elif key == 'c':
        cheat_mode = not cheat_mode
        print("Cheat mode:", "ON" if cheat_mode else "OFF")  


    if not is_colliding(new_x, new_z):
        player_pos[0], player_pos[2] = new_x, new_z


def update_crate():
    global crate_pos, crate_falling
    if crate_falling:
        crate_pos[1] -= 0.15
        if crate_pos[1] <= 0:
            crate_pos[1] = 0
            crate_falling = False

def draw_crate():
    if crate_collected:
        return
    glPushMatrix()
    glTranslatef(crate_pos[0], crate_pos[1], crate_pos[2])
    glColor3f(0.8, 0.5, 0.2)
    glutSolidCube(1.0)
    glPopMatrix()

def display_counts():
    global killed_zombies, player_health, crates_collected
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1.0, 1.0, 1.0)
    x = 10
    y = 580
    def draw_text(x, y, text):
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    draw_text(x, y, f"Zombies Killed: {killed_zombies}")
    draw_text(x, y - 25, f"Player Health: {player_health}")
    draw_text(x, y - 50, f"Crates Collected: {crates_collected}")
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def showScreen():
    global camera_pos, field_ofview, camera_last_target, fixedpo, player_pos, player_angle,show_go_ahead_msg, msg_start_time
    r, g, b = daynightcolour()
    glClearColor(r, g, b, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # gluPerspective(45.0, 800 / 600, 0.1, 100.0)
    # glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()
    # gluLookAt(10, 8, 18, 0, 0, 0, 0, 1, 0)
    setupCamera(fixedpo, player_pos, player_angle)  # Configure camera perspective

    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(-20, 0, -20)
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glEnd()
    update_crate()
    draw_crate()
    check_crate_collection()
    
    #building
    draw_building(-12, 0, -7, 3, 4, 2)
    draw_building(-9, 0, -13, 2, 3, 2)
    draw_building(6, 0, -8, 2, 5, 2)
    draw_building(-6, 0, 5, 3, 2, 3)
    draw_building(3, 0, 9, 2, 2, 2)

    # Broken Cars
    draw_broken_car(-2.0, 0.0, 6.5)
    draw_broken_car(6.0, 0.0, -5.0)
    draw_broken_car(0.0, 0.0, -10.0)

    # Firepits
    draw_firepit(-5, 2, -3)
    draw_firepit(4, 0, 5)

    # Barricades
    draw_barricade(6.0, 0.0, 3.0)
    draw_barricade(-6.0, 0.0, -10.0)
    draw_barricade(8.0, 0.0, 0.5)

    display_counts()
    update_zombies()
    for pos in zombie_positions:
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
    if show_go_ahead_msg:
        current_time = glutGet(GLUT_ELAPSED_TIME)
        if current_time - msg_start_time < 5000:
            display_go_ahead_message()
        else:
            show_go_ahead_msg = False
    if game_over:
        display_game_over()
    glutSwapBuffers()

def reset_game():
    global player_health, game_over, zombie_positions, player_pos, player_angle, zombie_health, bullets, killed_zombies
    global show_go_ahead_msg, msg_start_time, crate_pos, crate_falling, crate_collected, crates_collected
    player_health = 3
    game_over = False
    player_pos = [0.0, 0.0, -3.0]
    player_angle = 0.0
    zombie_positions = [
        [3, 0, -5],
        [-3, 0, -2],
        [7, 0, 3]
    ]
    zombie_health = [1, 1, 1]
    bullets = []
    killed_zombies = 0
    show_go_ahead_msg = False
    msg_start_time = 0
    crate_pos = [0.0, 5.0, 0.0]
    crate_falling = True
    crate_collected = False
    crates_collected = 0

def display_game_over():
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos3f(-1.0, 1.0, 0.0)
    for char in "GAME OVER":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glRasterPos3f(-1.0, 0.5, 0.0)
    for char in "Press 'R' to Restart":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def daynightcolour():
    cycle_length = 15.0
    t = (time.time() - start_time) % cycle_length
    phase = t / cycle_length  
    day_color = [0.75, 0.70, 0.65] 
    dusk_color = [0.15, 0.13, 0.13]
    night_color = [0.05, 0.05, 0.1]

    if phase < 0.5:
        f = phase * 2
        r = day_color[0] * (1 - f) + dusk_color[0] * f
        g = day_color[1] * (1 - f) + dusk_color[1] * f
        b = day_color[2] * (1 - f) + dusk_color[2] * f
    else:
        f = (phase - 0.5) * 2
        r = dusk_color[0] * (1 - f) + night_color[0] * f
        g = dusk_color[1] * (1 - f) + night_color[1] * f
        b = dusk_color[2] * (1 - f) + night_color[2] * f

    return r, g, b


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Zombie Survival Arena")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()