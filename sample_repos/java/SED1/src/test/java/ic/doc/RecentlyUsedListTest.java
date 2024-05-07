package ic.doc;

// Tests to implement:
// 1. The list should be empty when initialised.
// 2. We should be able to add things to the list.
// 3. We should be able to retrieve items from the list.
// 4. The most recent item should be first in the list.
// 5. Items in the list are unique, so duplicate insertions
//    should be moved rather than added

import org.junit.Test;

import java.util.InputMismatchException;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.Is.is;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

public class RecentlyUsedListTest {

  RecentlyUsedList testList = new RecentlyUsedList();

  // 1. The list should be empty when initialised.
  @Test
  public void listIsEmptyWhenInitialised() {
    assertThat(testList.size(), is(0));
  }

  // 2. We should be able to add things to the list.
  @Test
  public void ableToAddThingsToList() {
    String item = "012345";
    testList.add(item);
    assertTrue(testList.contains(item));
  }

  // Test the input type is strictly string
  @Test
  public void inputTypeIsString() {
    boolean thrown = false;
    testList.add("This is a test");
    try {
      testList.add(100);
      fail("should have thrown error");
    } catch (InputMismatchException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  // 3. We should be able to retrieve items from the list.
  @Test
  public void ableToRetrieveFromList() {
    String item = "012345";
    testList.add(item);
    assertThat(testList.getItemAt(0), is(item));
  }

  @Test
  public void testArrayIndexOutOfBoundsExceptionThrown() {
    boolean thrown = false;
    try {
      testList.getItemAt(1);
      fail("should have thrown exception");
    } catch (ArrayIndexOutOfBoundsException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  // 4. The most recent item should be first in the list.
  @Test
  public void mostRecentItemIsFirstInList() {
    String item1 = "Imperial";
    String item2 = "Cambridge";
    testList.add(item1);
    testList.add(item2);

    assertThat(testList.getMostRecent(), is(item2));
  }

  // 5. Items in the list are unique, so duplicate insertions
  //    should be moved rather than added
  @Test
  public void duplicateInsertionsMoved() {
    String item1 = "Imperial";
    String item2 = "Cambridge";
    testList.add(item1);
    testList.add(item2);
    testList.add(item1);

    assertThat(testList.size(), is(2));
    assertThat(testList.getMostRecent(), is(item1));
  }

}
