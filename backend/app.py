from fastapi import FastAPI
app = FastAPI()

from pydantic import BaseModel

from utils import init_agent

agent = init_agent()


class User_input(BaseModel):
    prompt: str

@app.post('/ask')
def operate(input: User_input):
    result = agent.run(query=input.prompt)
    return result["answers"][0].answer


