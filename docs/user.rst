Usuarios
========

Los servicios comunes para los usuarios comprenden una serie de operaciones, tales como:

Listar usuarios
----------------

``http://0.0.0.0:5000/api/users``

- **GET**. Listará todos los usuarios siempre y cuando se tengan permisos suficientes.

Actualización parcial
---------------------

``http://0.0.0.0:5000/api/users/{pk}``

- **PATCH**. Actualizará la información enviada, necesita permisos de authenticación.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `username`        +      Cadena     |
  +-------------------+-----------------+
  | `first_name`      +      Cadena     |
  +-------------------+-----------------+
  | `last_name`       +      Cadena     |
  +-------------------+-----------------+
  | `email`           +  Cadena/Email   |
  +-------------------+-----------------+
  | `about`           +      Text       |
  +-------------------+-----------------+
  | `gender`          + Choice/Char     |
  +-------------------+-----------------+
  | `birth_date`      + Date            |
  +-------------------+-----------------+
  | `address`         + Text            |
  +-------------------+-----------------+
  | `country`         + Choice/Chars    |
  +-------------------+-----------------+
  | `city`            + Choice/Chars    |
  +-------------------+-----------------+


Obtener CSRF token
------------------

``http://0.0.0.0:5000/api/users/get_csrf_token``

- **GET**. Devolverá un token CSRF para el usuario con **permisos de authenticación.**


Obtener Perfíl
--------------

``http://0.0.0.0:5000/api/users/profile``

- **GET**. Devolverá el perfil del usuario con **permisos de authenticación.**

Cambiar Contraseña
------------------

``http://0.0.0.0:5000/api/users/password_change``

- **POST**. Se deben enviar 3 parametros obviamente no sin antes tener **permisos de authenticación.**

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `current_password`+      Cadena     |
  +-------------------+-----------------+
  | `password1`       +      Cadena     |
  +-------------------+-----------------+
  | `password2`       +      Cadena     |
  +-------------------+-----------------+

Recuperar Contraseña
--------------------

``http://0.0.0.0:5000/api/users/password_recovery``

- **POST**. Se debe enviar 1 parametro y se enviará un correo al propietario de la cuenta.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `username`        +      Cadena     |
  +-------------------+-----------------+

.. note::
  **username** puede ser *nombre de usuario* o *correo electrónico*.

Confirmar Recuperación de Contraseña
------------------------------------

``http://0.0.0.0:5000/api/users/password_from_recovery``

- **POST**. Se debe enviar 2 parametros para resetear la contraseña.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `token`           +      Cadena     |
  +-------------------+-----------------+
  | `password`        +      Cadena     |
  +-------------------+-----------------+

Cambiar email
-------------

``http://0.0.0.0:5000/api/users/change_email``

- **POST**. Se debe enviar 1 parametros para cambiar email. Este paso se realiza cuando ocurrio una actualización parcial afectando al correo eletronico.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `email_token`     +      Cadena     |
  +-------------------+-----------------+

.. note::
  El token de correo solo se obtiene por la url que fue enviada al correo del usuario.

Cancelar Cuenta
-----------------

``http://0.0.0.0:5000/api/users/cancel``

- **POST**. Se debe enviar 1 parametros para cambiar email. Este paso se realiza cuando ocurrio una actualización parcial afectando al correo eletronico.

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `cancel_token`    +      Cadena     |
  +-------------------+-----------------+

.. note::
  El token de cancelación se envia al correo del usuario cuando este ha activado su cuenta.