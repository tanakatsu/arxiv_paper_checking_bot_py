## arXiv paper checking bot

A bot watching arXiv papers that matches your keywords.
When this bot find papers that matches your keywords, it can notifies you via slack.

### Get started

1. Git clone this repository
1. Copy `settings.example.yml` to `settings.yml` and edit it

    Change keywords to what you like. You can list multiple keywords as follows.

        - NILM
        - Deep Learning

    Set you slack token and destination channel

Now, preparation is all done.
Set job scheduler (e.g. `cron`) to run `python bot.py` periodically and wait for new papers.
