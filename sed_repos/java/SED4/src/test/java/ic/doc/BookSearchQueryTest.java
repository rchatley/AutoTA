package ic.doc;

import ic.doc.catalogues.Catalogue;
import org.jmock.Expectations;
import org.jmock.integration.junit4.JUnitRuleMockery;
import org.junit.Rule;
import org.junit.Test;

import java.util.List;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;

public class BookSearchQueryTest {

  @Rule
  public JUnitRuleMockery context = new JUnitRuleMockery();

  Catalogue catalogue = context.mock(Catalogue.class);

  BookSearchQueryBuilder builder = new BookSearchQueryBuilder(catalogue);
  List<Book> books;

  @Test
  public void searchesForBooksInLibraryCatalogueByAuthorSurname() {
    context.checking(
            new Expectations() {
              {
                exactly(1).of(catalogue).searchFor("LASTNAME='dickens' ");
              }
            });

    books = builder.withLastName("dickens").build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueByAuthorFirstname() {
    context.checking(
            new Expectations() {
              {
                exactly(1).of(catalogue).searchFor("FIRSTNAME='Jane' ");
                will(
                        returnValue(
                                List.of(
                                        new Book("Pride and Prejudice", "Jane Austen", 1813),
                                        new Book("Pride and Prejudice", "Jane Austen", 1813))));
              }
            });

    books = builder.withFirstName("Jane").build().execute();

    assertThat(books.size(), is(2));
    assertTrue(books.get(0).matchesAuthor("Austen"));
  }

  @Test
  public void searchesForBooksInLibraryCatalogueByTitle() {
    context.checking(
            new Expectations() {
              {
                exactly(1).of(catalogue).searchFor("TITLECONTAINS(Two Cities) ");
              }
            });

    builder.containingTitle("Two Cities").build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueBeforeGivenPublicationYear() {
    context.checking(
            new Expectations() {
              {
                exactly(1).of(catalogue).searchFor("PUBLISHEDBEFORE(1700) ");
              }
            });

    builder.publishedBefore(1700).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueAfterGivenPublicationYear() {

    context.checking(
            new Expectations() {
              {
                exactly(1).of(catalogue).searchFor("PUBLISHEDAFTER(1950) ");
              }
            });

    builder.publishedAfter(1950).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueWithCombinationOfParameters() {

    context.checking(
            new Expectations() {
              {
                exactly(1).of(catalogue).searchFor("LASTNAME='dickens' PUBLISHEDBEFORE(1840) ");
              }
            });

    builder.withLastName("dickens").publishedBefore(1840).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueWithCombinationOfTitleAndOtherParameters() {

    context.checking(
            new Expectations() {
              {
                exactly(1)
                        .of(catalogue)
                        .searchFor("TITLECONTAINS(of) PUBLISHEDAFTER(1800) PUBLISHEDBEFORE(2000) ");
              }
            });

    builder.containingTitle("of").publishedAfter(1800).publishedBefore(2000).build().execute();
  }
}
