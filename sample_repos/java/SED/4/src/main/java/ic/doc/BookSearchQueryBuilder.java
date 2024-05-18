package ic.doc;

import ic.doc.catalogues.Catalogue;

public class BookSearchQueryBuilder {

  private String name1 = null;
  private String name2 = null;
  private String title = null;
  private Integer date1 = null;
  private Integer date2 = null;
  private final Catalogue catalogue;

  public BookSearchQueryBuilder(final Catalogue catalogue) {
    nullCheck(catalogue);
    this.catalogue = catalogue;
  }

  private static void nullCheck(Object input) {
    if (input == null) {
      throw new IllegalArgumentException("Builder class does not accept null arguments!");
    }
  }

  public BookSearchQueryBuilder withFirstname(final String firstname) {
    nullCheck(firstname);
    this.name1 = firstname;
    return this;
  }

  public BookSearchQueryBuilder withSurname(final String surname) {
    nullCheck(surname);
    this.name2 = surname;
    return this;
  }

  public BookSearchQueryBuilder withTitle(final String title) {
    nullCheck(title);
    this.title = title;
    return this;
  }

  public BookSearchQueryBuilder withEarliestDate(final int earliestDate) {
    this.date1 = earliestDate;
    return this;
  }

  public BookSearchQueryBuilder withLatestDate(final int latestDate) {
    this.date2 = latestDate;
    return this;
  }

  public BookSearchQuery build() {
    return new BookSearchQuery(name1, name2, title, date1, date2, catalogue);
  }
}
