from infra import DatabaseConfig, EnvConfig, JwtConfig
from repositories import UserRepository
from services import UserService
from controllers import UserController
from routes import UserRoute, SwaggerConfig
from fastapi import FastAPI
import uvicorn


def main():
    # infra
    env_config = EnvConfig()
    database_config = DatabaseConfig()
    jwt_config = JwtConfig(env_config)

    # start database
    database_config.create_tables()

    # repositories
    user_repository = UserRepository(database_config)

    # services
    user_service = UserService(user_repository, jwt_config)

    # controllers
    user_controller = UserController(user_service)

    # routes
    user_route = UserRoute(user_controller)

    # api
    app = FastAPI()
    app.include_router(user_route.router)

    # swagger
    swagger_config = SwaggerConfig(app)
    swagger_config.apply()
    
    # start api
    uvicorn.run(app, host="localhost", port=3000)


main()