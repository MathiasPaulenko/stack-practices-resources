// tools.js — function calling example for the Slack bot.
// Companion code for https://stackpractices.com/recipes/slack-bot-openai/
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// 1. Declare the tools the model may call
const tools = [
  {
    type: 'function',
    function: {
      name: 'search_knowledge_base',
      description: 'Search the internal knowledge base for relevant documents',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'What the user is asking about' },
        },
        required: ['query'],
      },
    },
  },
];

// 2. Implement the tool — replace with your real search/vector store
async function searchKnowledgeBase({ query }) {
  return `Top result for "${query}": see the internal runbook (stubbed).`;
}

// 3. Run the two-step completion inside your event handler
export async function getAnswerWithTools(messages) {
  const first = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages,
    tools,
    tool_choice: 'auto',
  });

  const msg = first.choices[0].message;
  if (!msg.tool_calls?.length) return msg.content;

  const toolCall = msg.tool_calls[0];
  const args = JSON.parse(toolCall.function.arguments);
  const result = await searchKnowledgeBase(args);

  // Feed the tool result back for the final answer
  const second = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      ...messages,
      msg,
      { role: 'tool', tool_call_id: toolCall.id, content: result },
    ],
  });
  return second.choices[0].message.content;
}
