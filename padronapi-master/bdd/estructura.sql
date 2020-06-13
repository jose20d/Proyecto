DROP TABLE IF EXISTS ciudadano;
DROP TABLE IF EXISTS distrito;
DROP TABLE IF EXISTS canton;
DROP TABLE IF EXISTS provincia;
DROP TYPE IF EXISTS t_sexo;

CREATE TYPE t_sexo AS ENUM ('femenino','masculino');

CREATE TABLE provincia (
  codigo      character(1) PRIMARY KEY,
  nombre      varchar(10)
);

CREATE TABLE canton (
  provincia   character(1) REFERENCES provincia(codigo),
  codigo      character(2),
  nombre      varchar(22),
  PRIMARY KEY (provincia, codigo)
);

CREATE TABLE distrito (
  provincia   character(1),
  canton      character(2),
  codigo      character(3),
  nombre      varchar(34),
  PRIMARY KEY (provincia, canton, codigo),
  FOREIGN KEY (provincia, canton) REFERENCES canton (provincia, codigo)
);

CREATE TABLE ciudadano (
  cedula      character(9) PRIMARY KEY,
  vencimiento date,
  sexo        t_sexo,
  nombre      varchar(30),
  apellido1   varchar(26),
  apellido2   varchar(26),
  provincia   character(1),
  canton      character(2),
  distrito    character(3),
  junta       numeric(5),
  FOREIGN KEY (provincia, canton, distrito) REFERENCES distrito (provincia, canton, codigo)
);
