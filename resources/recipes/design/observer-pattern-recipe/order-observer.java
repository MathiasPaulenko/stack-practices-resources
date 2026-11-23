import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

class Order {
    private String status;
    private final PropertyChangeSupport support;

    Order() {
        this.support = new PropertyChangeSupport(this);
    }

    void addPropertyChangeListener(PropertyChangeListener listener) {
        support.addPropertyChangeListener(listener);
    }

    void removePropertyChangeListener(PropertyChangeListener listener) {
        support.removePropertyChangeListener(listener);
    }

    void setStatus(String newStatus) {
        String oldStatus = this.status;
        this.status = newStatus;
        support.firePropertyChange("status", oldStatus, newStatus);
    }
}

class OrderLogger implements PropertyChangeListener {
    public void propertyChange(java.beans.PropertyChangeEvent evt) {
        System.out.printf("Order %s changed from %s to %s%n",
            evt.getSource(), evt.getOldValue(), evt.getNewValue());
    }
}

public class OrderObserverDemo {
    public static void main(String[] args) {
        Order order = new Order();
        order.addPropertyChangeListener(new OrderLogger());
        order.setStatus("shipped");
    }
}
