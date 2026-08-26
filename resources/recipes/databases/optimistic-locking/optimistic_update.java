// JPA / Hibernate @Version example.
//
// Requires: jakarta.persistence, Spring Data JPA, H2 or PostgreSQL driver

package com.example.locking;

import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.Optional;

@Entity
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private BigDecimal price;

    @Version
    private Integer version;

    // Getters and setters omitted for brevity
}

interface ProductRepository extends JpaRepository<Product, Long> {
}

@Service
@Transactional
class ProductService {
    private final ProductRepository repo;

    ProductService(ProductRepository repo) {
        this.repo = repo;
    }

    public Product updatePrice(Long id, BigDecimal newPrice) {
        Product product = repo.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Product not found"));
        product.setPrice(newPrice);
        return repo.save(product);
    }
}
