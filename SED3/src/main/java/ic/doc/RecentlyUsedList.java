package ic.doc;

import java.util.InputMismatchException;
import java.util.Stack;

public class RecentlyUsedList<T> {

  private Stack<T> recentlyUsedList = new Stack<>();

  public int size() {
    return recentlyUsedList.size();
  }

  public void add(T item) {
    if (size() == 0) {
      recentlyUsedList.push(item);
    } else if (item.getClass().isInstance(recentlyUsedList.peek())) {
      recentlyUsedList.remove(item);
      recentlyUsedList.push(item);
    } else {
      throw new InputMismatchException();
    }
  }

  public boolean contains(T item) {
    return recentlyUsedList.contains(item);
  }

  public T getItemAt(int index) {
    if (index < 0 || index >= size()) {
      throw new ArrayIndexOutOfBoundsException();
    }
    return recentlyUsedList.get(index);
  }

  public T getMostRecent() {
    return recentlyUsedList.peek();
  }
}
