// CustomerACL.java — Anti-corruption layer in Java
package com.shop.acl;

import com.shop.domain.Customer;
import com.shop.domain.CustomerStatus;
import com.legacy.client.LegacyCustomerClient;
import com.legacy.dto.LegacyCustomerDTO;
import org.springframework.stereotype.Component;

@Component
public class CustomerACL {

    private final LegacyCustomerClient legacyClient;

    public CustomerACL(LegacyCustomerClient legacyClient) {
        this.legacyClient = legacyClient;
    }

    public Customer findById(String customerId) {
        LegacyCustomerDTO legacy = legacyClient.getCustomer(customerId);
        if (legacy == null) return null;
        return translateFromLegacy(legacy);
    }

    public Customer save(Customer customer) {
        LegacyCustomerDTO legacy = translateToLegacy(customer);
        LegacyCustomerDTO saved = legacyClient.insert(legacy);
        return translateFromLegacy(saved);
    }

    public Customer suspend(String customerId) {
        LegacyCustomerDTO legacy = legacyClient.updateStatus(customerId, "2");
        return translateFromLegacy(legacy);
    }

    private Customer translateFromLegacy(LegacyCustomerDTO legacy) {
        String fullName = legacy.getFirstName() + " " + legacy.getLastName();
        CustomerStatus status = switch (legacy.getStatusCode()) {
            case "1" -> CustomerStatus.active();
            case "2" -> CustomerStatus.suspended();
            case "3" -> CustomerStatus.churned();
            default -> CustomerStatus.active();
        };

        return new Customer(
            legacy.getCustomerId(),
            legacy.getEmailAddress().toLowerCase(),
            fullName.trim(),
            status,
            legacy.getCreationDate()
        );
    }

    private LegacyCustomerDTO translateToLegacy(Customer customer) {
        String[] nameParts = customer.getFullName().split(" ", 2);
        String firstName = nameParts[0];
        String lastName = nameParts.length > 1 ? nameParts[1] : "";

        String statusCode = switch (customer.getStatus()) {
            case ACTIVE -> "1";
            case SUSPENDED -> "2";
            case CHURNED -> "3";
        };

        LegacyCustomerDTO dto = new LegacyCustomerDTO();
        dto.setCustomerId(customer.getId());
        dto.setEmailAddress(customer.getEmail());
        dto.setFirstName(firstName);
        dto.setLastName(lastName);
        dto.setStatusCode(statusCode);
        return dto;
    }
}
