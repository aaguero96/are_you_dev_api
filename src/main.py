from infra import DatabaseConfig, EnvConfig, JwtConfig
from repositories import UserRepository, QuestionRepository
from services import UserService, QuestionService
from controllers import UserController, QuestionController
from routes import UserRoute, SwaggerConfig, ErrorHandlerConfig, QuestionRoute
from fastapi import FastAPI
from external_services import OpenAiService
from middlewares import AuthMiddleware
import uvicorn


def main():
    # infra
    env_config = EnvConfig()
    database_config = DatabaseConfig(env_config)
    jwt_config = JwtConfig(env_config)

    # start database
    if env_config.get_env("ENV") == "development":
        database_config.create_tables()

    # repositories
    user_repository = UserRepository(database_config)
    question_repository = QuestionRepository(database_config)

    # external services
    openai_service = OpenAiService(env_config)

    # services
    user_service = UserService(user_repository, jwt_config)
    question_service = QuestionService(question_repository, openai_service)

    # middlewares
    auth_middleware = AuthMiddleware(jwt_config, user_repository)

    # controllers
    user_controller = UserController(user_service)
    question_controller = QuestionController(question_service)

    # routes
    user_route = UserRoute(user_controller)
    question_route = QuestionRoute(question_controller, auth_middleware)

    # api
    app = FastAPI()
    app.include_router(user_route.router)
    app.include_router(question_route.router)

    # swagger
    swagger_config = SwaggerConfig(app)
    swagger_config.apply()

    # error handlers
    ErrorHandlerConfig(app)
    
    # start api
    uvicorn.run(app, host=env_config.get_env("HOST"), port=int(env_config.get_env("PORT")))


main()