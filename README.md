# chatbot-for-webpage

`chatbot-for-webpage` is a simple REST API-based chatbot that allows you to interact with any webpage by asking natural language questions. It automatically scrapes the webpage, builds a vector database using FAISS and HuggingFace embeddings, and lets you query it like a chatbot.

## Features
- Extracts text data from any given URL.
- Generates embeddings using HuggingFace models.
- Stores vectors locally using FAISS.
- Retrieves relevant information using vector similarity search.
- Allows chatting with the web page content.
- Optionally clears the stored vector database.
