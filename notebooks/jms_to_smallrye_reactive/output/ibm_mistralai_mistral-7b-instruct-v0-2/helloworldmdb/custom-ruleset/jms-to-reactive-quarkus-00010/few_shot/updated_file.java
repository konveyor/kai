
package org.jboss.as.quickstarts.mdb;

import io.quarkus.logging.Log;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import jakarta.inject.Inject;
import org.jboss.shrine.api.events.OrderEvent;

/**
 * A simple Message Driven Bean that asynchronously receives and processes the messages that are sent to the queue.
 *
 * @author Serge Pagop (spagop@redhat.com)
 */
@ApplicationScoped
public class HelloWorldQueueMDB {

    @Inject
    Log log;

    public void onMessage(@Observes OrderEvent event) {
        log.info("Received Message from queue: " + event.getMessage());
    }
}
