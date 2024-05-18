public class ContextC {
    private Strategy strategy;

    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }

    public void operation() {
        strategy.algorithm();
    }
}