
@ApplicationScoped
public class HelloWorldMDB {

   @Incoming("CMTQueue")
   public void onMessage(String msg) {
       Log.info("Received Message: " + msg);
   }
}
