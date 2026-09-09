import jakarta.activation.DataHandler;
import jakarta.activation.DataSource;
import jakarta.activation.FileDataSource;
import jakarta.mail.*;
import jakarta.mail.internet.*;
import java.io.File;
import java.util.Map;
import java.util.Properties;

/**
 * SMTP sender with TLS, templates, attachments, and rate limiting.
 */
public class SmtpSender {

    private final String host;
    private final int port;
    private final String user;
    private final String password;
    private final long rateLimitMs;
    private long lastSend = 0;

    public SmtpSender(String host, int port, String user, String password, long rateLimitMs) {
        this.host = host;
        this.port = port;
        this.user = user;
        this.password = password;
        this.rateLimitMs = rateLimitMs;
    }

    public void send(String to, String subject, String text, String html, File[] attachments)
            throws Exception {
        throttle();
        Properties props = new Properties();
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.smtp.host", host);
        props.put("mail.smtp.port", port);

        Session session = Session.getInstance(props, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(user, password);
            }
        });

        Message msg = new MimeMessage(session);
        msg.setFrom(new InternetAddress(user));
        msg.setRecipients(Message.RecipientType.TO, InternetAddress.parse(to));
        msg.setSubject(subject);

        Multipart mixed = new MimeMultipart("mixed");
        Multipart alt = new MimeMultipart("alternative");

        MimeBodyPart textPart = new MimeBodyPart();
        textPart.setText(text);
        alt.addBodyPart(textPart);

        if (html != null) {
            MimeBodyPart htmlPart = new MimeBodyPart();
            htmlPart.setContent(html, "text/html; charset=utf-8");
            alt.addBodyPart(htmlPart);
        }

        MimeBodyPart wrapper = new MimeBodyPart();
        wrapper.setContent(alt);
        mixed.addBodyPart(wrapper);

        if (attachments != null) {
            for (File f : attachments) {
                MimeBodyPart att = new MimeBodyPart();
                DataSource source = new FileDataSource(f);
                att.setDataHandler(new DataHandler(source));
                att.setFileName(f.getName());
                mixed.addBodyPart(att);
            }
        }

        msg.setContent(mixed);
        Transport.send(msg);
    }

    public void sendTemplate(String to, String subject, String templateText,
                             String templateHtml, Map<String, String> context)
            throws Exception {
        String text = renderTemplate(templateText, context);
        String html = templateHtml != null ? renderTemplate(templateHtml, context) : null;
        send(to, subject, text, html, null);
    }

    private String renderTemplate(String template, Map<String, String> context) {
        String result = template;
        for (Map.Entry<String, String> entry : context.entrySet()) {
            result = result.replace("${" + entry.getKey() + "}", entry.getValue());
        }
        return result;
    }

    private void throttle() {
        long elapsed = System.currentTimeMillis() - lastSend;
        if (elapsed < rateLimitMs) {
            try {
                Thread.sleep(rateLimitMs - elapsed);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        lastSend = System.currentTimeMillis();
    }
}
