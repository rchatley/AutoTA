package ic.doc;

import ic.doc.catalogues.Catalogue;

public class BookSearchQueryBuilder {
  private String firstName;
  private String lastName;
  private String title;
  private Integer publishedAfterDate;
  private Integer publishedBeforeDate;
  private final Catalogue catalogue;

  public BookSearchQueryBuilder(Catalogue catalogue) {
    this.catalogue = catalogue;
  }

  public BookSearchQuery build() {
    return new BookSearchQuery(firstName, lastName, title, publishedAfterDate, publishedBeforeDate, catalogue);
  }

  public BookSearchQueryBuilder withFirstName(String firstName) {
    this.firstName = firstName;
    return this;
  }

  public BookSearchQueryBuilder withLastName(String lastName) {
    this.lastName = lastName;
    return this;
  }

  public BookSearchQueryBuilder containingTitle(String title) {
    this.title = title;
    return this;
  }

  public BookSearchQueryBuilder publishedAfter(Integer minPublicationDate) {
    this.publishedAfterDate = minPublicationDate;
    return this;
  }

  public BookSearchQueryBuilder publishedBefore(Integer maxPublicationDate) {
    this.publishedBeforeDate = maxPublicationDate;
    return this;
  }
}