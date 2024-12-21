# Bienvenidos al Proyecto de TPI115 😎

## Índice 📋
- [Instalaciones Requeridas](#Instalacion)
- [Comandos Importantes](#Comandos)

## Instalacion 📌
Aqui tendremos las librerias necesarias para que funcione nuestro proyecto.
- ✅ **pip install psycopg2** Libreria para PostgreSQL 🐘
- ✅ **pip install pillow** Libreria para manipulacion de Imagenes 📷

## Comandos 💻
- 🚀 Iniciar Servidor: `python manage.py runserver`

- 📌 Migraciones: `python manage.py makemigrations` && `python manage.py migrate` 
Las migraciones son importantes, ya que nos ayudan a llevar un control en nuestra base de datos
recuerden que Django trabaja con modelos y gestiona esos modelos por medio de las migraciones.
Si se a realizar una modificacion en los modelos usamos MAKEMIGRATIONS para que genere los archivos de migracion necesarios en donde describen los cambios que se haran en la base de datos. MIGRATE aplica las migraciones generadas a la base de datos, en pocas palabras modifica la estructura de la base de datos, osea todas las modificaciones que realizamos anteriormente las guarda en la base de datos todo esto gracias al MAKEMIGRATIONS

- ⚽ Aplicaciones: `python manage.py startapp nombre_de_la_app` 
Django nos permite crear aplicaciones, una aplicacion es un modulo o componente autonomo diseñado para manejar una funcionalidad especifica dentro de un proyecto. Por ejemplo, nosotros necesitamos crear modelos para la base de datos entonces al crear una aplicacion ya nos trae importantes archivos logicos como por ejemplo Views.py que son para las vistas, Models.py que son para la logica de los modelos, tambien Admin.py que nos permite registrar nuestros modelos en el apartado de Administracion que nos trae Django.