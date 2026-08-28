// email/EmailRenderer.ts
import mjml2html from 'mjml';
import Handlebars from 'handlebars';

interface WelcomeData {
  name: string;
  dashboardUrl: string;
}

export async function compileTemplate(
  mjmlSource: string,
  data: WelcomeData
): Promise<{ html: string; errors: unknown[] }> {
  const { html: rawHtml, errors } = mjml2html(mjmlSource, {
    validationLevel: 'strict',
    minify: true,
  });

  const template = Handlebars.compile(rawHtml);
  const html = template(data);

  return { html, errors };
}

export type { WelcomeData };
