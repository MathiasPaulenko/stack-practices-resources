import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.StringWriter;
import java.util.List;

// Spring Boot sitemap endpoint — builds the urlset with the JDK DOM API.
// Swap the hardcoded UrlEntry list for a repository query.
@RestController
public class SitemapController {

  record UrlEntry(String loc, String lastmod, String changefreq, String priority) {}

  @GetMapping(value = "/sitemap.xml", produces = MediaType.APPLICATION_XML_VALUE)
  public String sitemap() {
    List<UrlEntry> urls = List.of(
      new UrlEntry("https://example.com/", "2024-06-01", "daily", "1.0"),
      new UrlEntry("https://example.com/blog/post-1", "2024-06-10", "weekly", "0.8"),
      new UrlEntry("https://example.com/products/item-1", "2024-06-05", "weekly", "0.6")
    );
    return buildSitemap(urls);
  }

  private String buildSitemap(List<UrlEntry> urls) {
    try {
      DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
      Document doc = builder.newDocument();

      Element urlset = doc.createElement("urlset");
      urlset.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9");
      doc.appendChild(urlset);

      for (UrlEntry entry : urls) {
        Element url = doc.createElement("url");
        urlset.appendChild(url);

        Element loc = doc.createElement("loc");
        loc.setTextContent(entry.loc());
        url.appendChild(loc);

        Element lastmod = doc.createElement("lastmod");
        lastmod.setTextContent(entry.lastmod());
        url.appendChild(lastmod);

        Element changefreq = doc.createElement("changefreq");
        changefreq.setTextContent(entry.changefreq());
        url.appendChild(changefreq);

        Element priority = doc.createElement("priority");
        priority.setTextContent(entry.priority());
        url.appendChild(priority);
      }

      Transformer transformer = TransformerFactory.newInstance().newTransformer();
      transformer.setOutputProperty(OutputKeys.INDENT, "yes");
      transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");

      StringWriter writer = new StringWriter();
      transformer.transform(new DOMSource(doc), new StreamResult(writer));
      return writer.toString();
    } catch (Exception e) {
      throw new RuntimeException("Failed to generate sitemap", e);
    }
  }
}
