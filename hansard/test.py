"""
Quick demo of the functionality.
These are not unittests and never will be.
You can run this file to get a csv of all times "fintech" has been mentioned.

"""


from lxml import etree


tree = etree.parse("scrapedxml/debates/debates2016-02-01c.xml")
root = tree.getroot()

for el in root:
    # print(el.tag)
    if el.tag == "speech":
        # print(etree.tostring(el[0], pretty_print=True))
        if "fintech" in etree.tostring(el).decode("utf-8").lower():
            for p in el:
                if "fintech" in etree.tostring(p).decode("utf-8").lower():
                    print(etree.tostring(p).decode("utf-8"))
        # if "fintech" in el.text:
        #     print(el.text)
        # exit
