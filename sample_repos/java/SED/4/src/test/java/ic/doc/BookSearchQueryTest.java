package ic.doc;

import ic.doc.catalogues.Catalogue;
import org.jmock.Expectations;
import org.jmock.integration.junit4.JUnitRuleMockery;
import org.junit.Rule;
import org.junit.Test;

public class BookSearchQueryTest {

  @Rule
  public JUnitRuleMockery context = new JUnitRuleMockery();
  private final Catalogue catalogue = context.mock(Catalogue.class);
  private final BookSearchQueryBuilder builder = new BookSearchQueryBuilder(catalogue);

  @Test
  public void searchesForBooksInLibraryCatalogueByAuthorSurname() {
    final String surname = "dickens";
    context.checking(new Expectations() {{
      oneOf(catalogue).searchFor("LASTNAME='" + surname + "' ");
    }});

    builder.withSurname(surname).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueByAuthorFirstname() {
    final String firstname = "Jane";
    context.checking(new Expectations() {{
      oneOf(catalogue).searchFor("FIRSTNAME='" + firstname + "' ");
    }});

    builder.withFirstname(firstname).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueByTitle() {
    final String title = "Two Cities";
    context.checking(new Expectations() {{
      oneOf(catalogue).searchFor("TITLECONTAINS(" + title + ") ");
    }});

    builder.withTitle(title).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueBeforeGivenPublicationYear() {
    final int latestDate = 1700;
    context.checking(new Expectations() {{
      oneOf(catalogue).searchFor("PUBLISHEDBEFORE(" + latestDate + ") ");
    }});

    builder.withLatestDate(latestDate).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueAfterGivenPublicationYear() {
    final int earliestDate = 1950;
    context.checking(new Expectations() {{
      oneOf(catalogue).searchFor("PUBLISHEDAFTER(" + earliestDate + ") ");
    }});

    builder.withEarliestDate(earliestDate).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueWithCombinationOfParameters() {
    final String surname = "dickens";
    final int latestDate = 1840;
    context.checking(new Expectations() {{
      oneOf(catalogue).searchFor("LASTNAME='" + surname + "' PUBLISHEDBEFORE(" + latestDate + ") ");
    }});

    builder.withSurname(surname).withLatestDate(latestDate).build().execute();
  }

  @Test
  public void searchesForBooksInLibraryCatalogueWithCombinationOfTitleAndOtherParameters() {
    final String title = "of";
    final int earliestDate = 1800;
    final int latestDate = 2000;
    context.checking(new Expectations() {{
      oneOf(catalogue).searchFor(
          "TITLECONTAINS(" + title + ") PUBLISHEDAFTER(" + earliestDate + ") PUBLISHEDBEFORE("
              + latestDate + ") ");
    }});

    builder.withTitle(title).withEarliestDate(earliestDate).withLatestDate(latestDate).build()
        .execute();
  }
}
