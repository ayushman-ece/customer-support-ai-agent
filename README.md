# Closira AI Engineering Assignment

## Features

- FAQ Answering
- Lead Qualification
- Escalation Detection
- Conversation Summary

## Setup

Install packages:

```bash
pip install -r requirements.txt
```

Create .env file:

```env
OPENROUTER_API_KEY=YOUR_KEY
```

Run:

```bash
python app.py
```

Type:

```text
exit
```

to end the conversation.

## Files

app.py

Main workflow

sop_data.json

Business SOP

prompt_design.md

Prompt engineering explanation

test_transcripts

Example conversations

## Model

OpenRouter

meta-llama/llama-3.1-8b-instruct:free

## Limitations

- CLI only
- Basic escalation detection
- Single-session memory