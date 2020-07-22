import numpy as np
from math import *

class HyperObject:
  verts = []
  edges = []
  transform = np.identity(4)

  def __init__(self, verts, edges):
    self.verts = verts
    self.edges = edges

  def transformedVerts(self):
    ts = []
    for vert in self.verts:
      ts.append(np.matmul(self.transform, vert))
    return ts

  def projectedVerts(self):
    w_dist = 2
    proj = []
    transformed = self.transformedVerts()
    for v in transformed:
      w = 1 / (w_dist - v[3])
      #projection matrix
      m = np.array([[w, 0, 0, 0],
                     [0, w, 0, 0],
                     [0, 0, w, 0]])
      proj.append(np.matmul(m, v))
    return proj


def generateUnitTesseract():
  verts = []
  for i in range(0, 2**4):
    x = (i >> 0 & 1) - 0.5
    y = (i >> 1 & 1) - 0.5
    z = (i >> 2 & 1) - 0.5
    w = (i >> 3 & 1) - 0.5
    verts.append(np.array([x, y, z, w]))
  return verts

# edges are between points with unit distance
def generateTesseractEdges(verts):
  edges = []
  for i0 in range(len(verts)):
    for i1 in range(len(verts)):
      if i0 != i1 and np.linalg.norm(verts[i0] - verts[i1]) == 1.0:
        edges.append((i0, i1))
  return edges

class Tesseract(HyperObject):
  def __init__(self, scale=np.array([1,1,1,1])):
    verts = generateUnitTesseract()
    edges = generateTesseractEdges(verts)
    for vert in verts:
      vert *= scale
    super(Tesseract, self).__init__(verts, edges)


def rotateAroundPlane(ax1, ax2, angle):
  assert(ax1 < ax2)
  m = np.identity(4)
  m[ax1][ax1] = cos(angle)
  m[ax2][ax1] = sin(angle)
  m[ax1][ax2] = -sin(angle)
  m[ax2][ax2] = cos(angle)
  return m








