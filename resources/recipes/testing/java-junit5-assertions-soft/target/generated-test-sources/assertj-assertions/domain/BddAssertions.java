package domain;

/**
 * Entry point for BDD assertions of different data types.
 */
@javax.annotation.Generated(value="assertj-assertions-generator")
public class BddAssertions {

  /**
   * Creates a new instance of <code>{@link domain.UserAssert}</code>.
   *
   * @param actual the actual value.
   * @return the created assertion object.
   */
  @org.assertj.core.util.CheckReturnValue
  public static domain.UserAssert then(domain.User actual) {
    return new domain.UserAssert(actual);
  }

  /**
   * Creates a new <code>{@link BddAssertions}</code>.
   */
  protected BddAssertions() {
    // empty
  }
}
