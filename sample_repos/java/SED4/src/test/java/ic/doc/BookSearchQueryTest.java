package ic.doc;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;

import java.util.List;

import ic.doc.catalogues.BritishLibraryCatalogue;
import ic.doc.catalogues.LibraryCatalogue;
import org.jmock.Expectations;
import org.jmock.integration.junit4.JUnitRuleMockery;
import org.junit.Rule;
import org.junit.Test;

public class BookSearchQueryTest {

  @Rule
  public JUnitRuleMockery context = new JUnitRuleMockery();
  LibraryCatalogue anyLib = context.mock(LibraryCatalogue.class);

  LibraryCatalogue britishLib = BritishLibraryCatalogue.getInstance();


  @Test
  public void searchesForBooksInLibraryCatalogueByAuthorSurname() {

    List<Book> books = new BookSearchQueryBuilder().bySurname("dickens")
        .build().execute(britishLib);

    assertThat(books.size(), is(2));
    assertTrue(books.get(0).matchesAuthor("dickens"));
  }

  @Test
  public void searchesForBooksInLibraryCatalogueByAuthorFirstname() {

    List<Book> books = new BookSearchQueryBuilder().byFirstname("Jane")
        .build().execute(britishLib);

    assertThat(books.size(), is(2));
    assertTrue(books.get(0).matchesAuthor("Austen"));
  }

  @Test
  public void searchesForBooksInLibraryCatalogueByTitle() {

    List<Book> books = new BookSearchQueryBuilder().byTitle("Two Cities")
        .build().execute(britishLib);

    assertThat(books.size(), is(1));
    assertTrue(books.get(0).matchesAuthor("dickens"));
  }

  @Test
  public void searchesForBooksInLibraryCatalogueBeforeGivenPublicationYear() {

    List<Book> books = new BookSearchQueryBuilder().beforeYear(1700)
        .build().execute(britishLib);

    assertThat(books.size(), is(1));
    assertTrue(books.get(0).matchesAuthor("Shakespeare"));
  }

  @Test
  public void searchesForBooksInLibraryCatalogueAfterGivenPublicationYear() {

    List<Book> books = new BookSearchQueryBuilder().afterYear(1950)
        .build().execute(britishLib);

    assertThat(books.size(), is(1));
    assertTrue(books.get(0).matchesAuthor("Golding"));
  }

  @Test
  public void searchesForBooksInLibraryCatalogueWithCombinationOfParameters() {

    List<Book> books = new BookSearchQueryBuilder()
        .bySurname("dickens").afterYear(1840)
        .build().execute(britishLib);

    assertThat(books.size(), is(1));
    assertTrue(books.get(0).matchesAuthor("charles dickens"));
  }

  @Test
  public void searchesForBooksInLibraryCatalogueWithCombinationOfTitleAndOtherParameters() {

    List<Book> books = new BookSearchQueryBuilder()
        .byTitle("of").afterYear(1800).beforeYear(2000)
        .build().execute(britishLib);

    assertThat(books.size(), is(3));
    assertTrue(books.get(0).matchesAuthor("charles dickens"));
  }

  @Test
  public void anyLibraryCanSearch() {
    context.checking(new Expectations() {{
      oneOf(anyLib).searchFor(
          "FIRSTNAME='Jane' LASTNAME='dickens' "
              + "TITLECONTAINS(Two Cities) PUBLISHEDAFTER(1800) PUBLISHEDBEFORE(2000) ");
    }});

    new BookSearchQueryBuilder()
        .byFirstname("Jane").bySurname("dickens").byTitle("Two Cities")
        .afterYear(1800).beforeYear(2000)
        .build().execute(anyLib);
  }
}
