// CustomerEtlJob.java — Spring Batch 5 ETL job (reference implementation)
//
// Same three stages as the Python pipeline, expressed as reader / processor /
// writer beans. Spring Batch 5 removed *BuilderFactory, so JobRepository and
// PlatformTransactionManager go into the JobBuilder/StepBuilder constructors.
//
// Requires: spring-boot-starter-batch, a DataSource pointing at the source DB.
// The MERGE statement is PostgreSQL 15+; swap it for INSERT ... ON DUPLICATE
// KEY UPDATE on MySQL or the equivalent MERGE variant on SQL Server/Oracle.

import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.core.job.builder.JobBuilder;
import org.springframework.batch.core.repository.JobRepository;
import org.springframework.batch.core.step.builder.StepBuilder;
import org.springframework.batch.item.ItemProcessor;
import org.springframework.batch.item.database.BeanPropertyItemSqlParameterSourceProvider;
import org.springframework.batch.item.database.JdbcBatchItemWriter;
import org.springframework.batch.item.database.JdbcCursorItemReader;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.PlatformTransactionManager;

import javax.sql.DataSource;
import java.sql.PreparedStatement;
import java.time.Instant;

@Configuration
@EnableBatchProcessing
public class CustomerEtlJob {

    private final DataSource dataSource;
    private final JobRepository jobRepository;
    private final PlatformTransactionManager transactionManager;

    public CustomerEtlJob(DataSource dataSource,
                          JobRepository jobRepository,
                          PlatformTransactionManager transactionManager) {
        this.dataSource = dataSource;
        this.jobRepository = jobRepository;
        this.transactionManager = transactionManager;
    }

    // Stage 1: extract — cursor-based read, only rows changed since the watermark.
    @Bean
    public JdbcCursorItemReader<Customer> reader() {
        JdbcCursorItemReader<Customer> reader = new JdbcCursorItemReader<>();
        reader.setDataSource(dataSource);
        reader.setSql("SELECT id, email, first_name, last_name, status FROM source.customers WHERE updated_at >= ?");
        reader.setPreparedStatementSetter((PreparedStatement ps) ->
            ps.setTimestamp(1, java.sql.Timestamp.from(Instant.now().minusSeconds(86400))));
        reader.setRowMapper(new CustomerRowMapper());
        return reader;
    }

    // Stage 2: transform — same cleaning rules as the Python transform stage.
    @Bean
    public ItemProcessor<Customer, Customer> processor() {
        return customer -> {
            customer.setEmail(customer.getEmail().toLowerCase().trim());
            customer.setFirstName(customer.getFirstName().trim());
            customer.setLastName(customer.getLastName().trim());
            customer.setFullName(customer.getFirstName() + " " + customer.getLastName());
            customer.setActive("active".equals(customer.getStatus()));
            return customer;
        };
    }

    // Stage 3: load — MERGE upsert into the warehouse (PostgreSQL 15+).
    @Bean
    public JdbcBatchItemWriter<Customer> writer() {
        JdbcBatchItemWriter<Customer> writer = new JdbcBatchItemWriter<>();
        writer.setDataSource(dataSource);
        writer.setSql("""
            MERGE INTO warehouse.customers target
            USING (VALUES (:id, :email, :firstName, :lastName, :status, :active, :fullName)) source
            ON target.id = source.id
            WHEN MATCHED THEN UPDATE SET email = source.email, first_name = source.first_name,
                last_name = source.last_name, status = source.status, is_active = source.active,
                full_name = source.full_name
            WHEN NOT MATCHED THEN INSERT (id, email, first_name, last_name, status, is_active, full_name)
                VALUES (source.id, source.email, source.first_name, source.last_name, source.status, source.active, source.full_name)
            """);
        writer.setItemSqlParameterSourceProvider(new BeanPropertyItemSqlParameterSourceProvider<>());
        return writer;
    }

    // Chunk size 1000: each commit covers 1000 rows, so a failed chunk can be
    // retried without re-reading the whole table.
    @Bean
    public Step etlStep() {
        return new StepBuilder("etlStep", jobRepository)
                .<Customer, Customer>chunk(1000, transactionManager)
                .reader(reader())
                .processor(processor())
                .writer(writer())
                .build();
    }

    @Bean
    public Job etlJob() {
        return new JobBuilder("etlCustomersJob", jobRepository)
                .start(etlStep())
                .build();
    }
}

// Domain object — mirrors the stg_customers staging row.
class Customer {
    private Long id;
    private String email;
    private String firstName;
    private String lastName;
    private String status;
    private String fullName;
    private boolean active;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
}

// Maps a source row into the domain object.
class CustomerRowMapper implements org.springframework.jdbc.core.RowMapper<Customer> {
    @Override
    public Customer mapRow(java.sql.ResultSet rs, int rowNum) throws java.sql.SQLException {
        Customer c = new Customer();
        c.setId(rs.getLong("id"));
        c.setEmail(rs.getString("email"));
        c.setFirstName(rs.getString("first_name"));
        c.setLastName(rs.getString("last_name"));
        c.setStatus(rs.getString("status"));
        return c;
    }
}
