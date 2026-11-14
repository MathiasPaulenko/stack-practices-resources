import java.util.List;
import org.springframework.cache.annotation.CacheConfig;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cache.annotation.Caching;
import org.springframework.stereotype.Service;

/**
 * Every Spring Cache annotation in one service. SpEL keys always reference
 * real parameter names — #user works only where a parameter is named `user`;
 * #result is legal in `unless` and in @CacheEvict's post-invocation condition,
 * never in a pre-invocation `condition`.
 */
@Service
@CacheConfig(cacheNames = {"users"})
public class UserService {

  private final UserRepository userRepository;

  public UserService(UserRepository userRepository) {
    this.userRepository = userRepository;
  }

  /** Cache hit skips the method entirely. */
  @Cacheable(key = "#id")
  public User getUserById(String id) {
    return userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id));
  }

  @Cacheable(key = "#email")
  public User getUserByEmail(String email) {
    return userRepository.findByEmail(email);
  }

  /** condition sees only arguments — evaluated before the call. */
  @Cacheable(key = "#id", condition = "#id != null")
  public User getUserByIdConditional(String id) {
    return userRepository.findById(id).orElseThrow();
  }

  /** unless sees #result — evaluated after the call, vetoes storing it. */
  @Cacheable(key = "#id", unless = "#result == null || !#result.isActive()")
  public User findUserById(String id) {
    return userRepository.findById(id).orElse(null);
  }

  /** Always runs; the saved entity replaces the cache entry. */
  @CachePut(key = "#user.id")
  public User updateUser(User user) {
    return userRepository.save(user);
  }

  /** #result.id caches the newly created user under its generated id. */
  @CachePut(key = "#result.id")
  public User createUser(UserDto dto) {
    User user = new User(null, dto.getEmail(), dto.getName(), true);
    return userRepository.save(user);
  }

  @CacheEvict(key = "#id")
  public void deleteUser(String id) {
    userRepository.deleteById(id);
  }

  @CacheEvict(allEntries = true)
  public void clearUserCache() {
    // No-op — the annotation clears the cache.
  }

  /** Evicts before the method runs — safe when the method may throw. */
  @CacheEvict(allEntries = true, beforeInvocation = true)
  public void bulkUpdateUsers(List<User> users) {
    userRepository.saveAll(users);
  }

  /** Pre-invocation condition: only arguments are visible. */
  @CacheEvict(key = "#user.id", condition = "#user.active == false")
  public void deactivateUser(User user) {
    user.setActive(false);
    userRepository.save(user);
  }

  /**
   * Post-invocation evict: @CacheEvict's condition CAN read #result because
   * eviction runs after the method by default. The "activeUsers" aggregate
   * only resets when the saved user actually ended up inactive.
   */
  @CachePut(key = "#user.id")
  @CacheEvict(value = "activeUsers", allEntries = true,
              condition = "#result.active == false")
  public User deactivateIfFraud(User user) {
    user.setActive(!isFraudulent(user));
    return userRepository.save(user);
  }

  private boolean isFraudulent(User user) {
    return false; // placeholder for a real fraud check
  }

  /** Stacked operations: keys must reference existing parameters. */
  @Caching(
      evict = {
          @CacheEvict(key = "#id"),
          @CacheEvict(key = "#dto.email"),
          @CacheEvict(value = "userList", allEntries = true),
      }
  )
  public User updateUserAndEvictCaches(String id, UserDto dto) {
    User user = userRepository.findById(id).orElseThrow();
    user.setEmail(dto.getEmail());
    user.setName(dto.getName());
    return userRepository.save(user);
  }

  /** Uses the customKeyGenerator bean from CacheConfig. */
  @Cacheable(keyGenerator = "customKeyGenerator")
  public User getUser(String id, String tenantId) {
    return userRepository.findByIdAndTenant(id, tenantId);
  }
}
