package ic.doc.templatemethod;

public class FibonacciSequence extends Sequence {

    @Override
    public int generate_term(int i) {
        if (i < 2) {
            return 1;
        }
        return generate_term(i - 1) + generate_term(i - 2);
    }
}

