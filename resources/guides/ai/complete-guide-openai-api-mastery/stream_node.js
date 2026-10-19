// Streaming with the OpenAI Node SDK — same async-iterator pattern.
import OpenAI from "openai";

const client = new OpenAI();

const stream = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Explain async programming." }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
}
