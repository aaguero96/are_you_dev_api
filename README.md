# are_you_dev_api

1. Start Development
- Recommendations:
    - git installed on computer with version => `git version 2.44.0`

- Clone this repository:
    - `git clone https://github.com/aaguero96/are_you_dev_api.git` fro HTTPS
    - `git clone git@github.com:aaguero96/are_you_dev_api.git` fro SSH

- Create envs:
	- `cp .env.example .env`
	- fill up .env file with correct values
    
2. Run local
- Recommendations:
    - python installed on computer with version => `Python 3.12.3`

- Create virtual environment:
    - `python -m venv .venv`

- Enter in virtual environment:
    - `source ./.venv/Scripts/activate` for WINDOWS

- Install dependencies:
    - `pip install -r requirements.txt`

- Start project:
    - `python ./src/main.py`

3. Swagger
- If you want to use swagger access `/docs` endpoint in API