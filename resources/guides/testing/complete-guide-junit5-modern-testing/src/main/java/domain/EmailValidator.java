package domain;

public class EmailValidator {

    public boolean isValid(String email) {
        return email != null && email.matches("^[^@\s]+@[^@\s]+\.[^@\s]+$");
    }

    public void validateEmail(String email) {
        if (!isValid(email)) {
            throw new ValidationException("Invalid email: " + email);
        }
    }
}
