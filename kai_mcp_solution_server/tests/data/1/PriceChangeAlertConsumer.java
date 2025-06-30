import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import java.math.BigDecimal;

@ApplicationScoped
public class PriceChangeAlertConsumer {

    private static final BigDecimal PRICE_CHANGE_ALERT_PERCENTAGE = new BigDecimal("0.10");

    @Inject
    ProductService productService; 

    @Incoming("product-updates-channel")
    @Transactional
    public void processPriceUpdate(ProductUpdateEvent event) { /
        System.out.println("Quarkus received product update for: " + event.getProductId());
        BigDecimal oldPrice = productService.getCurrentPrice(event.getProductId());

        if (oldPrice == null || oldPrice.compareTo(BigDecimal.ZERO) == 0) {
             System.err.println("Quarkus: Old price not found or zero for " + event.getProductId() + ", cannot calculate change.");
             return;
        }

        BigDecimal priceDifference = event.getNewPrice().subtract(oldPrice).abs();
        BigDecimal percentageChange = priceDifference.divide(oldPrice, 4, BigDecimal.ROUND_HALF_UP);

        if (percentageChange.compareTo(PRICE_CHANGE_ALERT_PERCENTAGE) > 0) {
            System.out.println("QUARKUS_ALERT: Price for item " + event.getProductId() +
                               " changed significantly from " + oldPrice + " to " + event.getNewPrice());
            productService.logPriceChangeAlert(event.getProductId(), oldPrice, event.getNewPrice());
        }
    }
}