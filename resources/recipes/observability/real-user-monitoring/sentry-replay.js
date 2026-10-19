import * as Sentry from '@sentry/browser';

Sentry.init({
  dsn: 'https://abc@sentry.io/1', // replace with your project DSN
  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.01,
  replaysOnErrorSampleRate: 1.0,
});
