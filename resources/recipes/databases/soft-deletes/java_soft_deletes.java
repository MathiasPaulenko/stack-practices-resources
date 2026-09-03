// Soft deletes implementation with JPA / Hibernate.
// Requires: Hibernate 6+, Jakarta Persistence.
// Run: javac java_soft_deletes.java && java -cp . java_soft_deletes
// (adjust classpath for Hibernate dependencies)

import jakarta.persistence.*;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;

@Entity
@Table(name = "users")
@FilterDef(name = "softDeleteFilter", condition = "deleted_at IS NULL")
@Filter(name = "softDeleteFilter")
class User {
    @Id
    @GeneratedValue
    private Long id;

    private String email;
    private String name;

    @Column(name = "deleted_at")
    private Instant deletedAt;

    @Column(name = "deleted_by")
    private String deletedBy;

    public void softDelete(String deletedBy) {
        this.deletedAt = Instant.now();
        this.deletedBy = deletedBy;
    }

    public void restore() {
        this.deletedAt = null;
        this.deletedBy = null;
    }

    public Long getId() { return id; }
    public String getEmail() { return email; }
    public Instant getDeletedAt() { return deletedAt; }
    public void setEmail(String email) { this.email = email; }
    public void setName(String name) { this.name = name; }
}

public class java_soft_deletes {

    public static List<User> findActiveUsers(EntityManager em) {
        em.unwrap(org.hibernate.Session.class)
            .enableFilter("softDeleteFilter");
        return em.createQuery("SELECT u FROM User u", User.class).getResultList();
    }

    public static void restoreUser(EntityManager em, Long userId) {
        em.getTransaction().begin();
        User user = em.find(User.class, userId);
        if (user != null && user.getDeletedAt() != null) {
            user.restore();
            em.createQuery("UPDATE Post p SET p.deletedAt = NULL WHERE p.userId = :uid")
                .setParameter("uid", userId)
                .executeUpdate();
        }
        em.getTransaction().commit();
    }

    public static int purgeOldSoftDeletes(EntityManager em, int days) {
        Instant cutoff = Instant.now().minus(days, ChronoUnit.DAYS);
        em.getTransaction().begin();
        int users = em.createQuery("DELETE FROM User u WHERE u.deletedAt IS NOT NULL AND u.deletedAt < :cutoff")
            .setParameter("cutoff", cutoff)
            .executeUpdate();
        em.createQuery("DELETE FROM Post p WHERE p.deletedAt IS NOT NULL AND p.deletedAt < :cutoff")
            .setParameter("cutoff", cutoff)
            .executeUpdate();
        em.getTransaction().commit();
        return users;
    }

    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("soft-deletes-pu");
        EntityManager em = emf.createEntityManager();

        em.getTransaction().begin();
        User user = new User();
        user.setEmail("alice@example.com");
        user.setName("Alice");
        em.persist(user);
        em.getTransaction().commit();

        System.out.println("Created user: " + user.getEmail());

        em.getTransaction().begin();
        user.softDelete("admin");
        em.getTransaction().commit();

        System.out.println("Soft-deleted user: " + user.getEmail());

        List<User> visible = findActiveUsers(em);
        System.out.println("Visible users: " + visible.size());

        restoreUser(em, user.getId());
        System.out.println("Restored user");

        visible = findActiveUsers(em);
        System.out.println("Visible users after restore: " + visible.size());

        em.close();
        emf.close();
    }
}
