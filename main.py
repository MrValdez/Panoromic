# resources:
#  - http://pyopengl.sourceforge.net/context/tutorials/nehe6.html
#  - https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/
#  - http://cyrille.rossant.net/2d-graphics-rendering-tutorial-with-pyopengl/
#  - http://stackoverflow.com/questions/9863969/updating-a-texture-in-opengl-with-glteximage2d/13248668#13248668
#  - http://stackoverflow.com/questions/3887636/how-to-manipulate-texture-content-on-the-fly/10702468#10702468
#  - https://wiki.tiker.net/PyCuda/Examples/GlInterop
#  - http://python-opengl-examples.blogspot.com/2009/04/render-to-texture.html
#  - https://groups.google.com/forum/#!topic/pyglet-users/0tjqel26oZU
#  - https://www.opengl.org/discussion_boards/showthread.php/139933-color-key-transparency

import os

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays.vbo import VBO
from OpenGL.GL.ARB.pixel_buffer_object import *

from PIL.Image import open

screen = None
resolution = (1024, 768)
def init():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "{},0".format(int(resolution[0]/6))
    pygame.init()
    global screen 
    pygame.display.set_mode(resolution, DOUBLEBUF | OPENGL)
    gluPerspective(45, (resolution[0]/resolution[1]), 0.1, 50.0)
    screen = pygame.Surface(resolution, pygame.SRCALPHA).convert_alpha()

    glFrontFace(GL_CCW)
    global NormalText
    NormalText = pygame.font.Font(None, 17)

def generate_texture():
    glEnable(GL_TEXTURE_2D)
    textures = []

    for file in ["bg_vh.jpg", "bg_h.jpg", "bg.jpg"]:
        im = open(file)
        try:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)

        for filter, filter_name in ((GL_NEAREST, "Nearest"),
                                    (GL_LINEAR,  "Linear")):
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

    create_pygame_surface_texture()
    return textures

def create_pygame_surface_texture():
    image = pygame.image.tostring (screen, "RGBA")
    image_size = screen.get_size()
 
    # generate a texture id
    global texture_display
    texture_display = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_display)

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, resolution[0], resolution[1], GL_RGBA, GL_UNSIGNED_BYTE, image)

def generate_qudratic():
    quadratic = gluNewQuadric()
    gluQuadricTexture(quadratic, GL_TRUE);
    return quadratic

def print(message):
    screen.fill([0, 0, 0, 0])
    output = NormalText.render(message, True, [255, 255, 255])
    screen.blit(output, [0, 0])

    create_pygame_surface_texture()

def main(quadratic, textures):
    current_texture = 0
    size = 4
    speed = 10
    auto_move = True    
    use_sphere = True
    rotate = [0, 0]

    print("Press SPACE to change texture. Press Q to toggle between Circle or Cylinder projection. Press Escape to exit.")

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
            print("{}. {}".format(file, filter_name))

        if keypress[pygame.K_q] and not prev_keypress[pygame.K_q]:
            use_sphere = not use_sphere

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        texture = textures[current_texture][0]
        glBindTexture(GL_TEXTURE_2D, texture)

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

        if 1:
            glBindTexture(GL_TEXTURE_2D, texture_display)

            glDisable(GL_DEPTH_TEST)
            glDepthMask(False)
            
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            #glViewport(0, 0, resolution[0], resolution[1])
            glLoadIdentity()
            glOrtho(0, 1, 1, 0, 0, 1)
            
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glEnable(GL_ALPHA_TEST)
            glAlphaFunc(GL_GREATER, 0)

            glEnable(GL_BLEND);
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glBlendFunc(GL_SRC_ALPHA, GL_DST_COLOR)

            glBegin(GL_TRIANGLE_STRIP)
            #glColor4f(0.5, 0.5, 1.0, 1.0)
            glTexCoord2f(0, 0)
            glVertex2i(0, 0)
            glTexCoord2f(1, 0)
            glVertex2i(1, 0)
            glTexCoord2f(0, 1)
            glVertex2i(0, 1)
            glTexCoord2f(1, 1)
            glVertex2i(1, 1)
            glEnd()

            glDisable(GL_ALPHA_TEST)
            
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

            glPopMatrix()
            glDepthMask(True)
            glEnable(GL_DEPTH_TEST)
        
        pygame.display.flip()
        pygame.time.wait(10)

init()
textures = generate_texture()
quadratic = generate_qudratic()
main(quadratic, textures)