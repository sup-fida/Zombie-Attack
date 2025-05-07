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
#Player state
player_pos = [0.0, 0.0, -3.0]
player_angle = 0.0
player_health = 3  #player 3 health point starting
game_over = False  
bullets = []  #store bullet list
bullet_speed = 1  #bulllet speed
max_bullet_range = 10.0  #range max

#Crate variables for falling crate feature
crates_collected = 0  #count
crate_pos = [0.0, 5.0, 0.0]  # Start above the ground
crate_falling = True  # Flag to indicate if the crate is falling
crate_collected = False  # Flag to indicate if crate is collected
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