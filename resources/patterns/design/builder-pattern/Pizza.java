// Fluent Builder as a nested static class (the Java convention).

public class Pizza {
    private final String size;
    private final boolean cheese;
    private final boolean pepperoni;
    private final boolean mushrooms;

    private Pizza(Builder builder) {
        this.size = builder.size;
        this.cheese = builder.cheese;
        this.pepperoni = builder.pepperoni;
        this.mushrooms = builder.mushrooms;
    }

    public static class Builder {
        private final String size;
        private boolean cheese = false;
        private boolean pepperoni = false;
        private boolean mushrooms = false;

        public Builder(String size) { this.size = size; }
        public Builder cheese() { this.cheese = true; return this; }
        public Builder pepperoni() { this.pepperoni = true; return this; }
        public Builder mushrooms() { this.mushrooms = true; return this; }
        public Pizza build() { return new Pizza(this); }
    }

    @Override
    public String toString() {
        return "Pizza(" + size + ", cheese=" + cheese + ", pepperoni=" + pepperoni
            + ", mushrooms=" + mushrooms + ")";
    }

    public static void main(String[] args) {
        Pizza pizza = new Pizza.Builder("large").cheese().pepperoni().build();
        System.out.println(pizza);
        // Pizza(large, cheese=true, pepperoni=true, mushrooms=false)
    }
}
