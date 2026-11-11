import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;
import org.xhtmlrenderer.pdf.ITextRenderer;

import java.io.FileOutputStream;
import java.io.OutputStream;

/**
 * HTML-to-PDF generation with Thymeleaf + Flying Saucer (OpenPDF).
 *
 * Dependencies (Maven):
 *   org.thymeleaf:thymeleaf
 *   org.xhtmlrenderer:flying-saucer-pdf-openpdf
 *
 * The template (invoice-template.html) must live on the classpath,
 * e.g. src/main/resources/invoice-template.html, and must be well-formed
 * XHTML: close all tags, quote all attributes.
 */
public class PdfGenerator {

    public static void generate(String outputPath, String customer, String total) throws Exception {
        ClassLoaderTemplateResolver resolver = new ClassLoaderTemplateResolver();
        resolver.setSuffix(".html");
        resolver.setTemplateMode("HTML");

        TemplateEngine engine = new TemplateEngine();
        engine.setTemplateResolver(resolver);

        Context ctx = new Context();
        ctx.setVariable("customer", customer);
        ctx.setVariable("total", total);
        String html = engine.process("invoice-template", ctx);

        try (OutputStream out = new FileOutputStream(outputPath)) {
            ITextRenderer renderer = new ITextRenderer();
            renderer.setDocumentFromString(html);
            renderer.layout();
            renderer.createPDF(out);
        }
    }

    public static void main(String[] args) throws Exception {
        generate("invoice_12345.pdf", "Acme Corp", "1,250.00");
        System.out.println("Wrote invoice_12345.pdf");
    }
}
