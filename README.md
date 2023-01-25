# Hansard Parser

## What is this

This is a complete Web UI with Hansard Parser included.
This will parse all debates and return a CSV of every time a phrase is mentioned, along with the debate and corresponding MP.
This is a quick and easy solution. No automation or deployment scripts included.

## How to setup

- Fetch code onto an EC2 instance (other providers are available)
- Setup python and an environment with `python -m venv env`
- Fetch all python packages `python -m pip install -r requirements.txt`
- Fetch all debates with the command shown below.
- Setup a daily cronjob to fetch new debates (if you feel so inclined)
- Run the Web UI with:

```bash
uvicorn main:app --port 80 --host 0.0.0.0
```

## Fetching debates

Data on all debates in parliament are fetched from theyworkforyou.com.
This provides all debates in XML format.
These are rather messy and a pain to parse, however gov.uk websites block all attempts to scrape.

```bash
rsync -az --progress --exclude '.svn' --exclude 'tmp/' --relative 'data.theyworkforyou.com::parldata/scrapedxml/debates/debates202*-*-*' .
```

This will check the files you already have downloaded, so can be safely ran multiple times.
