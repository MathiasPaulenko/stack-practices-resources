import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/** Minimal repository stub so UserService compiles standalone. */
public class UserRepository {

  private final Map<String, User> store = new ConcurrentHashMap<>();

  public User findById(String id) {
    return store.get(id);
  }

  public User save(User user) {
    store.put(user.id(), user);
    return user;
  }

  public void deleteById(String id) {
    store.remove(id);
  }
}
