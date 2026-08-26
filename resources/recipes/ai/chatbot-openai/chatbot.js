// Support chatbot using the OpenAI Assistants API.
//
// Run: node chatbot.js
//
// Requires: npm install openai
// Set: OPENAI_API_KEY environment variable

import OpenAI from 'openai';

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

function getOrderStatus(orderId) {
  // Mock function — replace with your real backend call.
  return `Order ${orderId} is shipped and arriving tomorrow.`;
}

async function createAssistant() {
  const assistant = await client.beta.assistants.create({
    name: 'Support Bot',
    instructions:
      'You are a support agent. Answer from the knowledge base. ' +
      'If you need order data, call get_order_status.',
    model: 'gpt-4o-mini',
    tools: [
      { type: 'file_search' },
      {
        type: 'function',
        function: {
          name: 'get_order_status',
          description: 'Get the status of a customer order',
          parameters: {
            type: 'object',
            properties: { order_id: { type: 'string' } },
            required: ['order_id'],
          },
        },
      },
    ],
    tool_resources: { file_search: { vector_store_ids: ['vs_...'] } },
  });
  return assistant.id;
}

async function runConversation(assistantId, userMessage) {
  const thread = await client.beta.threads.create();
  await client.beta.threads.messages.create(thread.id, {
    role: 'user',
    content: userMessage,
  });

  let run = await client.beta.threads.runs.create(thread.id, {
    assistant_id: assistantId,
  });

  while (['queued', 'in_progress', 'requires_action'].includes(run.status)) {
    await new Promise((r) => setTimeout(r, 1000));
    run = await client.beta.threads.runs.retrieve(run.id, {
      thread_id: thread.id,
    });

    if (run.status === 'requires_action') {
      const outputs = run.required_action.submit_tool_outputs.tool_calls.map(
        (tc) => {
          if (tc.function.name === 'get_order_status') {
            const args = JSON.parse(tc.function.arguments);
            return {
              tool_call_id: tc.id,
              output: getOrderStatus(args.order_id),
            };
          }
          return { tool_call_id: tc.id, output: '{}' };
        }
      );
      run = await client.beta.threads.runs.submitToolOutputs(run.id, {
        thread_id: thread.id,
        tool_outputs: outputs,
      });
    }
  }

  if (['failed', 'expired', 'cancelled'].includes(run.status)) {
    return `Run failed with status: ${run.status}`;
  }

  const messages = await client.beta.threads.messages.list(thread.id, {
    limit: 1,
    order: 'desc',
  });
  return messages.data[0].content[0].text.value;
}

async function main() {
  const assistantId = await createAssistant();
  const reply = await runConversation(
    assistantId,
    'What is the status of order ORD-9981?'
  );
  console.log(reply);
}

main().catch(console.error);
