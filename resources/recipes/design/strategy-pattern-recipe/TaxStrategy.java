interface TaxStrategy {
    BigDecimal calculateTax(BigDecimal amount);
}

enum TaxRegion implements TaxStrategy {
    US {
        public BigDecimal calculateTax(BigDecimal amount) {
            return amount.multiply(new BigDecimal("0.08"));
        }
    },
    EU {
        public BigDecimal calculateTax(BigDecimal amount) {
            return amount.multiply(new BigDecimal("0.20"));
        }
    },
    UK {
        public BigDecimal calculateTax(BigDecimal amount) {
            return amount.multiply(new BigDecimal("0.20"));
        }
    };
}

class Invoice {
    private final TaxStrategy taxStrategy;

    Invoice(TaxStrategy taxStrategy) {
        this.taxStrategy = taxStrategy;
    }

    BigDecimal getTotal(BigDecimal subtotal) {
        return subtotal.add(taxStrategy.calculateTax(subtotal));
    }
}

Invoice invoice = new Invoice(TaxRegion.EU);
