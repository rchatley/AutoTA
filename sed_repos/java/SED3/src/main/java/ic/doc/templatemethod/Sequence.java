package ic.doc.templatemethod;

import java.util.Iterator;

public abstract class Sequence implements Iterable<Integer> {

    public final int term(int i) {
        if (i < 0) {
            throw new IllegalArgumentException("Not defined for indices < 0");
        }
        return generate_term(i);
    }


    public abstract int generate_term(int i);

    public Iterator<Integer> iterator() {
        return new SequenceIterator();
    }

    private class SequenceIterator implements Iterator<Integer> {

        private int index = 0;

        @Override
        public boolean hasNext() {
            return true;
        }

        @Override
        public Integer next() {
            return term(index++);
        }

        @Override
        public void remove() {
            throw new UnsupportedOperationException("Remove is not implemented");
        }
    }
}