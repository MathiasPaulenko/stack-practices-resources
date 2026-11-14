import com.github.tomakehurst.wiremock.junit5.WireMockRuntimeInfo;
import com.github.tomakehurst.wiremock.junit5.WireMockTest;
import org.junit.jupiter.api.Test;

import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static org.assertj.core.api.Assertions.assertThat;

@WireMockTest(httpPort = 8089)
class PaymentGatewayIntegrationTest {

    @Test
    void charge_returnsApproved_onValidCard(WireMockRuntimeInfo wm) {
        stubFor(post("/v1/charges")
            .withRequestBody(matchingJsonPath("$.amount"))
            .willReturn(okJson("{\"status\": \"approved\", \"id\": \"ch_123\"}")));

        PaymentClient client = new PaymentClient("http://localhost:8089");
        ChargeResult result = client.charge("cust-123", 4999);

        assertThat(result.status()).isEqualTo("approved");
        verify(postRequestedFor(urlEqualTo("/v1/charges"))
            .withHeader("Idempotency-Key", notNullValue()));
    }
}
