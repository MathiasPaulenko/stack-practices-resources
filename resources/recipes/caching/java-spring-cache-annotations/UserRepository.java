import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/** Repository stub — swap for your real repository in production. */
@Repository
public interface UserRepository extends JpaRepository<User, String> {

  User findByEmail(String email);

  User findByIdAndTenant(String id, String tenantId);
}
