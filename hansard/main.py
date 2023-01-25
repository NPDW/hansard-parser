import argparse
import re
import subprocess
from csv import DictWriter

from lxml import etree


COUNT = 0


def get_files_mentioning(query):
    regex_query = r".*".join(query.lower().split(" "))
    output = subprocess.run(
        ["rg", "-l", "-i", regex_query, "hansard/scrapedxml"], capture_output=True
    )
    results = output.stdout.decode("utf-8").split("\n")
    return results


def parse_file(filename, query):
    # print(filename)
    global COUNT
    tree = etree.parse(filename)
    root = tree.getroot()
    mentions = []

    ########################################
    # Old attempt to parse the XML.
    # However it is broken up over multiple files (whenever they do a gidredirect for later edits)
    # This is a nightmare and leads to things constantly breaking.
    # A cleaner and more reliable method is to regex for the phrase we are looking for.
    ########################################
    # mentions = root.xpath(
    #     f'.//p[re:test(text(),"(?i){query}")]',
    #     namespaces={"re": "http://exslt.org/regular-expressions"},
    # )
    # for el in root:
    #     if el.tag == "speech":
    #         if query.lower() in etree.tostring(el).decode("utf-8").lower():
    #             for p in el:
    #                 if query.lower() in etree.tostring(p).decode("utf-8").lower():
    #                     # print("Made it here")
    #                     mentions.append(p)
    ########################################

    regex_query = r".*".join(query.lower().split(" "))

    # Checks all speech elements.
    # We cannot just search for the text in el.text due to nested elements within breaking this.
    # Instead we regex search the raw element body.
    for el in root:
        if el.tag == "speech":
            if re.search(regex_query, etree.tostring(el).decode("utf-8").lower()):
                for p in el:
                    if re.search(
                        regex_query, etree.tostring(p).decode("utf-8").lower()
                    ):
                        mentions.append(p)
    results = []
    for mention in mentions:
        parent = mention.getparent()
        if parent.tag != "speech":
            raise Exception()

        speaker_name = parent.get("speakername")
        # Get speech
        found_heading = False
        temp_parent = parent
        while not found_heading:
            temp_parent = temp_parent.getprevious()
            try:
                temp_parent.tag
            except:
                # Stupid gidredirect. Just have to accept incomplete list.
                found_heading = True
                debate = "Unknown"

            if (
                not found_heading
                and temp_parent.tag != "speech"
                and temp_parent.tag != "gidredirect"
            ):
                debate = temp_parent.text.strip()
                found_heading = True

        url = f"https://hansard.parliament.uk/search/Contributions?endDate={filename[26:-5]}&house=Commons&partial=False&searchTerm={query}&startDate={filename[26:-5]}"
        COUNT += 1
        results.append(
            {
                "speaker": speaker_name.replace("\n", " "),
                "debate": debate.replace("\n", " "),
                "date": filename[-15:-5],
                "url": url,
                "text": etree.tostring(mention)
                .decode("utf-8")
                .rstrip()
                .replace("\n", " "),
            }
        )
    return results


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--query", help="Required. Term to query", required=True, dest="query"
    )
    parser.add_argument(
        "--start-date", help="Start Date", required=False, dest="start_date"
    )
    parser.add_argument(
        "--output", help="Output file path", required=False, dest="output"
    )

    parser.add_argument("--end-date", help="End Date", required=False, dest="end_date")

    return parser.parse_args()


def main():
    args = parse_args()
    query = args.query
    # This argument is currently unused.
    start_date = args.start_date
    output = args.output
    files = get_files_mentioning(query)
    files.pop()
    results = []
    for file in files:
        results += parse_file(file, query)
    global COUNT
    print(COUNT)

    sorted_results = sorted(results, key=lambda result: result["date"])

    target = output if output else f"{query}.csv"
    with open(target, "w+") as f:
        writer = DictWriter(f, fieldnames=sorted_results[0].keys())
        writer.writeheader()
        writer.writerows(sorted_results)


if __name__ == "__main__":
    main()
