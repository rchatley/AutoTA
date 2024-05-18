package ic.doc.strategy;

public class FibonacciGenerator implements TermGenerator {
    @Override
    public int term(int i) {
        if (i < 2) {
            return 1;
        }
        return term(i - 1) + term(i - 2);
    }
}