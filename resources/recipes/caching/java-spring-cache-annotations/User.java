import java.io.Serializable;
import java.time.Instant;

/** Minimal domain stub so the service compiles. Must be serializable for Redis storage. */
public class User implements Serializable {

  private String id;
  private String email;
  private String name;
  private boolean active;
  private Instant updatedAt;

  public User() {}

  public User(String id, String email, String name, boolean active) {
    this.id = id;
    this.email = email;
    this.name = name;
    this.active = active;
    this.updatedAt = Instant.now();
  }

  public String getId() { return id; }
  public void setId(String id) { this.id = id; }
  public String getEmail() { return email; }
  public void setEmail(String email) { this.email = email; }
  public String getName() { return name; }
  public void setName(String name) { this.name = name; }
  public boolean isActive() { return active; }
  public void setActive(boolean active) { this.active = active; }
  public Instant getUpdatedAt() { return updatedAt; }
  public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }
}
