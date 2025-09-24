# Assistant Chatbot

A chatbot built using fastapi with deep learning trained on set of intents which can help website visitors to provide insights about the webseeder services.

## Overview

This project provides a REST API using which frontend can talk with the chatbot using web sockets.

## Quick Start

### Prerequisites

- Python 3.8+
- Git

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Webseeder-Technologies/chatbot.git
cd chatbot/main-backend
```

2. **Set up a virtual environment**:
```bash
python3 -m venv .venv      # on Windows: python -m venv .venv 
source .venv/bin/activate  # On Windows: source .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Give Execute Permission**:
```bash
chmod +x run.sh
```
Now on you can use this command to run the fastapi server anytime whenever you make changes to the code.

5. **Start the API server**:
```bash
./run.sh
```
> ⚠️ If `./run.sh` command not working for you then use this command to run:
```bash
uvicorn main:app --host 0.0.0.0 --port 5700
```
The API will be available at `http://localhost:5700/docs`



