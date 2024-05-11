# %%
import os
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core.settings import Settings
# %%
api_key = os.environ["MISTRAL_KEY"]
llm = MistralAI(api_key=api_key,model="open-mistral-7b")
embed_model = MistralAIEmbedding(model_name='mistral-embed', api_key=api_key)

Settings.llm = llm
Settings.embed_model = embed_model
#%%
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
# nhl_data_docs = SimpleDirectoryReader(input_files=[r"C:\Portfolio\Sports-Bot\raw\nhl\data\standings\20072008.json"]).load_data()
nhl_data_docs = SimpleDirectoryReader(input_files=[r"C:\Users\phin_\OneDrive\Desktop\avs.json"]).load_data()
nhl_data_index = VectorStoreIndex.from_documents(nhl_data_docs)
nhl_data_engine = nhl_data_index.as_query_engine()

# %%
response = nhl_data_engine.query("how many points did the colorado avalanche win at home during the 2008 season?")
# %%
print(response)
# %%
