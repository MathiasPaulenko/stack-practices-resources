"""Parse data.xml with ElementTree, XPath, defusedxml, and iterparse."""
import xml.etree.ElementTree as ET


def parse_dom(path: str = "data.xml") -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    for item in root:
        name = item.findtext("name")
        print(item.get("id"), item.get("category"), name)


def parse_xpath(path: str = "data.xml") -> None:
    tree = ET.parse(path)
    for item in tree.getroot().findall(".//item[@category='book']"):
        print("book:", item.get("id"), item.findtext("name"))


def parse_untrusted(path: str = "data.xml") -> None:
    # pip install defusedxml
    import defusedxml.ElementTree as DET

    root = DET.parse(path).getroot()
    print("untrusted root:", root.tag, len(root), "children")


def parse_streaming(path: str = "data.xml") -> None:
    for event, elem in ET.iterparse(path, events=("end",)):
        if elem.tag == "item":
            print("stream:", elem.get("id"), elem.findtext("name"))
            elem.clear()


if __name__ == "__main__":
    parse_dom()
    parse_xpath()
    parse_streaming()
    # parse_untrusted()  # requires: pip install defusedxml
