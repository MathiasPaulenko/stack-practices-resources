import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

/**
 * Declarative caching with Spring annotations backed by Caffeine.
 * Pair with CacheConfig.java and spring-boot-starter-cache.
 */
@Service
public class UserService {

  private final UserRepository userRepository;

  public UserService(UserRepository userRepository) {
    this.userRepository = userRepository;
  }

  @Cacheable(value = "users", key = "#id")
  public User getUser(String id) {
    return userRepository.findById(id); // Only called on cache miss
  }

  @CachePut(value = "users", key = "#user.id")
  public User updateUser(User user) {
    return userRepository.save(user); // Writes through to the cache
  }

  @CacheEvict(value = "users", key = "#id")
  public void deleteUser(String id) {
    userRepository.deleteById(id); // Removes from the cache
  }

  @CacheEvict(value = "users", allEntries = true)
  public void clearUserCache() {
    // Clears the entire users cache
  }
}
