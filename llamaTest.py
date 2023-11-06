from llama_cpp import Llama
llm = Llama(model_path="./models/mistral-7b-v0.1.Q4_K_M.gguf")
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
print(output)
