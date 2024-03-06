
package org.jboss.as.quickstarts.ejb.remote.stateful;

import jakarta.ws.rs.Path;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

/**
 * CounterBean is now a JAX-RS resource that provides RESTful endpoints to increment,
 * decrement, and get the current count.
 */
@Path("/counter")
public class CounterBean {

    private int count = 0;

    @GET
    @Path("/increment")
    @Produces(MediaType.TEXT_PLAIN)
    public void increment() {
        this.count++;
    }

    @GET
    @Path("/decrement")
    @Produces(MediaType.TEXT_PLAIN)
    public void decrement() {
        this.count--;
    }

    @GET
    @Path("/count")
    @Produces(MediaType.TEXT_PLAIN)
    public int getCount() {
        return this.count;
    }
}
