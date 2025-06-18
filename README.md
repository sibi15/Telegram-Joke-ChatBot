# Telegram Joke ChatBot
This project is a Telegram chatbot that generates a single joke based on any topic you mention. Built using Python, the LangChain framework, and Groq’s Gemma2-9B-It model, the bot demonstrates a playful use of LLMs in a real-time messaging context. It processes user messages, extracts a topic via regex, and replies with a joke through Telegram.

Tools and Libraries:
Telegram Bot API (python-telegram-bot), LangChain & LangChain Core, Groq API (LLM backend), dotenv for environment variable handling, and regex for topic parsing

Features:
- Mention-based topic detection in Telegram group chats
- Uses LangChain’s template and LLM chain to generate one-line jokes
- Calls Groq’s Gemma2-9B-It model via API key
- Traces LLM activity using LANGCHAIN_TRACING_V2
- Async support for real-time message handling
