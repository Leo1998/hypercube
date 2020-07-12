import numpy
from math import *
from pyquaternion import Quaternion

import ctypes
import pygame
from pygame.locals import *
import pyglet
from pyglet.gl import *

cube_verts = (
    (-3.0,-3.0, 3.0),
    (-3.0, 3.0, 3.0),
    ( 3.0, 3.0, 3.0),
    ( 3.0,-3.0, 3.0),
    (-3.0,-3.0,-3.0),
    (-3.0, 3.0,-3.0),
    ( 3.0, 3.0,-3.0),
    ( 3.0,-3.0,-3.0)
)

cube_edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,6),
    (5,1),
    (5,4),
    (5,6),
    (7,3),
    (7,4),
    (7,6)
)

def Cube():
    glPointSize(8.0)
    glBegin(GL_POINTS)
    glColor3fv((ctypes.c_float * 3)(*(1.0,1.0,1.0)))
    for vert in cube_verts:
        glVertex3fv((ctypes.c_float * 3)(*vert))
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((ctypes.c_float * 3)(*(0.8,0.8,0.8)))
    for edge in cube_edges:
        for vertex in edge:
            glVertex3fv((ctypes.c_float * 3)(*cube_verts[vertex]))
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

    accum = Quaternion()
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

        Cube()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
  main()






'''axis_verts = (
    (-7.5, 0.0, 0.0),
    ( 7.5, 0.0, 0.0),
    ( 0.0,-7.5, 0.0),
    ( 0.0, 7.5, 0.0),
    ( 0.0, 0.0,-7.5),
    ( 0.0, 0.0, 7.5)
)

axes = (
    (0,1),
    (2,3),
    (4,5)
)

axis_colors = (
    (1.0,0.0,0.0), # Red
    (0.0,1.0,0.0), # Green
    (0.0,0.0,1.0)  # Blue
)

cube_surfaces = (
    (0,1,2,3), # Front
    (3,2,6,7), # Right
    (7,6,5,4), # Left
    (4,5,1,0), # Back
    (1,5,6,2), # Top
    (4,0,3,7)  # Bottom
)


cube_colors = (
    (0.769,0.118,0.227), # Red
    (  0.0,0.318,0.729), # Blue
    (  1.0,0.345,  0.0), # Orange
    (  0.0, 0.62,0.376), # Green
    (  1.0,  1.0,  1.0), # White
    (  1.0,0.835,  0.0)  # Yellow
)

def Axis():
    glBegin(GL_LINES)
    for color,axis in zip(axis_colors,axes):
        glColor3fv((ctypes.c_float * 3)(*color))
        for point in axis:
            glVertex3fv((ctypes.c_float * 3)(*axis_verts[point]))
    glEnd()
'''
