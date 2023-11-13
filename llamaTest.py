import os
from dotenv import load_dotenv
from llama_cpp import Llama

load_dotenv()

llm = Llama(model_path =os.getenv('MODEL_PATH'))
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, echo=True)
print(output)
