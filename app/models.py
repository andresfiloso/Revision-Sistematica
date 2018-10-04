#######################
##### Proyecto.py #####
#######################

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

  def setProyecto(self, proyecto):
    self.proyecto = proyecto

  def getDescripcion(self):
    return self.descripcion

  def setDescripcion(self, descripcion):
    self.descripcion = descripcion

  def getInclusion(self):
    return self.inclusion

  def setInclusion(self, inclusion):
    self.inclusion = inclusion

  def getExclusion(self):
    return self.exclusion

  def setExlcusion(self, exclusion):
    self.exclusion = exclusion


#######################
##### Usuario.py ######
#######################

class Usuario:
  def __init__(self, idUsuario, usuario, password, email):
    self.idUsuario = idUsuario
    self.usuario = usuario
    self.password = password
    self.email = email

  def getIdUsuario(self):
    return self.idUsuario

  def setIdUsuario(self, idUsuario):
    self.idUsuario = idUsuario

  def getUsuario(self):
    return self.usuario

  def setUsuario(self, usuario):
    self.usuario = usuario

  def getPassword(self):
    return self.password

  def setPassword(self, password):
    self.password = password

  def getEmail(self):
    return self.email

  def setEmail(self, email):
    self.email = email

