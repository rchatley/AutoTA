package ic.doc.templatemethod;

public class TriangleNumbersSequence extends Sequence {

    @Override
    public int generate_term(int i) {
        if (i == 0) {
            return 1;
        }
        return (i + 1) * (i + 2) / 2;
    }
}
