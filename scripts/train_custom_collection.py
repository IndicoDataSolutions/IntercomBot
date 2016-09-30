import json

from tqdm import tqdm

import indicoio
from indicoio.custom import Collection


def _reformat_example(example):
    messages, user_id = example
    messages = filter(lambda x: x is not None, messages)
    messages = "\n".join(messages)
    return [messages, user_id]

def train_custom_collection(data_file, collection_name):
    data = json.load(open(data_file))

    # Join a list of messages into a single example
    data = map(_reformat_example, data)

    batch_size = 20
    c = Collection(collection_name, domain='topics')

    try:
        c.clear()
    except indicoio.IndicoError:
        # act like nothing happened
        pass

    for start_idx in tqdm(range(0, len(data), batch_size)):
        messages = data[start_idx:start_idx+batch_size]
        messages = filter(lambda x: x[0].strip() != "", messages)
        c.add_data(messages)

    c.train()
    c.wait()

    print "%s: %s" % (collection_name, str(c.info()))
    return c

if __name__ == "__main__":
    collection = train_custom_collection('data/messages.json', 'triage-bot')
