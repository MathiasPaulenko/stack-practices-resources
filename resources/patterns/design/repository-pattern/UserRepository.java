// Repository Pattern — Java implementation.

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.ArrayList;

class User {
    int id;
    String name;
    String role;

    User(int id, String name, String role) {
        this.id = id;
        this.name = name;
        this.role = role;
    }
}

interface UserRepository {
    Optional<User> getById(int id);
    List<User> findAll();
    void save(User user);
    boolean delete(int id);
}

class InMemoryUserRepository implements UserRepository {
    private final Map<Integer, User> users = new HashMap<>();

    @Override
    public Optional<User> getById(int id) {
        return Optional.ofNullable(users.get(id));
    }

    @Override
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }

    @Override
    public void save(User user) {
        users.put(user.id, user);
    }

    @Override
    public boolean delete(int id) {
        return users.remove(id) != null;
    }
}

class UserService {
    private final UserRepository repo;

    UserService(UserRepository repo) {
        this.repo = repo;
    }

    User promoteUser(int id) {
        User user = repo.getById(id)
            .orElseThrow(() -> new IllegalArgumentException("User not found"));
        user.role = "admin";
        repo.save(user);
        return user;
    }
}
