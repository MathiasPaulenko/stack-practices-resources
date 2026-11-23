import java.io.File;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

/** DOM and SAX parsing of data.xml with XXE-safe factory settings. */
public class ParseXml {
    public static void main(String[] args) throws Exception {
        parseDom();
        parseSax();
    }

    static void parseDom() throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
        factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        factory.setXIncludeAware(false);
        factory.setExpandEntityReferences(false);

        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new File("data.xml"));

        NodeList items = doc.getElementsByTagName("item");
        for (int i = 0; i < items.getLength(); i++) {
            Element item = (Element) items.item(i);
            System.out.println(item.getAttribute("id") + " "
                + item.getElementsByTagName("name").item(0).getTextContent());
        }
    }

    static void parseSax() throws Exception {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        SAXParser parser = factory.newSAXParser();
        parser.parse(new File("data.xml"), new DefaultHandler() {
            public void startElement(String uri, String localName, String qName, Attributes attrs) {
                if (qName.equals("item")) {
                    System.out.println("sax: " + attrs.getValue("id"));
                }
            }
        });
    }
}
