#!/usr/bin/python
# -*- coding: utf-8 -*-

class Proyecto:
  def __init__(self, idProyecto, proyecto, descripcion, inclusion, exclusion):
    self.idProyecto = idProyecto
    self.proyecto = proyecto
    self.descripcion = descripcion
    self.inclusion = inclusion
    self.exclusion = exclusion

  def getIdProyecto(self):
    return self.idProyecto

  def setIdProyecto(self, idProyecto):
    self.idProyecto = idProyecto

  def getProyecto(self):
    return self.proyecto

  def setProyecto(self, idProyecto):
    self.proyecto = proyecto

  def getDescripcion(self):
    return self.descripcion

  def setDescripcion(self, idProyecto):
    self.descripcion = descripcion

  def getInclusion(self):
    return self.inclusion

  def setInclusion(self, idProyecto):
    self.inclusion = inclusion

  def getExclusion(self):
    return self.exclusion

  def setExlcusion(self, idProyecto):
    self.exclusion = exclusion