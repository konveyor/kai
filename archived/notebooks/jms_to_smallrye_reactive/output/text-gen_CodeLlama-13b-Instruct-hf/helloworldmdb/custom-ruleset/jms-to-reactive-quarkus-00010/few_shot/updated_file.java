
package org.jboss.as.quickstarts.mdb;

import java.util.logging.Logger;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.jboss.as.quickstarts.mdb.HelloWorldQueueMDB;

@ApplicationScoped
public class HelloWorldQueueMDB {

   private static final Logger LOGGER = Logger.getLogger(HelloWorldQueueMDB.class.toString());

   @Incoming("CMTQueue")
   public void onMessage(String msg) {
       LOGGER.info("Received Message from queue: " + msg);
   }
}
