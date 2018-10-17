CREATE DATABASE rsdb;
USE rsdb;

CREATE TABLE Usuario (
	idUsuario INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	usuario VARCHAR(30) NOT NULL,
    pass VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE Proyecto (
	idProyecto INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	proyecto VARCHAR(120) NOT NULL,
    descripcion VARCHAR(145) NOT NULL,
    inclusion VARCHAR(145) NOT NULL,
    exclusion VARCHAR(145) NOT NULL,
    idUsuario INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_proyecto_usuario`
		FOREIGN KEY (idUsuario) REFERENCES Usuario (idUsuario)
		ON DELETE CASCADE
		ON UPDATE RESTRICT
) ENGINE = InnoDB;

CREATE TABLE Transaccion (
	idTransaccion INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	transaccion VARCHAR(120) NOT NULL,
    tipoTransaccion VARCHAR(20) NOT NULL,
    fechahora DATETIME NULL,
    idProyecto INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_transaccion_proyecto`
		FOREIGN KEY (idProyecto) REFERENCES Proyecto (idProyecto)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,
    idUsuario INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_transaccion_usuario`
		FOREIGN KEY (idUsuario) REFERENCES Usuario (idUsuario)
		ON DELETE CASCADE
		ON UPDATE RESTRICT    
) ENGINE = InnoDB;

CREATE TABLE Busqueda (
	idBusqueda INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	busqueda VARCHAR(120) NOT NULL,
    fechahora DATETIME NULL,
    idProyecto INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_busqueda_proyecto`
		FOREIGN KEY (idProyecto) REFERENCES Proyecto (idProyecto)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,
    idUsuario INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_busqueda_usuario`
		FOREIGN KEY (idUsuario) REFERENCES Usuario (idUsuario)
		ON DELETE CASCADE
		ON UPDATE RESTRICT    
) ENGINE = InnoDB;

CREATE TABLE Articulo (
	idArticulo INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	articulo VARCHAR(120) NOT NULL,
    url VARCHAR(120) NOT NULL,
    test TINYINT(1) NOT NULL,
    clasificacion VARCHAR(50) NOT NULL,
    keywords VARCHAR(120) NOT NULL,
    idProyecto INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_articulo_proyecto`
		FOREIGN KEY (idProyecto) REFERENCES Proyecto (idProyecto)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,
    idUsuario INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_articulo_usuario`
		FOREIGN KEY (idUsuario) REFERENCES Usuario (idUsuario)
		ON DELETE CASCADE
		ON UPDATE RESTRICT    
) ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS Colaborador (
  idProyecto INT UNSIGNED NOT NULL,
  idUsuario INT UNSIGNED NOT NULL,
  PRIMARY KEY (idProyecto, idUsuario),
  FOREIGN KEY (idProyecto) REFERENCES Proyecto (idProyecto) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (idUsuario)  REFERENCES usuario (idUsuario) ON DELETE RESTRICT ON UPDATE CASCADE)
ENGINE = InnoDB;
