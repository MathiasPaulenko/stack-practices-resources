// Spring for GraphQL controller from the recipe.
//
// Drop this into a Spring Boot project with the `spring-boot-starter-graphql`
// dependency and place schema.graphqls in src/main/resources/graphql/.
// The endpoint lands on /graphql by default.

import java.util.ArrayList;
import java.util.List;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

@Controller
public class BookController {

    private final List<Book> books = new ArrayList<>(List.of(
        new Book("Clean Code", "Robert C. Martin", 464),
        new Book("The Pragmatic Programmer", "Andy Hunt", 352)
    ));

    @QueryMapping
    public List<Book> books() {
        return books;
    }

    @MutationMapping
    public Book addBook(@Argument String title,
                        @Argument String author,
                        @Argument int pages) {
        Book book = new Book(title, author, pages);
        books.add(book);
        return book;
    }
}

record Book(String title, String author, int pages) {}
