
import jakarta.enterprise.context.ApplicationScoped;
import io.quarkus.logging.Log;

public class HelloWorldQueueMDB {

    @Incoming("CMTQueue")
    public void onMessage(String msg) {
        Log.info("Received Message: " + msg);
    }
}
