// Hibernate / JPA CRUD: entity + repository with explicit transactions.
//
// This file is a reference implementation. To run it you need a JPA provider
// (Hibernate) and a JDBC driver on the classpath, e.g. inside a Spring Boot
// or plain Jakarta EE project.
import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "users")
class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false, unique = true)
    private String email;

    private String role = "user";

    public Integer getId() { return id; }
    public String getEmail() { return email; }
    public String getRole() { return role; }
    public void setEmail(String email) { this.email = email; }
    public void setRole(String role) { this.role = role; }
}

@Entity
@Table(name = "posts")
class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private String title;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User author;
}

public class java_jpa_crud {

    static class UserRepository {
        private final EntityManager em;

        UserRepository(EntityManager em) { this.em = em; }

        public void create(User user) {
            em.getTransaction().begin();
            em.persist(user);
            em.getTransaction().commit();
        }

        public User findByEmail(String email) {
            return em.createQuery(
                    "SELECT u FROM User u WHERE u.email = :email", User.class)
                .setParameter("email", email)
                .getSingleResult();
        }

        public void updateRole(Integer id, String role) {
            em.getTransaction().begin();
            User user = em.find(User.class, id);
            user.setRole(role);
            em.getTransaction().commit();
        }

        public void delete(Integer id) {
            em.getTransaction().begin();
            em.remove(em.find(User.class, id));
            em.getTransaction().commit();
        }
    }

    public static void main(String[] args) {
        // Requires a persistence.xml + datasource; shown here as API reference.
        System.out.println("See README.md for how to wire the EntityManager.");
    }
}
