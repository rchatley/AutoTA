package ic.doc.strategy;

import static ic.doc.matchers.IterableBeginsWith.beginsWith;
import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.Is.is;
import static org.junit.Assert.fail;

import org.junit.Test;

public class FibonacciSequenceTest {

  final FibonacciTermGenerator generator = new FibonacciTermGenerator();
  final Sequence sequence = new Sequence(generator);

  @Test
  public void definesFirstTwoTermsToBeOne() {

    assertThat(generator.term(0), is(1));
    assertThat(generator.term(1), is(1));
  }

  @Test
  public void definesSubsequentTermsToBeTheSumOfThePreviousTwo() {

    assertThat(generator.term(2), is(2));
    assertThat(generator.term(3), is(3));
    assertThat(generator.term(4), is(5));
  }

  @Test
  public void isUndefinedForNegativeIndices() {

    try {
      generator.term(-1);
      fail("should have thrown exception");
    } catch (IllegalArgumentException e) {
      assertThat(e.getMessage(), containsString("Not defined for indices < 0"));
    }
  }

  @Test
  public void canBeIteratedThrough() {
    assertThat(sequence, beginsWith(1, 1, 2, 3, 5));
  }

}