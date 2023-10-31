<h1 align="center"> PROYECTO INDIVIDUAL NÚMERO UNO MACHINE LEARNING OPERATIONS (MLOps) </h1>



<div align="center">
  <img src="https://github.com/JairAlarc/ProyectoCohorte16/assets/118782518/f86fc552-ce0d-49c2-a356-184c7e71bdd1" width="1200" alt="steam">
</div>

¡Después de un arduo trabajo y desafíos en Steam, la plataforma de videojuegos multinacional, me complace contarles que he logrado un hito importante! Mi tarea inicial era crear un sistema de recomendación de videojuegos para los usuarios de Steam, y debo decir que no fue nada fácil. 😅

Cuando comencé, me enfrenté a datos en un estado bastante crudos y desorganizados. La falta de estructura y la ausencia de procesos automatizados para mantener los datos actualizados parecían una montaña insuperable. Pero, como dicen por ahí, el camino a la grandeza a menudo comienza en cero. 💪

Me sumergí de lleno en el papel de Data Engineer y trabajé incansablemente para transformar esos datos desafiantes en información valiosa. Al final, logré desarrollar un Producto Mínimo Viable (MVP) que cumplió con los objetivos del proyecto.

Este proyecto en Steam me enseñó la importancia de la perseverancia y la pasión por lo que hago. Me enorgullece compartir mi historia de éxito en esta emocionante travesía. ¡El mundo de los videojuegos es realmente asombroso! 🎮✨

En nuestra propuesta de trabajo, tuvimos varios puntos claves:

1. **Transformaciones en los Datos**: En el MVP, decidimos centrarnos en la lectura del conjunto de datos con el formato correcto. Esto implica la eliminación de columnas innecesarias que no se utilizan para responder consultas o preparar modelos de aprendizaje automático. Al hacerlo, logramos optimizar el rendimiento de la API y el entrenamiento del modelo.

2. **Feature Engineering**: Uno de los aspectos importantes fue la creación de una nueva columna llamada 'sentiment_analysis' en el dataset 'user_reviews'. Aplicamos un análisis de sentimiento con Procesamiento del Lenguaje Natural (NLP), Textblob, Vader para clasificar las reseñas de juegos de los usuarios en tres categorías: '0' si es mala y '1' si es positiva. Esta columna reemplazó la columna 'user_reviews.review', lo que facilita el trabajo de análisis de datos. 

3. **Desarrollo de la API**: En esta fase, propusimos exponer los datos de la empresa mediante el uso del framework FastAPI. Creamos varios endpoints para la API, cada uno con su decorador correspondiente. Estas son las funciones que creamos para los endpoints:

    - `developer(desarrollador: str)`: Proporciona la cantidad de elementos y el porcentaje de contenido gratuito por año según la empresa desarrolladora.

    - `userdata(User_id: str)`: Devuelve información sobre un usuario específico, incluyendo el dinero gastado, el porcentaje de recomendación basado en las revisiones y la cantidad de elementos.

    - `UserForGenre(genero: str)`: Proporciona el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

    - `best_developer_year(año: int)`: Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado, considerando revisiones recomendadas y comentarios positivos.

    - `developer_reviews_analysis(desarrolladora: str)`: Basado en la desarrolladora proporcionada, retorna un diccionario que muestra la cantidad total de registros de reseñas de usuarios categorizados con análisis de sentimiento positivo o negativo.

Cada una de estas funciones permite realizar consultas específicas en la API para obtener información relevante de manera eficiente.

Después de preparar nuestros datos y exponerlos a través de la API, llegamos al emocionante paso de desarrollar un sistema de recomendación utilizando modelos de aprendizaje automático. Teníamos dos opciones proporcionadas por el equipo: crear un sistema de recomendación ítem-ítem o uno de usuario-ítem. Asumimos el desafío de explorar ambos para demostrar nuestras capacidades al equipo.

Para el Sistema de Recomendación Ítem-Ítem: Diseñamos un modelo basado en la similitud del coseno. Cuando los usuarios ingresan un juego, nuestro modelo busca en la base de datos de juegos y recomienda una lista de 5 juegos similares al que ingresaron. 

Para el Sistema de Recomendación Usuario-Ítem: Desarrollamos un modelo que se basa en encontrar usuarios similares. Cuando un usuario ingresa su ID, el modelo busca en la base de datos de usuarios similares y recomienda una lista de 5 juegos que a esos usuarios similares les gustaron. Este sistema de recomendación permite a los usuarios recibir sugerencias personalizadas basadas en sus preferencias y en las de usuarios similares.

Ambos sistemas de recomendación se integran en nuestra API, lo que permite a los usuarios acceder a estas recomendaciones a través de solicitudes GET. Esta implementación brinda a los departamentos de Analytics y Machine Learning la capacidad de utilizar los sistemas de recomendación para mejorar la experiencia de los usuarios y aumentar la participación en la plataforma. ¡Un paso emocionante hacia una plataforma de Steam más personalizada y atractiva para los usuarios! 😁🎮
