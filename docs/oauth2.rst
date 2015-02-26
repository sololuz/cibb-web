Authenticación Oauth2
=====================

Para utilizar este metodo de authenticación es recomendable que la API este desplegada sobre un protocolo seguro
como HTTPS.
Y el flujo de authenticación es el siguiente.


Crear el cliente
----------------

Sedeberá crear un  *Provider.Client* para obtener valores **client_id** y **client_secret** que seran utilizados luego.

Obtener un access token
-----------------------

``http://0.0.0.0:5000/oauth2/access_token``

- **POST**. Se debe enviar una peticion con la siguiente informacion

  +-------------------------------------+
  |             PETICIÓN                |
  +===================+=================+
  | `client_id`       +      Cadena     |
  +-------------------+-----------------+
  | `client_secret`   +      Cadena     |
  +-------------------+-----------------+
  | `username`        +      Cadena     |
  +-------------------+-----------------+
  | `password`        +      Cadena     |
  +-------------------+-----------------+

  La respuesta de la petición será algo como esto::

  {"access_token": "<your-access-token>",  "scope": "read", "expires_in": 86399, "refresh_token": "<your-refresh-token>"}



Acceder al API
--------------

para acceder a la API con authorización oauth2 solo se debera insertar lo siguiente en las cabeceras.

 access_token you've received in the Authorization request header.

  +--------------------------------------------------+
  |                     HEADERS                      |
  +===================+==============================+
  | `Authorization`   +  Bearer <your-access-token>  |
  +-------------------+------------------------------+

.. note::

  Para la authenticación oauth2 se esta utilizando el paquete **django-oauth2-provider**