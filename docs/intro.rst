Inicio e Instalación
====================

Para empezar **cibb** es  una estructura básica para un proyecto Django
totalmente orientada a servicios, en este caso servicios web *REST*.

El objetivo de  **cibb** es no depender de ningun framework de lado frontend.
por lo que a la larga existiran muchas implementaciones frontend para **cibb**.
implementaciones en *BackboneJS*, *AngularJS* y *ReactJS* principalmente.



Para utilizar la plantilla deberá seguir los siguientes pasos.

.. rubric:: 1. Crear y activar un entorno virtual

``virtualenv env && source env/bin/activate``

.. rubric:: 2. Instalar Django

``pip install Django``

.. rubric:: 3. Crear el proyecto

``django-admin.py startproject --template=https://github.com/jvacx/cibb``

.. rubric:: 3. Instalación para desarrollo

``make develop``

.. rubric:: 4. (opcional) Instalación para Producción

``make prod``

.. note::

    Estamos suponiendo que para estos pasos se tiene instalados y configurados:
    **python**, **virtualenv**, **nodejs**, **make y build essentials**..
