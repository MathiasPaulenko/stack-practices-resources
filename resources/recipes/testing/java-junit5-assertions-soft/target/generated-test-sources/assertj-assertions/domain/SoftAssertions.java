package domain;

/**
 * Entry point for soft assertions of different data types.
 */
@javax.annotation.Generated(value="assertj-assertions-generator")
public class SoftAssertions extends org.assertj.core.api.SoftAssertions {

  /**
   * Creates a new "soft" instance of <code>{@link domain.UserAssert}</code>.
   *
   * @param actual the actual value.
   * @return the created "soft" assertion object.
   */
  @org.assertj.core.util.CheckReturnValue
  public domain.UserAssert assertThat(domain.User actual) {
    return proxy(domain.UserAssert.class, domain.User.class, actual);
  }

}
