# resources:
#  - http://pyopengl.sourceforge.net/context/tutorials/nehe6.html
#  - https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/

import os

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL.Image import open

def init():
    display = (1024, 768)
    os.environ["SDL_VIDEO_WINDOW_POS"] = "{},0".format(int(display[0]/6))
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glFrontFace(GL_CCW)

def generate_texture():
    glEnable(GL_TEXTURE_2D)
    textures = []

    for file in ["bg.jpg", "bg_h.jpg", "bg_vh.jpg"]:
        im = open(file)
        try:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)

        for filter, filter_name in ((GL_LINEAR,  "Linear"),
                                    (GL_NEAREST, "Nearest")):
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            glTexImage2D(
                GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                GL_RGBA, GL_UNSIGNED_BYTE, image
            )

            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

            data = (texture, file, filter_name)
            textures.append(data)

    return textures
    
def generate_qudratic():
    quadratic = gluNewQuadric()
    gluQuadricTexture(quadratic, GL_TRUE);
    return quadratic

def main(quadratic, textures):
    current_texture = 0
    size = 4
    speed = 10
    auto_move = True    
    use_sphere = True
    rotate = [0, 0]
        
    keypress = pygame.key.get_pressed()
    while True:
        prev_keypress = keypress
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_ESCAPE]:
            pygame.quit()
            isRunning = False
            break
        if keypress[pygame.K_SPACE] and not prev_keypress[pygame.K_SPACE]:
            current_texture = (current_texture + 1) % len(textures)
            data = textures[current_texture]
            texture, file, filter_name = data
            glBindTexture(GL_TEXTURE_2D, texture)
            print(file, filter_name)

        if keypress[pygame.K_q] and not prev_keypress[pygame.K_q]:
            use_sphere = not use_sphere

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        #glTranslatef(0.0,0.0, -15.0)
        glTranslatef(0.0,0.0, -(size/2))  

        if auto_move:
            rotate[0] += 0.05

            if (keypress[pygame.K_LEFT] or
                keypress[pygame.K_RIGHT] or
                keypress[pygame.K_UP] or 
                keypress[pygame.K_DOWN]):
                auto_move = False
        else:
            if keypress[pygame.K_LEFT]:
                rotate[0] += -0.1
            if keypress[pygame.K_RIGHT]:
                rotate[0] += +0.1
            if keypress[pygame.K_UP]:
                rotate[1] += -0.1
            if keypress[pygame.K_DOWN]:
                rotate[1] += +0.1

        glRotatef(rotate[1] * speed, 1, 0, 0)
        glRotatef(rotate[0] * speed, 0, 1, 0)

        if use_sphere:
            glRotatef(-90, 1, 0, 0)
            glTranslatef(0, -size, 0)
            gluSphere(quadratic, size*2, 140, 140)
        else:
            glTranslatef(0, -size, 0)
            glRotatef(-90, 1, 0, 0)
            gluCylinder(quadratic, size, size, 8, 14, 14);
        
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)
    
init()
textures = generate_texture()
quadratic = generate_qudratic()
main(quadratic, textures)