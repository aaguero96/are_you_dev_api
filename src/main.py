from infra import DatabaseConfig
from repositories import UserRepository
from services import UserService
from controllers import UserController
from routes import UserRoute, SwaggerConfig
from fastapi import FastAPI
import uvicorn


def main():
    database_config = DatabaseConfig()
    database_config.create_tables()

    user_repository = UserRepository(database_config)

    user_service = UserService(user_repository)

    user_controller = UserController(user_service)

    user_route = UserRoute(user_controller)

    app = FastAPI()
    app.include_router(user_route.router)

    swagger_config = SwaggerConfig(app)
    swagger_config.apply()
    
    uvicorn.run(app, host="localhost", port=3000)


main()