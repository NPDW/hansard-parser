Hansard scraper.

Data on all debates in parliament are fetched from theyworkforyou.com.
This provides all debates in XML format.
These are rather messy and a pain to parse, however gov.uk websites block all attempts to scrape.

To download debates:

```bash
rsync -az --progress --exclude '.svn' --exclude 'tmp/' --relative 'data.theyworkforyou.com::parldata/scrapedxml/debates/debates*-*-*' .
```

This will check the files you already have downloaded, so can safely be ran multiple times.
