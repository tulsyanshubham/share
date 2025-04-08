import os
from groq import Groq
from itertools import cycle

apiKeys = [
    os.environ.get("GROQ_API_KEY_1"),
    os.environ.get("GROQ_API_KEY_2"),
    os.environ.get("GROQ_API_KEY_3"),
    os.environ.get("GROQ_API_KEY_4"),
    os.environ.get("GROQ_API_KEY_5"),
    os.environ.get("GROQ_API_KEY_6"),
    os.environ.get("GROQ_API_KEY_7"),
    os.environ.get("GROQ_API_KEY_8"),
]

output_dir = "output"
groqClients = [Groq(api_key=key) for key in apiKeys]

groq_cycle = cycle(groqClients)