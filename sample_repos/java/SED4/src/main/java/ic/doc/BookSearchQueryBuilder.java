package ic.doc;

public class BookSearchQueryBuilder {
  private String firstname;
  private String surname;
  private String title;
  private Integer after;
  private Integer before;


  public BookSearchQueryBuilder byFirstname(String firstname) {
    this.firstname = firstname;
    return this;
  }

  public BookSearchQueryBuilder bySurname(String surname) {
    this.surname = surname;
    return this;
  }

  public BookSearchQueryBuilder byTitle(String title) {
    this.title = title;
    return this;
  }

  public BookSearchQueryBuilder afterYear(int year) {
    this.after = year;
    return this;
  }

  public BookSearchQueryBuilder beforeYear(int year) {
    this.before = year;
    return this;
  }

  public BookSearchQuery build() {
    return new BookSearchQuery(firstname, surname, title, after, before);
  }
}
