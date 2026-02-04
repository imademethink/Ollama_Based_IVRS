# Ollama Unleashed: Ollama based Next-Gen Secure IVRS powered by Ollama, RAG, Sentiment analysis, Guardrails

# YouTube video link : https://youtu.be/_aMUL1xTc9o

<img width="1536" height="1024" alt="Thumbnail" src="https://github.com/user-attachments/assets/892fb6a6-9665-4759-96c9-de777b3556a6" />

Ollama AI model assisted mechanism suitable for IVRS (banking domain)

It uses popular AI model gpt-oss:120b-cloud (user by OpenAI)

Gemini full discussion link : https://gemini.google.com/share/9653f6bde3fa


# Features
1) Customer validation

2) Understanding Customer Intent

3) Max 3 attempt then graceful exit

4) AI Bot response based on query

5) Know Intent + Tone

6) Apply Guard Rail

7) Unsupported task handling

8) Graceful exit

# Steps
As explained in above YouTube video, install Ollama (Windows/ Linux), get the API key

Store the key in ollama_api_key_file.txt

Download cloud AI model using : ollama run gpt-oss:120b-cloud

git clone https://github.com/imademethink/Ollama_Based_IVRS.git

cd Ollama_Based_IVRS-main

pip install -r requirements.txt

python ivrs1_dev.py

python ivrs2_qa.py

# Note : Strictly use Python 3.11 version 


