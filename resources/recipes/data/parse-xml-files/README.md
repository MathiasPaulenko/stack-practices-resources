# Parse XML Files — Companion Code

Runnable examples for the StackPractices recipe
[Parse XML Files in Python, Java, and JavaScript](https://stackpractices.com/recipes/parse-xml-files/).

## Contents

| File | What it shows |
| --- | --- |
| `data.xml` | Small sample catalog used by all examples |
| `parse_xml.py` | Python ElementTree (DOM), XPath, `iterparse` streaming, `defusedxml` for untrusted input |
| `parse-xml.mjs` | Node.js `fast-xml-parser` object mapping with `processEntities: false` |
| `ParseXml.java` | Java JAXP DOM + SAX with XXE-safe factory configuration |

## Run

```bash
python parse_xml.py          # Python 3.8+, stdlib only
node parse-xml.mjs           # npm install fast-xml-parser
javac ParseXml.java && java ParseXml
```

For `parse_untrusted()` in `parse_xml.py`, install `defusedxml` first
(`pip install defusedxml`) and uncomment the call in `__main__`.
