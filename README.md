# Market Spread API
Esta API expone endpoints para obtener los spreads de los mercados de Buda.

## Correr servidor de desarrollo
Es necesario contar con poetry y python mayor a 3.10, es más fácil

Para buildear la imagen:

`docker build -t market-spread-api .`

y correr el servidor:

`docker run -p 8000:8000 market-spread-api`

la aplicación estará corriendo en localhost:8000, para ver la documentación ir a

`localhost:8000/api/v1/docs`

### Endpoints
- Todos los mercados: `GET localhost:8000/api/v1/markets/`
- Todos los spreads: `GET localhost:8000/api/v1/markets/spreads/`
- Detalle de mercado: `GET localhost:8000/api/v1/markets/<market_id>/`
- Spread para mercado específico: `GET localhost:8000/api/v1/markets/<market_id>/spread/`
- Crear alerta: `POST localhost:8000/api/v1/spread-alerts/`
- Hacer seguimiento de alerta: `GET localhost:8000/api/v1/spread-alerts/<alert-id>/`

## Tests
Para ejecutar los tests es necesario correr el siguiente script, el script asume que la imagen tageó como market-spread-api:
`scripts/run_tests.sh`

## Documentación
La documentacion de la API se encuentra en `localhost:8000/api/v1/docs`


## Algunas consideraciones

El servicio aquí desarrollado es puramente demostrativo, no está preparado para producción y puede 
beneficiarse de varias mejoras:

- Autenticación y autorización para creación y consulta de alertas
- Uso de una db más apta que sqlite (de ser necesario), y utilizar compose u otro para que
la db exista en otro contenedor independiente de la app.
- Logueo de solicitudes/respuestas a API de Buda en caso de error
- El cliente de Buda tiene una pequeña dependencia de Django que podría eliminarse y volverse un componente
más modular si fuera útil
- Se necesitaría usar un servidor wsgi digno como gunicorn en producción
- Se agredecería testear las vistas