
# Librerias 

from fastapi import FastAPI
import pandas as pd
import ast
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI, Query
from typing import Union, List
from textblob import TextBlob
from langdetect import detect
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.params import Path
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

app = FastAPI()
'''
# Función def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
dfGames_copia = pd.read_csv('dfdeveloper.csv')
def developer(desarrollador: str = Path(..., title="Nombre del desarrollador")):
    # Convertir el nombre del desarrollador a minúsculas
    desarrollador = desarrollador.lower()

    # Filtrar el DataFrame para obtener solo las filas de la empresa desarrolladora
    df_desarrollador = dfGames_copia[dfGames_copia['developer'].str.lower() == desarrollador]

    # Agrupar por anio y contar la cantidad de juegos en cada grupo
    resumen_por_anio = df_desarrollador.groupby('anios').agg({'item_id': 'count'}).reset_index()
    resumen_por_anio = resumen_por_anio.rename(columns={'item_id': 'Cantidad de Items'})

    # Contar el número de juegos gratuitos por anio
    juegos_gratis_por_anio = df_desarrollador[df_desarrollador['price'] == 0.0].groupby('anios').agg({'item_id': 'count'}).reset_index()
    
    # Combinar las dos tablas por el anio
    resumen_por_anio = resumen_por_anio.merge(juegos_gratis_por_anio, on='anios', how='left')
    
    # Comprobar si la columna "Juegos Gratuitos" existe
    if 'item_id' in resumen_por_anio:
        # Calcular el porcentaje de contenido gratuito y formatearlo
        resumen_por_anio['Contenido Free'] = (resumen_por_anio['item_id'] / resumen_por_anio['Cantidad de Items'] * 100).fillna(0)
        resumen_por_anio['Contenido Free'] = resumen_por_anio['Contenido Free'].apply(lambda x: f"{x:.2f}%")
        # Eliminar la columna "Juegos Gratuitos" si existe
        resumen_por_anio = resumen_por_anio.drop(columns=['item_id'])
    else:
        # Si no existe la columna, establecer Contenido Free en 0.00% para todos los anios
        resumen_por_anio['Contenido Free'] = "0.00%"
    return resumen_por_anio.to_dict(orient="records")

# Ruta para la función developer
@app.get("/recomendar/desarrollador/{desarrollador}")
def recommend_developer(desarrollador: str):
    result = developer(desarrollador)
    return {"recommendations": result}




# def userdata( User_id : str ): Debe devolver cantidad de dinero gastado por el usuario, 
# el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
dfFilReviews = pd.read_csv('dfuserdataR.csv')
dfFilGames = pd.read_csv('dfuserdataG.csv')
def userdata(User_id: str = Path(..., title="ID de usuario")):
    # Filtrar las reseñas del usuario en dfFilReviews
    User_id = User_id.lower()
    user_reviews = dfFilReviews[dfFilReviews['user_id'].str.lower() == User_id]

    user_url = dfFilReviews[dfFilReviews['user_id'] == User_id]['user_url'].iloc[0] if User_id in dfFilReviews['user_id'].values else None

    # Calcular la cantidad de dinero gastado por el usuario en dfFilGames
    money_spent = user_reviews.merge(dfFilGames, on='item_id', how='inner')['price'].sum()

    # Calcular el porcentaje de recomendación
    total_reviews = user_reviews.shape[0]
    positive_reviews = user_reviews['recommend'].sum()
    percentage_recommendation = (positive_reviews / total_reviews) * 100 if total_reviews > 0 else 0

    # Calcular la cantidad de ítems
    items_count = user_reviews['item_id'].nunique()

    user_data = {
        "Usuario X": User_id,
        "Dinero gastado": f"${money_spent:.2f} USD",
        "URL del Usuario": user_url,  # Agregamos la URL del Usuario
        "% de recomendación": f"{percentage_recommendation:.2f}%",
        "Cantidad de items": items_count
    }
    return user_data

# Ruta para la función userdata
@app.get("/userdata/{User_id}")
def get_user_data(User_id: str):
    result = userdata(User_id)
    return {"user_data": result}




# def best_developer_year( año : int ): Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. 
# (reviews.recommend = True y comentarios positivos)
dfFilGamesbest = pd.read_csv('dfbestGames.csv')
dfFilReviewsbest = pd.read_csv('dbestReviews.csv')
def best_developer_year(anio):
    anio = int(anio)  # Convierte a número entero
    
    # Filtrar las revisiones para el anio dado
    reviews_anio = dfFilReviewsbest[dfFilReviewsbest['postedAnios'] == anio]
    
    # Contar cuántos usuarios han recomendado cada juego por desarrollador
    developer_recommended_count = reviews_anio[(reviews_anio['recommend'] == 1)].groupby('item_id')['recommend'].count()
    
    # Unir los datos con la información de los desarrolladores
    developer_recommended_count = developer_recommended_count.reset_index()
    developer_recommended_count = developer_recommended_count.rename(columns={'item_id': 'item_id', 'recommend': 'Recomendaciones'})
    developer_data = dfFilGamesbest[['item_id', 'developer']]
    developer_data = developer_data.merge(developer_recommended_count, on='item_id', how='inner')
    
    # Calcular el total de recomendaciones por desarrollador
    developer_total_recommended = developer_data.groupby('developer')['Recomendaciones'].sum()
    
    # Obtener el top 3 de desarrolladores con más recomendaciones
    top_developers = developer_total_recommended.nlargest(3).reset_index()
    
    # Formatear la salida como una lista de diccionarios
    result = [{"Puesto {}: {}".format(i + 1, row['developer']): row['Recomendaciones']} for i, row in top_developers.iterrows()]
    
    return result
# Ruta para la función best_developer_year
@app.get("/best_developer/{anio}")
def get_best_developer_year(anio: int):
    result = best_developer_year(anio)
    return {"best_developers": result}




# def developer_reviews_analysis( desarrolladora : str ): Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador 
# como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de 
# sentimiento como valor positivo o negativo.
df_games = pd.read_csv('dfAnalisiGames.csv')
df_reviews = pd.read_csv('dfAnalisisReviews.csv')
def developer_sentiment(developer: str):
   
    developer = developer.lower()
    # Filtrar reseñas del desarrollador especificado
    item_ids_developer = df_games[df_games['developer'].str.lower() == developer]['item_id']
    df_reviews_developer = df_reviews[df_reviews['item_id'].isin(item_ids_developer)]

    # Realizar el análisis de sentimiento en las reseñas
    vader_analyzer = SentimentIntensityAnalyzer()
    df_reviews_developer['vader_sentiment'] = df_reviews_developer['review'].apply(lambda x: vader_analyzer.polarity_scores(x))
    df_reviews_developer['textblob_sentiment'] = df_reviews_developer['review'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)

    # Clasificar comentarios neutros según la columna 'recommend'
    df_reviews_developer['sentiment'] = 'neutral'
    df_reviews_developer.loc[df_reviews_developer['recommend'] == 1, 'sentiment'] = 'positive'
    df_reviews_developer.loc[df_reviews_developer['recommend'] == 0, 'sentiment'] = 'negative'

    # Contar reseñas positivas y negativas
    positive_reviews = df_reviews_developer[df_reviews_developer['sentiment'] == 'positive'].shape[0]
    negative_reviews = df_reviews_developer[df_reviews_developer['sentiment'] == 'negative'].shape[0]

    results = {
        "developer": developer,
        "positive_sentiment": positive_reviews,
        "negative_sentiment": negative_reviews
    }

    return results

@app.get("/developer_sentiment/{developer}")
def get_developer_sentiment(developer: str):
    result = developer_sentiment(developer)
    return {"sentiment_data": result}


'''
#def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género
#  dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
dfFilGamesufg = pd.read_csv('dfuserforGenG.csv')
dfFilItemsufg = pd.read_csv('dfuserforGenIReduci.csv')
@app.get("/user_for_genre/{genero}")
async def get_user_for_genre(genero: str):
    # Realiza la búsqueda del género en el DataFrame
    merged_df = pd.merge(dfFilGamesufg, dfFilItemsufg, on='item_id', how='inner')
    
    condition = merged_df['genres'].str.contains(genero, case=False, na=False)
    juegos_por_genero = merged_df[condition]

    # A partir de aquí, obtendremos la lista de item_id para los juegos en ese género.
    item_ids = juegos_por_genero['item_id'].tolist()

    grouped = merged_df.groupby(['anios', 'user_id'])['playtimeTotal'].sum().reset_index()

    # Encuentra el 'user_id' que tiene la mayor suma de 'playtimeTotal' por año.
    max_playtime_users_by_year = grouped.groupby(['anios', 'user_id'])['playtimeTotal'].max().reset_index()

    max_hours_played = max_playtime_users_by_year.groupby('anios').apply(lambda x: x.loc[x['playtimeTotal'].idxmax()])

    result = {
        "Genero": genero,
        "Numero de Juegos": len(item_ids),
        "Usuario con más horas jugadas para Género": max_hours_played.to_dict(orient='records')
    }

    return result



# Si es un sistema de recomendación item-item: def recomendacion_juego( id de producto ): 
# Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
mergedMachine = pd.read_csv('mergedMachine.csv')  
# Calcula la similitud del coseno una vez para todos los datos
features = mergedMachine.iloc[:, 5:]  # Selecciona las columnas relevantes
cosine_sim = cosine_similarity(features, features)

# Función para recomendaciones
def recomendacion_juego(id_producto, num_recomendaciones=5):
    # Obtiene el índice del juego ingresado
    idx = mergedMachine.index[mergedMachine['item_id'] == id_producto].tolist()[0]
    
    # Obtiene las puntuaciones de similitud del juego ingresado con otros juegos
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordena los juegos en función de la similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Inicializa una lista de juegos recomendados
    recommended_games = []
    
    # Itera a través de los juegos recomendados y agrega juegos únicos hasta alcanzar 5 recomendaciones
    for score in sim_scores:
        if len(recommended_games) >= num_recomendaciones:
            break
        recommended_game = mergedMachine.iloc[score[0]]
        # Verifica si el juego ya está en la lista de recomendaciones y no es el juego de entrada
        if recommended_game['Titulo'] not in recommended_games and recommended_game['item_id'] != id_producto:
            recommended_games.append(recommended_game['Titulo'])
    
    return recommended_games

# Modelo Pydantic para solicitudes de la API
class RecomendacionRequest(BaseModel):
    item_id: int

# Ruta para obtener recomendaciones
@app.get("/recomendaciones/")
async def obtener_recomendaciones(item_id: int):
    recomendaciones = recomendacion_juego(item_id)
    return {"Juegos recomendados": recomendaciones}




#Si es un sistema de recomendación user-item: def recomendacion_usuario( id de usuario ): 
# Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.
def recomendacion_usuario_juego(dataframe, user_id, num_recomendaciones=5):
    # Tu código para calcular recomendaciones
    user_id = user_id.lower()
    features = dataframe.iloc[:, 5:]  # Asumiendo que las columnas de características comienzan en la columna 4
    cosine_sim = cosine_similarity(features, features)
    
    # Obtiene el índice del usuario ingresado
    idx = dataframe.index[dataframe['user_id'].str.lower() == user_id].tolist()
    
    if not idx:
        return "Usuario no encontrado"
    
    idx = idx[0]
    
    # Obtiene las puntuaciones de similitud del usuario ingresado con otros usuarios
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordena los usuarios en función de la similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtiene los índices de los juegos recomendados
    top_indices = [x[0] for x in sim_scores]
    
    # Obtiene los nombres de los juegos recomendados junto con sus item_id
    recommended_games = dataframe.iloc[top_indices][['item_id', 'Titulo']].drop_duplicates(subset=['Titulo']).head(num_recomendaciones)
    recommended_games_list = recommended_games.to_dict(orient='records')
    
    return recommended_games_list

# Ruta para obtener recomendaciones de juegos basadas en user_id
@app.get("/recomendacion_usuario_juego/")
async def obtener_recomendaciones_usuario_juego(user_id: str):
    recomendaciones = recomendacion_usuario_juego(mergedMachine, user_id)
    return {"user_id": user_id, "recommended_games": recomendaciones}

