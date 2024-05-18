package ic.doc.strategy;

import org.junit.Test;

import static ic.doc.matchers.IterableBeginsWith.beginsWith;
import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.Is.is;
import static org.junit.Assert.fail;

public class TriangularNumbersSequenceTest {

    final TermGenerator generator = new TriangularNumberGenerator();
    final Sequence sequence = new Sequence(generator);

    @Test
    public void definesFirstTermToBeOne() {
        assertThat(generator.term(0), is(1));
    }

    @Test
    public void hasEachTermEqualTonPlusOnenPlusTwoOverTwo() {
        assertThat(generator.term(2), is(6));
        assertThat(generator.term(3), is(10));
        assertThat(generator.term(4), is(15));
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
        assertThat(sequence, beginsWith(1, 3, 6, 10, 15));
    }

}