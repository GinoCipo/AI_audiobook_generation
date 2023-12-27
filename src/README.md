# Funcionalidad del modulo. 
Esta api permite la creacion de audiolibros con gen AI mediante la api de lovo llamada genny. La documentacion en particular de esta api se puede revisar en 

https://docs.genny.lovo.ai/reference/intro/getting-started.

**Para que eta API funcione es muy importante que reclames tu key del enlace de arriba y modifiques la variable personal_api_key en el archivo tts_api.py.**

La api esta implementada con fastapi y ponyORM, con una base de datos SQLite.

## Funcionalidad desde el frontend de Linguoo.
### Paso 1, subir el archivo.
En el frontend de Linguoo se reciben archivos en formato .txt. El propio Front se encarga de la division del texto en parrafos y presentarlos para edicion.

### Paso 2, revisar y editar texto.
Se renderizan un area de texto por parrafo con contenido. En caso de que haya habido un error en la division de texto o un cambio que se quiera realizar una edicion es posible revisar este problema aca.

Una vez conforme con el texto se aprieta el boton que lo envia a la api. Generando un nuevo "audiolibro" en la base de datos y posteriormente generando un audio para cada parrafo que se almacena en una carpeta output y una subcarpeta con el nombre del audiolibro.

### Paso 3, revisar los audios.
Por cada parrafo se tiene un reproductor de audio y un boton para modificarlo. El boton abre una nueva ventana donde se puede ver el texto perteneciente al parrafo. Una vez editado este texto se actualiza el texto en la base de datos, se genera el nuevo audio y se actualiza.

### Paso 4, producto final.
La api se encarga de concatenar todos los audios para generar el producto final, el cual se puede reproducir y revisar en el front, ademas de descargar con la opcion de 3 puntos a la derecha.