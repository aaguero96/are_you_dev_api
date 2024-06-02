from abc import ABC, abstractmethod
from openai import OpenAI
from infra import IEnvConfig
from errors import ConflictError, InternalServerError
import re


class IOpenAiService(ABC):
    @abstractmethod
    def validate_question(question: str, existing_questions_json: str) -> str:
        pass


class OpenAiService(IOpenAiService):
    def __init__(self, env_config: IEnvConfig) -> None:
        api_key = env_config.get_env("OPENAI_API_KEY")
        client = OpenAI()
        client.api_key = api_key
        self._client = client

    def validate_question(self, question: str, existing_questions_json: str) -> str:
        request_message = f'I have this question "{question}", I want to translate that to english, fix grammar errors, and check if this questions exists integraly or with similarities in this JSON "{existing_questions_json}", if exists in JSON (integraly or with similarities) just return string "Question already exists" and if doesnt exists in JSON just return the question that was translated and fixed. Important, only return the string not an analyse. Also if question doesnt make sense or if you doesnt has capcaity to do that return just "error"'
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": request_message}
            ]
        )
        response_message = response.choices[0].message.content
        if response_message.lower().find("question already exists") != -1:
            raise ConflictError(f'question "{question}" already exists in database')
        if response_message.lower().find("error") != -1:
            err = ValueError(f"error to process question {question}")
            raise InternalServerError(err)
        match = re.match(r'^"(.*)"$', response_message)
        if match:
            return match.group(1)
        else:
            return response_message