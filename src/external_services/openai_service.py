from abc import ABC, abstractmethod
from openai import OpenAI
from infra import IEnvConfig
from errors import ConflictError, InternalServerError, BadRequestError
import json


class IOpenAiService(ABC):
    @abstractmethod
    def validate_question(description: str, existing_questions_json: str) -> str:
        pass


class OpenAiService(IOpenAiService):
    def __init__(self, env_config: IEnvConfig) -> None:
        api_key = env_config.get_env("OPENAI_API_KEY")
        client = OpenAI()
        client.api_key = api_key
        self._client = client

    def validate_question(self, description: str, existing_questions_json: str) -> str:
        if existing_questions_json is None:
            existing_questions_json = "{}"
        request_message = (
            f'I have this description "{description}";'
            'I want to translate that to english and fix grammar errors;'
            f'Also check if this description exists integraly, have similarities or have represent the same description that descriptions in this JSON "{existing_questions_json}";'
            'If exists integraly, have similarities or have represent the same description that descriptions in this JSON just return string "Description already exists" in field "error" in response JSON;'
            'If does not just return the description that was translated and fixed as string in field "description" and "" (empty string) in field error in response JSON;'
            'Also if the description is not a question with you response with "Yes" or "No" return string "Description is not a question" in field error in response JSON;'
            'If you want to return anything that I do not describe here return a string with word "Error" in field "error" in response JSON.'
        )
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": request_message}
            ],
            response_format={"type": "json_object"},
        )
        response_message = response.choices[0].message.content.strip()
        response_json = json.loads(response_message)
        print("request", request_message)
        print("response", response_json)
        if response_json["error"].lower().find("description already exists") != -1:
            raise ConflictError(f'description "{description}" already exists in database')
        if response_json["error"].lower().find("description is not a question") != -1:
            raise BadRequestError(f'description "{description}" sent that was not a question')
        if response_json["error"].find("error") != -1:
            err = ValueError(f"error to process description {description}")
            raise InternalServerError(err)
        return response_json["description"]