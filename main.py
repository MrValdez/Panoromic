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
    #im = open("bg.jpg")
    #im = open("bg_h.jpg")
    im = open("bg_vh.jpg")

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

    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    quadratic = gluNewQuadric()
    gluQuadricTexture(quadratic, GL_TRUE);
    return quadratic

def main(quadratic):
    #glTranslatef(0.0,0.0, -15.0)

    while True:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            isRunning = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(0.1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        #gluSphere(quadratic, 40, 140, 140)
        glTranslatef(0, 0, -4)
        #gluCylinder(quadratic, 4, 4, 8, 14, 14);
        gluCylinder(quadratic, 4, 4, 8, 14, 14);
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)
    
init()
quadratic = generate_texture()
main(quadratic)