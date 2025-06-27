import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Coroutine, TypeVar

from kai_mcp_solution_server.dao import SolutionChangeSet, SolutionFile

T = TypeVar("T")


# https://stackoverflow.com/questions/55647753/call-async-function-from-sync-function-while-the-synchronous-function-continues
def run_coroutine_sync(coroutine: Coroutine[Any, Any, T], timeout: float = 30) -> T:
    def run_in_new_loop():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(coroutine)
        finally:
            new_loop.close()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coroutine)

    if threading.current_thread() is threading.main_thread():
        if not loop.is_running():
            return loop.run_until_complete(coroutine)
        else:
            with ThreadPoolExecutor() as pool:
                future = pool.submit(run_in_new_loop)
                return future.result(timeout=timeout)
    else:
        return asyncio.run_coroutine_threadsafe(coroutine, loop).result()


async def main() -> None:
    s = SolutionChangeSet(
        diff="""\

diff --git a/tests/data/1/PriceChangeNotifierMDB.java b/tests/data/1/PriceChangeAlertConsumer.java
index 42003ae..2c75b13 100644
--- a/tests/data/1/PriceChangeNotifierMDB.java
+++ b/tests/data/1/PriceChangeAlertConsumer.java
@@ -1,48 +1,35 @@
-import javax.ejb.MessageDriven;
-import javax.ejb.ActivationConfigProperty;
-import javax.inject.Inject;
-import javax.jms.MessageListener;
-import javax.jms.Message;
-import javax.jms.TextMessage;
-import javax.jms.JMSException;
+import jakarta.enterprise.context.ApplicationScoped;
+import jakarta.inject.Inject;
+import jakarta.transaction.Transactional;
+import org.eclipse.microprofile.reactive.messaging.Incoming;
 import java.math.BigDecimal;
 
-
-@MessageDriven(activationConfig = {
-    @ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "jms/topic/ProductUpdates"),
-    @ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic")
-})
-public class PriceChangeNotifierMDB implements MessageListener {
+@ApplicationScoped
+public class PriceChangeAlertConsumer {
 
     private static final BigDecimal PRICE_CHANGE_ALERT_PERCENTAGE = new BigDecimal("0.10");
 
     @Inject
-    private ProductService productService; // Assumed defined and injectable
+    ProductService productService; 
 
-    public void onMessage(Message rcvMessage) {
-        TextMessage msg;
-        try {
-            if (rcvMessage instanceof TextMessage) {
-                msg = (TextMessage) rcvMessage;
-                String eventStr = msg.getText();
-                String productId = "sampleProductId"; 
-                BigDecimal newPrice = new BigDecimal("120.00"); 
+    @Incoming("product-updates-channel")
+    @Transactional
+    public void processPriceUpdate(ProductUpdateEvent event) { /
+        System.out.println("Quarkus received product update for: " + event.getProductId());
+        BigDecimal oldPrice = productService.getCurrentPrice(event.getProductId());
 
+        if (oldPrice == null || oldPrice.compareTo(BigDecimal.ZERO) == 0) {
+             System.err.println("Quarkus: Old price not found or zero for " + event.getProductId() + ", cannot calculate change.");
+             return;
+        }
 
-                BigDecimal oldPrice = productService.getCurrentPrice(productId);
-                BigDecimal priceDifference = newPrice.subtract(oldPrice).abs();
-                BigDecimal percentageChange = priceDifference.divide(oldPrice, 4, BigDecimal.ROUND_HALF_UP);
+        BigDecimal priceDifference = event.getNewPrice().subtract(oldPrice).abs();
+        BigDecimal percentageChange = priceDifference.divide(oldPrice, 4, BigDecimal.ROUND_HALF_UP);
 
-                if (percentageChange.compareTo(PRICE_CHANGE_ALERT_PERCENTAGE) > 0) {
-                    System.out.println("ALERT: Price for item " + productId +
-                                       " changed significantly from " + oldPrice + " to " + newPrice);
-                    productService.logPriceChangeAlert(productId, oldPrice, newPrice);
-                }
-            }
-        } catch (JMSException jmse) {
-            System.err.println("PriceChangeNotifierMDB: JMSException: " + jmse.getMessage());
-        } catch (Exception e) {
-            System.err.println("PriceChangeNotifierMDB: Exception: " + e.getMessage());
+        if (percentageChange.compareTo(PRICE_CHANGE_ALERT_PERCENTAGE) > 0) {
+            System.out.println("QUARKUS_ALERT: Price for item " + event.getProductId() +
+                               " changed significantly from " + oldPrice + " to " + event.getNewPrice());
+            productService.logPriceChangeAlert(event.getProductId(), oldPrice, event.getNewPrice());
         }
     }
 }
\ No newline at end of file

""",
        before=[
            SolutionFile(
                uri="file://PriceChangeNotifierMDB.java",
                content="""\

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
    private ProductService productService; // Assumed defined and injectable

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

""",
            )
        ],
        after=[
            SolutionFile(
                uri="file://PriceChangeAlertConsumer.java",
                content="""\
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

""",
            )
        ],
    )

    print(s.model_dump_json(indent=2))

    # settings = SolutionServerSettings()
    # ctx = KaiSolutionServerContext(settings)
    # await ctx.create()

    # print(settings.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
