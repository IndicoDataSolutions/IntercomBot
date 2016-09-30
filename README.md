# IntercomBot
Bot for triaging incoming intercom requests and assigning them to the right people.

# Installation (linux-specific)

Install the python module:
```
sudo python setup.py develop
```

Sign up for an intercom API key at https://developers.intercom.io/page/getting-started
and set up a webhook that responds to the "New Message from a User", "Reply from a User", and "Conversation assigned to Teammate" events.

Set the required environment variables in your `~/.bashrc`:
```
export INTERCOM_INDICO_API_KEY='{INDICO_API_KEY}'
export INTERCOM_APP_ID='{INTERCOM_APP_ID}'
export INTERCOM_API_KEY='{INTERCOM_API_KEY}'
```


Make an intercom user for the bot and paste it's user ID into `intercombot/config.py` as the `SUGGESTOR_ID`.   

Build base message routing model based on historic data
```
python scripts/download_conversations.py
python scripts/train_custom_collections.py
```

Run the server:
```
python -m indicobot.server
```

Watch the bot start auto-assigning users to conversations!
