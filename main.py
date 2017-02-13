# resources:
#  - http://pyopengl.sourceforge.net/context/tutorials/nehe6.html
#  - https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL.Image import open

def init():
    pygame.init()
    display = (1024, 768)
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

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )

        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        data = (texture, file)
        textures.append(data)

    return textures
    
def generate_qudratic():
    quadratic = gluNewQuadric()
    gluQuadricTexture(quadratic, GL_TRUE);
    return quadratic

def main(quadratic, textures):
    current_texture = 0
    size = 4
    #glTranslatef(0.0,0.0, -15.0)
    glTranslatef(0.0,0.0, -(size / 2))

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
            texture, file = data
            glBindTexture(GL_TEXTURE_2D, texture)
            print(file)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(0.1, 0, 1, 0)
        #glTranslatef(0.0,0.0, -0.001)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(0, -3.8, 0)
        glRotatef(-90, 1, 0, 0)
        #gluSphere(quadratic, 40, 140, 140)
        gluCylinder(quadratic, size, size, 8, 14, 14);
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)
    
init()
textures = generate_texture()
quadratic = generate_qudratic()
main(quadratic, textures)