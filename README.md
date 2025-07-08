# Bot DaiChat

Telegram bot for managing appointment slots. This project is configured to run on [Render](https://dashboard.render.com/).

## Deployment

1. Create a new **Worker** service from this repository on Render.
2. Set the environment variable `BOT_TOKEN` with your Telegram bot token.
3. Render will automatically install dependencies using `requirements.txt` and start the bot with `python main.py` as defined in `render.yaml`.

## Local development

Create a `.env` file with:

```
BOT_TOKEN=YOUR_TOKEN
```

Then install dependencies and run:

```bash
pip install -r requirements.txt
python main.py
```
