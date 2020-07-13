import numpy

from pyquaternion import Quaternion
import ctypes
import pygame
from pygame.locals import *
import pyglet
from pyglet.gl import *

from base import *


def drawObject(obj):
    proj = obj.projectedVerts()

    glPointSize(8.0)
    glBegin(GL_POINTS)
    glColor3fv((ctypes.c_float * 3)(*(1.0,1.0,1.0)))
    for vert in proj:
        glVertex3fv((ctypes.c_float * 3)(*vert))
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((ctypes.c_float * 3)(*(0.8,0.8,0.8)))
    for edge in obj.edges:
        for vertex in edge:
            glVertex3fv((ctypes.c_float * 3)(*proj[vertex]))
    glEnd()

def main():
    pygame.init()
    display = (1280,720)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # Using depth test to make sure closer colors are shown over further ones
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Default view
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.5, 40)
    glTranslatef(0.0,0.0,-17.5)

    cube = Tesseract()

    angle = 0
    accum = Quaternion(1, 0, 0, 0)
    inc_x = 0
    inc_y = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                #Rotating about the x axis
                if event.key == pygame.K_UP:
                    inc_x =  pi/100
                if event.key == pygame.K_DOWN:
                    inc_x = -pi/100

                # Rotating about the y axis
                if event.key == pygame.K_LEFT:
                    inc_y =  pi/100
                if event.key == pygame.K_RIGHT:
                    inc_y = -pi/100

                # Reset to default view
                if event.key == pygame.K_SPACE:
                    accum = (1,0,0,0)

            if event.type == pygame.KEYUP:
                # Stoping rotation
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    inc_x = 0.0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    inc_y = 0.0

        rot_x = Quaternion(axis=[1.0,0.0,0.0], angle=inc_x)
        rot_y = Quaternion(axis=[0.0,1.0,0.0], angle=inc_y)
        accum = accum * rot_x * rot_y 

        # dont judge me pls
        mat = accum.transformation_matrix.T
        m = tuple(mat.reshape(1, -1)[0])

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf((ctypes.c_float * 16)(*m))

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        angle += pi/120
        cube.transform = rotateAroundPlane(2, 3, angle)

        drawObject(cube)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
  main()

