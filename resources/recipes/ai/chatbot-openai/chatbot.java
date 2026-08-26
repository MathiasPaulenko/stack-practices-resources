// Support chatbot using the OpenAI Assistants API (Java).
//
// Requires: com.openai:openai-java
// Set: OPENAI_API_KEY environment variable

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.JsonValue;
import com.openai.models.FunctionDefinition;
import com.openai.models.FunctionParameters;
import com.openai.models.beta.assistants.AssistantCreateParams;
import com.openai.models.beta.assistants.FileSearchTool;
import com.openai.models.beta.assistants.FunctionTool;

import java.util.List;
import java.util.Map;

public class SupportAssistant {

    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        FunctionDefinition getOrderStatus = FunctionDefinition.builder()
            .name("get_order_status")
            .description("Get the status of a customer order")
            .parameters(FunctionParameters.builder()
                .putAllAdditionalProperties(Map.of(
                    "type", JsonValue.from("object"),
                    "properties", JsonValue.from(Map.of(
                        "order_id", Map.of("type", "string")
                    )),
                    "required", JsonValue.from(List.of("order_id"))
                ))
                .build())
            .build();

        AssistantCreateParams params = AssistantCreateParams.builder()
            .name("Support Bot")
            .instructions("You are a support agent. Answer from the knowledge base. " +
                          "If you need order data, call get_order_status.")
            .model("gpt-4o-mini")
            .addTool(FileSearchTool.builder().build())
            .addTool(FunctionTool.builder().function(getOrderStatus).build())
            .toolResources(AssistantCreateParams.ToolResources.builder()
                .fileSearch(AssistantCreateParams.ToolResources.FileSearch.builder()
                    .vectorStoreIds(List.of("vs_..."))
                    .build())
                .build())
            .build();

        var assistant = client.beta().assistants().create(params);
        System.out.println("Assistant created: " + assistant.id());

        // Thread, message, run, and tool-output submission follow the same pattern
        // using ThreadCreateParams, MessageCreateParams, RunCreateParams, etc.
        // See chatbot.py or chatbot.js for the full conversation loop.
    }
}
