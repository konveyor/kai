package org.jboss.as.quickstarts.servlet;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.jms.Destination;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;

import jakarta.ws.rs.core.Context;
import java.util.List;
import java.util.ArrayList;
import jakarta.ws.rs.core.MultivaluedMap;
import jakarta.ws.rs.core.UriInfo;
import jakarta.ws.rs.core.MediaType;

import jakarta.ws.rs.core.Response;


@ApplicationScoped
@Path("/HelloWorldMDBServletClient")
public class HelloWorldMDBServletClient {

    private static final int MSG_COUNT = 5;

    @Inject
    @Channel("HELLOWORLDMDBQueue")
    Emitter<String> queueEmitter;

    @Inject
    @Channel("HELLOWORLDMDBTopic")
    Emitter<String> topicEmitter;


    @GET
    @Produces(MediaType.TEXT_HTML)
    public Response doGet(@Context UriInfo uriInfo) {
        MultivaluedMap<String, String> queryParams = uriInfo.getQueryParameters();
        boolean isUsingTopic = queryParams.containsKey("topic");


        Emitter<String> emitter = isUsingTopic ? topicEmitter : queueEmitter;
        String destination = isUsingTopic ? "topic" : "queue";
      StringBuilder response = new StringBuilder();
        response.append("<h1>Quickstart: Example demonstrates the use of eclipse reactive messaging in Quarkus.</h1>");
        response.append("<p>Sending messages to <em>").append(destination).append("</em></p>");
        response.append("<h2>The following messages will be sent to the destination:</h2>");

     List<String> messages = generateMessages(emitter);
        response.append("<ol>");
        for (String message : messages) {
            response.append("<li>").append(message).append("</li>");
        }
        response.append("</ol>");


        response.append("<p><i>Check your console or logs to see the result of messages processing.</i></p>");

        return Response.ok(response.toString()).build();
    
    }

    private List<String> generateMessages(Emitter<String> emitter) {
        List<String> messages = new ArrayList<>();

        for (int i = 1; i <= MSG_COUNT; i++) {
            String messageText = "This is message " + i;
            messages.add(messageText);
            emitter.send(messageText);
        }

        return messages;
    }
}
