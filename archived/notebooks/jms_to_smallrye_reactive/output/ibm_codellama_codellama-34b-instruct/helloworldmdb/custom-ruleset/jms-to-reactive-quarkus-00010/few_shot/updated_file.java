
package org.jboss.as.quickstarts.mdb;

import io.quarkus.logging.Log;
import jakarta.enterprise.context.ApplicationScoped;

/**
 * <p>
 * A simple Message Driven Bean that asynchronously receives and processes the messages that are sent to the queue.
 * </p>
 *
 * @author Serge Pagop (spagop@redhat.com)
 */
@ApplicationScoped
public class HelloWorldQueueMDB {

    private static final Logger LOGGER = Logger.getLogger(HelloWorldQueueMDB.class.toString());

    /**
     * @see MessageListener#onMessage(Message)
     */
    @Incoming("CMTQueue")
    public void onMessage(String msg) {
        Log.info("Received Message from queue: " + msg);
    }
}
