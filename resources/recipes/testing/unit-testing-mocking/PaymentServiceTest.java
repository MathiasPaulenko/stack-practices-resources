// PaymentServiceTest.java — Mockito 5.x stub examples
import org.junit.jupiter.api.Test;
import static org.mockito.Mockito.*;

class PaymentServiceTest {
    @Test
    void sendsReceiptOnSuccess() {
        EmailService emailMock = mock(EmailService.class);
        when(emailMock.send(any())).thenReturn(new Receipt("123"));

        PaymentService service = new PaymentService(emailMock);
        service.processPayment(100, "u1");

        verify(emailMock, times(1)).send(argThat(email ->
            email.getSubject().equals("Payment received")
        ));
    }
}
