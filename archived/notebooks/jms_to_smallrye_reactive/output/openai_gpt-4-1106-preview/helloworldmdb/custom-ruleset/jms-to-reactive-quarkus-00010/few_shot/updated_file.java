
package org.jboss.as.quickstarts.mdb;

import io.quarkus.logging.Log;
import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.reactive.messaging.Incoming;

/**
 * <p>
 * A simple bean that asynchronously receives and processes the messages that are sent to the queue using Quarkus.
 * </p>
 *
 * @author Serge Pagop (spagop@redhat.com)
 */
@ApplicationScoped
public class HelloWorldQueueMDB {

    @Incoming("helloworld-queue")
    public void onMessage(String msg) {
        Log.info("Received Message from queue: " + msg);
    }
}
