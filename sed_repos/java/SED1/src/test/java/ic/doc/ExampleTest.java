package ic.doc;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.Is.is;

import org.junit.Test;

public class ExampleTest {

  @Test
  public void canAnswerTheUniversalQuestion() {
    assertThat(new Example().answer(), is(42));
  }

}