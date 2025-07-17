import streamlit as st
import tiktoken

from openai import AzureOpenAI

AZUREOPENAI_ENDPOINT = st.secrets["AZUREOPENAI_ENDPOINT"]
AZUREOPENAI_API_KEY = st.secrets["AZUREOPENAI_API_KEY"]

client = AzureOpenAI(
  azure_endpoint = AZUREOPENAI_ENDPOINT,
  api_key=AZUREOPENAI_API_KEY,
  api_version="2024-02-01"
)

def count_tokens(text: str, model: str = "gpt-4-1106-preview") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def llm_image(client, prompt, img_base64):  
    response = client.chat.completions.create(
      model="gpt-4.1", # model = "deployment_name".
      messages=[
          {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_base64}"
                    }
                }
            ]
          },
      ], max_tokens=500
    )
    
    return response.choices[0].message.content

def llm_text(client, question):  
    response = client.chat.completions.create(
      model="gpt-4.1", # model = "deployment_name".
      messages=[
          {"role": "user", "content": question},
      ]
    )
    
    return response.choices[0].message.content

