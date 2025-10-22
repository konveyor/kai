
package org.jboss.as.quickstarts.mdb;

import io.smallrye.reactive.messaging.annotations.Blocking;
import io.smallrye.reactive.messaging.annotations.Incoming;
import org.eclipse.microprofile.reactive.messaging.Message;
import org.jboss.logging.Logger;

import javax.enterprise.context.ApplicationScoped;
import javax.jms.JMSException;
import javax.jms.TextMessage;

/**
 * <p>
 * A simple bean that asynchronously receives and processes the messages that are sent to the queue.
 * </p>
 *
 * @author Serge Pagop (spagop@redhat.com)
 */
@ApplicationScoped
public class HelloWorldQueueMDB {

    private static final Logger LOGGER = Logger.getLogger(HelloWorldQueueMDB.class);

    /**
     * The `onMessage` method is now replaced with a method that consumes messages from the channel named "helloworld".
     * The `@Incoming` annotation is used to specify the channel name which is configured in the `application.properties`.
     */
    @Incoming("helloworld")
    @Blocking
    public void receive(Message<String> message) {
        try {
            String payload = message.getPayload();
            LOGGER.info("Received Message from queue: " + payload);
        } catch (Exception e) {
            LOGGER.error("Failed to process message", e);
            throw new RuntimeException(e);
        }
    }
}
