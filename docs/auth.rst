Authenticación
===============

Este conjunto de funciones se asocian con todas las operaciones basicas como registrar un nuevo usuario o iniciar sesión.


Registro
--------

``http://0.0.0.0:5000/api/auth/register``

- **POST**. Se deben enviar los datos principales del usuario.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `first_name`      +      Cadena     |
  +-------------------+-----------------+
  | `last_name`       +      Cadena     |
  +-------------------+-----------------+
  | `email`           +      Cadena     |
  +-------------------+-----------------+
  | `username`        +      Cadena     |
  +-------------------+-----------------+
  | `password`        +      Cadena     |
  +-------------------+-----------------+


Confirmar Registro
------------------

``http://0.0.0.0:5000/api/auth/confirm_register``

- **POST**. Se deben enviar el token que se recibe por correo al crear cuenta.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `token`           +      Cadena     |
  +-------------------+-----------------+


Iniciar Sesión
--------------

Disponibilidad de Email
-----------------------

``http://0.0.0.0:5000/api/auth/check_email``

- **POST**. Verifica si el correo electroníco no esta siendo usado por nadie más.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `email`           +      Cadena     |
  +-------------------+-----------------+

Disponibilidad de nombre de Usuario
-----------------------------------

``http://0.0.0.0:5000/api/auth/check_username``

- **POST**. Verifica si el nombre de usuario no esta siendo usado por nadie más.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `username`        +      Cadena     |
  +-------------------+-----------------+
