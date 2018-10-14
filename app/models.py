from datetime import datetime

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

  def __repr__(self):
    return "Esto seria un proyecto"
  def __str__(self):
    return "[" + str(self.getIdProyecto()) + ", " + self.getProyecto() + ", " + self.getDescripcion() + ", " +  self.getInclusion() + ", " +  self.getExclusion() + "]"


#######################
##### Usuario.py ######
#######################

class Usuario:
  def __init__(self, idUsuario, usuario, email):
    self.idUsuario = idUsuario
    self.usuario = usuario
    self.email = email

  def getIdUsuario(self):
    return self.idUsuario

  def setIdUsuario(self, idUsuario):
    self.idUsuario = idUsuario

  def getUsuario(self):
    return self.usuario

  def setUsuario(self, usuario):
    self.usuario = usuario

  def getEmail(self):
    return self.email

  def setEmail(self, email):
    self.email = email

  def __repr__(self):
    return "Esto seria un usuario"
  def __str__(self):
    return "[" + str(self.getIdUsuario()) + ", " + self.getUsuario() + ", " +  self.getEmail() + "]"


#######################
### Transaccion.py ####
#######################

class Transaccion:
  def __init__(self, idTransaccion, transaccion, tipoTransaccion, fechahora, proyecto, usuario):
    self.idTransaccion = idTransaccion
    self.transaccion = transaccion
    self.tipoTransaccion = tipoTransaccion
    self.fechahora = fechahora
    self.proyecto = proyecto
    self.usuario = usuario

  def getIdTransaccion(self):
    return self.idTransaccion

  def getTransaccion(self):
    return self.transaccion

  def getTipoTransaccion(self):
    return self.tipoTransaccion

  def getFechahora(self):
    return self.fechahora

  def getFechahoraFormat(self):
    
    datetime_object = datetime.strptime(str(self.fechahora), '%Y-%m-%d %H:%M:%S')

    #print self.fechaHora.month

    now = datetime.now()
    ahora = now.strftime('%d/%m/%Y %H:%M')

    formatDate = datetime_object.strftime('%d/%m/%Y %H:%M')

    difYear = now.year - datetime_object.year
    difMonth = now.month - datetime_object.month
    difDay = now.day - datetime_object.day
    difHour = now.hour - datetime_object.hour
    difMinutos = now.minute - datetime_object.minute

    result = ""
    if(difYear == 0):
      if(difMonth == 0):
        if(difDay == 0):
          if(difHour == 0): #diferencia de algunos minutos
            result = "Hace " + str(difMinutos) + " minutos"
          else: # diferencia de + de 1 hora
            if(difHour == 1):
              result = "Hace " + str(difHour) + " hora"
            else:
              result = "Hace " + str(difHour) + " horas"
            if(difMinutos == 0): # diferencia de segundos
              result = "Hace algunos segundos"
        else:
          if(difDay == 1):
            result = "Hace " + str(difDay) + " dia"
          else:
            result = "Hace " + str(difDay) + " dias"
      else:
        if(difMonth == 1):
          result = "Hace " + str(difMonth) + " mes"
        else:
          result = "Hace " + str(difMonth) + " meses"
    else:
        if(difYear == 1):
          result = "Hace " + str(difYear) + " year"
        else:
           result = "Hace " + str(difYear) + " years"

    return result

  def getFechahoraFull(self):
    
    datetime_object = datetime.strptime(str(self.fechahora), '%Y-%m-%d %H:%M:%S')

    #print self.fechaHora.month

    formatDate = datetime_object.strftime('%d/%m/%Y %H:%M')


    return str(formatDate)

  def getProyecto(self):
    return self.proyecto

  def getUsuario(self):
    return self.usuario

  def __repr__(self):
    return "Esto seria una transaccion"
  def __str__(self):
    return "[" + str(self.transaccion()) + ", " + self.tipoTransaccion() + ", " +  self.fechahora() + "]"


#######################
##### Busqueda.py #####
#######################

class Busqueda:
  def __init__(self, idBusqueda, busqueda, fechahora, proyecto, usuario):
    self.idBusqueda = idBusqueda
    self.busqueda = busqueda
    self.fechahora = fechahora
    self.proyecto = proyecto
    self.usuario = usuario

  def getIdBusqueda(self):
    return self.idBusqueda

  def getBusqueda(self):
    return self.busqueda

  def getFechahora(self):
    return self.fechahora

  def getFechahoraFormat(self):
    
    datetime_object = datetime.strptime(str(self.fechahora), '%Y-%m-%d %H:%M:%S')

    #print self.fechaHora.month

    now = datetime.now()
    ahora = now.strftime('%d/%m/%Y %H:%M')

    formatDate = datetime_object.strftime('%d/%m/%Y %H:%M')

    difYear = now.year - datetime_object.year
    difMonth = now.month - datetime_object.month
    difDay = now.day - datetime_object.day
    difHour = now.hour - datetime_object.hour
    difMinutos = now.minute - datetime_object.minute

    result = ""
    if(difYear == 0):
      if(difMonth == 0):
        if(difDay == 0):
          if(difHour == 0): #diferencia de algunos minutos
            result = "Hace " + str(difMinutos) + " minutos"
          else: # diferencia de + de 1 hora
            if(difHour == 1):
              result = "Hace " + str(difHour) + " hora"
            else:
              result = "Hace " + str(difHour) + " horas"
            if(difMinutos == 0): # diferencia de segundos
              result = "Hace algunos segundos"
        else:
          if(difDay == 1):
            result = "Hace " + str(difDay) + " dia"
          else:
            result = "Hace " + str(difDay) + " dias"
      else:
        if(difMonth == 1):
          result = "Hace " + str(difMonth) + " mes"
        else:
          result = "Hace " + str(difMonth) + " meses"
    else:
        if(difYear == 1):
          result = "Hace " + str(difYear) + " year"
        else:
           result = "Hace " + str(difYear) + " years"

    return result

  def getFechahoraFull(self):
    
    datetime_object = datetime.strptime(str(self.fechahora), '%Y-%m-%d %H:%M:%S')

    #print self.fechaHora.month

    formatDate = datetime_object.strftime('%d/%m/%Y %H:%M')


    return str(formatDate)

  def getProyecto(self):
    return self.proyecto

  def getUsuario(self):
    return self.usuario

  def __repr__(self):
    return "Esto seria una busqueda"
  def __str__(self):
    return "[" + str(self.busqueda()) + ", " + self.fechahora() + "]"