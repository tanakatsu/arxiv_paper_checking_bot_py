import os
import yaml
import json
import arxiv
from slacker import Slacker
from argparse import ArgumentParser


SETTINGS_FILE = "settings.yml"
HISTORY_FILE = "histories.json"


def load_settings(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return data


def load_histories(filename):
    if not os.path.exists(filename):
        return []

    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def save_histories(histories, filename):
    with open(filename, 'w') as f:
        json.dump(histories, f)


def get_new_entries(results, histories):
    db_entry_ids = [h for h in histories]
    new_results = [result for result in results if result.entry_id not in db_entry_ids]
    return new_results


def update_histories(histories, new_entries):
    for entry in new_entries:
        histories.append(entry.entry_id)
    return histories


def build_message(new_entry):
    entry_id = new_entry.entry_id
    title = new_entry.title
    summary = new_entry.summary

    msg = f"New paper: {title}\n\n{entry_id}\n\n{summary}"
    return msg


parser = ArgumentParser()
parser.add_argument('--dryrun', action='store_true')
args = parser.parse_args()

settings = load_settings(SETTINGS_FILE)
histories = load_histories(HISTORY_FILE)

results = []
for keyword in settings["keywords"]:
    search = arxiv.Search(
      query = keyword,
      max_results = settings["api"]["max_results"],
      sort_by = arxiv.SortCriterion.SubmittedDate
    )
    results.extend(search.results())

new_entries = get_new_entries(results, histories)
if len(new_entries):
    slack = Slacker(token=settings["slack"]["token"])
    for entry in new_entries:
        msg = build_message(entry)
        if args.dryrun:
            print(msg)
            print("\n")
        else:
            slack.chat.post_message(channel=settings["slack"]["channel"],
                                    username=settings["slack"]["bot_name"],
                                    text="```" + msg + "```",
                                    icon_emoji=settings["slack"]["options"]["icon_emoji"])
    print(f"Found {len(new_entries)} papers.")
    update_histories(histories, new_entries)
    save_histories(histories, HISTORY_FILE)
else:
    print("Found no new papers.")
