// app.js — Slack bot with OpenAI via Bolt Socket Mode.
// Companion code for https://stackpractices.com/recipes/slack-bot-openai/
import { App } from '@slack/bolt';
import OpenAI from 'openai';
import dotenv from 'dotenv';

dotenv.config();

const slack = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  appToken: process.env.SLACK_APP_TOKEN,
  socketMode: true,
});

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// In-memory conversation store (use Redis in production)
const conversations = new Map();

function getHistory(userId) {
  if (!conversations.has(userId)) {
    conversations.set(userId, [{ role: 'system', content: 'You are a helpful assistant in a Slack workspace.' }]);
  }
  return conversations.get(userId);
}

async function getGPTResponse(messages) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages,
    max_tokens: 500,
  });
  return response.choices[0].message.content;
}

// Respond to app mentions in channels
slack.event('app_mention', async ({ event, say }) => {
  const text = event.text.replace(/<@[^>]+>/, '').trim();
  if (!text) return; // bare mention with no question

  const history = getHistory(event.user);
  history.push({ role: 'user', content: text });
  const reply = await getGPTResponse(history);
  history.push({ role: 'assistant', content: reply });

  // Keep the system prompt plus the last 10 messages
  if (history.length > 11) {
    conversations.set(event.user, [history[0], ...history.slice(-10)]);
  }

  await say({ text: reply, thread_ts: event.ts });
});

// Respond to direct messages — skip bots, non-DM traffic, and empty text
slack.message(async ({ message, say }) => {
  if (message.bot_id || message.subtype || message.channel_type !== 'im' || !message.text?.trim()) {
    return;
  }

  const history = getHistory(message.user);
  history.push({ role: 'user', content: message.text });
  const reply = await getGPTResponse(history);
  history.push({ role: 'assistant', content: reply });

  await say(reply);
});

(async () => {
  await slack.start();
  console.log('Slack bot is running');
})();
