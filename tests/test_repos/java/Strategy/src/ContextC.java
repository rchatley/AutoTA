public class ContextC {
    private Strategy strategy;

    public ContextC(Strategy strategy) {
        this.strategy = strategy;
    }

    public void operation() {
        strategy.algorithm();
    }
}