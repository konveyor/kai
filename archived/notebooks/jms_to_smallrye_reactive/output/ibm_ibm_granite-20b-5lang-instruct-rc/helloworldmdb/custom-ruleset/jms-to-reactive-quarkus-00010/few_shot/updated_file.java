
package org.jboss.as.quickstarts.cmt.mdb;
import io.quarkus.logging.Log;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class HelloWorldMDB {
@Incoming("CMTQueue")
public void onMessage(String msg) {
Log.info("Received Message: " + msg);
}
}
