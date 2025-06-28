import javax.ejb.MessageDriven;
import javax.ejb.ActivationConfigProperty;
import javax.inject.Inject;
import javax.jms.MessageListener;
import javax.jms.Message;
import javax.jms.TextMessage;
import javax.jms.JMSException;
import java.math.BigDecimal;


@MessageDriven(activationConfig = {
    @ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "jms/topic/ProductUpdates"),
    @ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic")
})
public class PriceChangeNotifierMDB implements MessageListener {

    private static final BigDecimal PRICE_CHANGE_ALERT_PERCENTAGE = new BigDecimal("0.10");

    @Inject
    private ProductService productService; /**
     * Processes incoming JMS messages to detect significant product price changes and triggers alerts if the change exceeds a defined threshold.
     *
     * If the received message is a `TextMessage`, the method retrieves the product's current price and compares it to a new price (currently hardcoded). If the percentage change exceeds 10%, it logs an alert and notifies the product service.
     */

    public void onMessage(Message rcvMessage) {
        TextMessage msg;
        try {
            if (rcvMessage instanceof TextMessage) {
                msg = (TextMessage) rcvMessage;
                String eventStr = msg.getText();
                String productId = "sampleProductId"; 
                BigDecimal newPrice = new BigDecimal("120.00"); 


                BigDecimal oldPrice = productService.getCurrentPrice(productId);
                BigDecimal priceDifference = newPrice.subtract(oldPrice).abs();
                BigDecimal percentageChange = priceDifference.divide(oldPrice, 4, BigDecimal.ROUND_HALF_UP);

                if (percentageChange.compareTo(PRICE_CHANGE_ALERT_PERCENTAGE) > 0) {
                    System.out.println("ALERT: Price for item " + productId +
                                       " changed significantly from " + oldPrice + " to " + newPrice);
                    productService.logPriceChangeAlert(productId, oldPrice, newPrice);
                }
            }
        } catch (JMSException jmse) {
            System.err.println("PriceChangeNotifierMDB: JMSException: " + jmse.getMessage());
        } catch (Exception e) {
            System.err.println("PriceChangeNotifierMDB: Exception: " + e.getMessage());
        }
    }
}