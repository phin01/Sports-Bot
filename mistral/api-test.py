#%%
import os

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
# %%
api_key = os.environ["MISTRAL_KEY"]
model = "open-mistral-7b"
client = MistralClient(api_key=api_key)

# %%
chat_response = client.chat(
    model=model,
    messages=[ChatMessage(role="user", content="How many goals has the Colorado Avalanche scored in the 2008 NHL season?")]
)
# %%
print(chat_response.choices[0].message.content)
# %%
print(chat_response.model_dump_json())
# %%
