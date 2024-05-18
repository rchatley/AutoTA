package ic.doc.strategy;

import org.junit.Test;

import static ic.doc.matchers.IterableBeginsWith.beginsWith;
import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.Is.is;
import static org.junit.Assert.fail;

public class TriangleNumbersSequenceTest {

    final Sequence sequence = new Sequence(new TriangleNumbersGenerator());

    @Test
    public void definesFirstTermToBeOne() {
        assertThat(sequence.term(0), is(1));
    }

    @Test
    public void definesSubsequentTermsToBeHalfOfTheProductOfNextTwoIndices() {

        assertThat(sequence.term(1), is((2 * 3) / 2));
        assertThat(sequence.term(2), is((3 * 4) / 2));
        assertThat(sequence.term(3), is((4 * 5) / 2));
    }

    @Test
    public void isUndefinedForNegativeIndices() {

        try {
            sequence.term(-1);
            fail("Should have thrown exception");
        } catch (IllegalArgumentException e) {
            assertThat(e.getMessage(), containsString("Not defined for indices < 0"));
        }
    }

    @Test
    public void canBeIteratedThrough() {
        assertThat(sequence, beginsWith(1, 3, 6, 10, 15));
    }
}