from langchain_community.chat_models import ChatOpenAI

template = """
You are an excellent enterprise architect who has an extensive
background in helping companies rewrite their legacy Java EE applications to Quarkus.

You will read a user's problem along with examples of how they have solved a problem in the past.
The past examples will be presented in format of a summary of the issue along with source code of 
that point in time along with the updated source code when the problem is fixed

You will then write Quarkus code to solve their current problem.
You will output the results in the form a diff which can be applied via 'git apply'.

Your job is to look at the 'Current Issue' and the 'Current Issue Original Source Code' 
and rewrite the 'Current Issue Original Source Code' so the 'Current Issue' is solved 
in a manner similar to how the diff for 'Example #1 Diff' was obtained.

Think through the changes you will make and explain each step of the process.
If you are unsure of what changes is needed please state you are unsure and ask 
for clarification to help you.

When you are done explaining the reasoning for each change, write the updated 
Quarkus source code in the form of a diff which can be applied via 'git apply' 
in Markdown format, e.g.:

```diff
....
```

### Input:

Example #1 Issue: {example1_issue}

Example #1 Diff:
{example1_diff}

Current Issue: 
{current_issue}

Current Issue Original Source Code: 
```java
{current_issue_original_code}
```
"""

# Example #1 Original Source Code:
# ```java
# {example1_original_code}
# ```

# Example #1 Solved Source Code:
# ```java
# {example1_solved_code}
# ```

example1_original_code = """import java.util.HashMap;
import java.util.Map;

public class OldStyleRouter {
    interface RequestHandler {
        void handle(String requestData);
    }

    private Map<String, RequestHandler> routes;

    public OldStyleRouter() {
        routes = new HashMap<>();
    }

    public void addRoute(String path, RequestHandler handler) {
        routes.put(path, handler);
    }

    public void handleRequest(String path, String requestData) {
        if (routes.containsKey(path)) {
            routes.get(path).handle(requestData);
        } else {
            System.out.println("No handler for path: " + path);
        }
    }

    public static void main(String[] args) {
        OldStyleRouter router = new OldStyleRouter();

        // Adding routes using anonymous classes
        router.addRoute("/home", new RequestHandler() {
            @Override
            public void handle(String data) {
                System.out.println("Home Page Requested: " + data);
            }
        });
        router.addRoute("/about", new RequestHandler() {
            @Override
            public void handle(String data) {
                System.out.println("About Page Requested: " + data);
            }
        });

        // Handling requests
        router.handleRequest("/home", "User data for home");
        router.handleRequest("/about", "User data for about");
    }
}
"""

example1_solved_code = """import java.util.HashMap;
import java.util.Map;
import java.util.function.Consumer;

public class ModernRouter {
    private Map<String, Consumer<String>> routes;

    public ModernRouter() {
        routes = new HashMap<>();
    }

    public void addRoute(String path, Consumer<String> handler) {
        routes.put(path, handler);
    }

    public void handleRequest(String path, String requestData) {
        if (routes.containsKey(path)) {
            routes.get(path).accept(requestData);
        } else {
            System.out.println("No handler for path: " + path);
        }
    }

    public static void main(String[] args) {
        ModernRouter router = new ModernRouter();

        // Adding routes with lambda expressions
        router.addRoute("/home", data -> System.out.println("Home Page Requested: " + data));
        router.addRoute("/about", data -> System.out.println("About Page Requested: " + data));

        // Handling requests
        router.handleRequest("/home", "User data for home");
        router.handleRequest("/about", "User data for about");
    }
}
"""

example1_diff = """diff --git a/a b/b
index e16cb82..df9b214 100644
--- a/a
+++ b/b
@@ -1,45 +1,32 @@
 import java.util.HashMap;
 import java.util.Map;
+import java.util.function.Consumer;
 
-public class OldStyleRouter {
-    interface RequestHandler {
-        void handle(String requestData);
-    }
-
-    private Map<String, RequestHandler> routes;
+public class ModernRouter {
+    private Map<String, Consumer<String>> routes;
 
-    public OldStyleRouter() {
+    public ModernRouter() {
         routes = new HashMap<>();
     }
 
-    public void addRoute(String path, RequestHandler handler) {
+    public void addRoute(String path, Consumer<String> handler) {
         routes.put(path, handler);
     }
 
     public void handleRequest(String path, String requestData) {
         if (routes.containsKey(path)) {
-            routes.get(path).handle(requestData);
+            routes.get(path).accept(requestData);
         } else {
             System.out.println("No handler for path: " + path);
         }
     }
 
     public static void main(String[] args) {
-        OldStyleRouter router = new OldStyleRouter();
+        ModernRouter router = new ModernRouter();
 
-        // Adding routes using anonymous classes
-        router.addRoute("/home", new RequestHandler() {
-            @Override
-            public void handle(String data) {
-                System.out.println("Home Page Requested: " + data);
-            }
-        });
-        router.addRoute("/about", new RequestHandler() {
-            @Override
-            public void handle(String data) {
-                System.out.println("About Page Requested: " + data);
-            }
-        });
+        // Adding routes with lambda expressions
+        router.addRoute("/home", data -> System.out.println("Home Page Requested: " + data));
+        router.addRoute("/about", data -> System.out.println("About Page Requested: " + data));
 
         // Handling requests
         router.handleRequest("/home", "User data for home");
"""

current_issue_original_code = """import java.util.Comparator;

public class OldStyleJavaExample {
    public static void main(String[] args) {
        // Using an anonymous class to implement a comparator
        Comparator<Integer> compareIntegers = new Comparator<Integer>() {
            @Override
            public int compare(Integer x, Integer y) {
                return x.compareTo(y);
            }
        };

        // Using the comparator
        int comparisonResult = compareIntegers.compare(5, 10);
        System.out.println("Result using anonymous class: " + comparisonResult);
    }
}
"""

template_args = {
    "example1_issue": "The usage of anonymous classes for routes is against our coding conventions. Please use modern Java functional syntax instead",
    # "example1_original_code": example1_original_code,
    # "example1_solved_code": example1_solved_code,
    "example1_diff": example1_diff,
    "current_issue": "The usage of anonymous classes for routes is against our coding conventions. Please use modern Java functional syntax instead",
    "current_issue_original_code": current_issue_original_code,
}

formatted_prompt = template.format(**template_args)

complex_prompt = """
You are an excellent enterprise architect who has an extensive background in
helping companies rewrite their legacy Java EE applications to Quarkus.

You will read a user's problem along with examples of how they have solved a
problem in the past. The past examples will be presented in format of a summary
of the issue along with source code of that point in time along with the updated
source code when the problem is fixed

You will then write Quarkus code to solve their current problem. You will output
the results in the form a diff which can be applied via 'git apply'.

Your job is to look at the 'Current Issue' and the 'Current Issue Original
Source Code' and rewrite the 'Current Issue Original Source Code' so the
'Current Issue' is solved. You will not have an example to go off of, so please
be as accurate as possible.

Think through the changes you will make and explain each step of the process. If
you are unsure of what changes is needed please state you are unsure and ask for
clarification to help you.

When you are done explaining the reasoning for each change, write the updated
Quarkus source code in the form of a diff which can be applied via 'git apply'
in Markdown format, e.g.:

```diff
....
```

Current Issue: 
{current_issue}

Current Issue Original Source Code: 
```java
{current_issue_original_code}
```
"""

complex_code = """
package org.jboss.as.quickstarts.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.annotation.Resource;
import javax.inject.Inject;
import javax.jms.Destination;
import javax.jms.JMSContext;
import javax.jms.JMSDestinationDefinition;
import javax.jms.JMSDestinationDefinitions;
import javax.jms.Queue;
import javax.jms.Topic;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Definition of the two JMS destinations used by the quickstart
 * (one queue and one topic).
 */
@JMSDestinationDefinitions(
    value = {
        @JMSDestinationDefinition(
            name = "java:/queue/HELLOWORLDMDBQueue",
            interfaceName = "javax.jms.Queue",
            destinationName = "HelloWorldMDBQueue"
        ),
        @JMSDestinationDefinition(
            name = "java:/topic/HELLOWORLDMDBTopic",
            interfaceName = "javax.jms.Topic",
            destinationName = "HelloWorldMDBTopic"
        )
    }
)

/**
 * <p>
 * A simple servlet 3 as client that sends several messages to a queue or a topic.
 * </p>
 *
 * <p>
 * The servlet is registered and mapped to /HelloWorldMDBServletClient using the {@linkplain WebServlet
 * @HttpServlet}.
 * </p>
 *
 * @author Serge Pagop (spagop@redhat.com)
 *
 */
@WebServlet("/HelloWorldMDBServletClient")
public class HelloWorldMDBServletClient extends HttpServlet {

    private static final long serialVersionUID = -8314035702649252239L;

    private static final int MSG_COUNT = 5;

    @Inject
    private JMSContext context;

    @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
    private Queue queue;

    @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
    private Topic topic;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();
        out.write("<h1>Quickstart: Example demonstrates the use of <strong>JMS 2.0</strong> and <strong>EJB 3.2 Message-Driven Bean</strong> in JBoss EAP.</h1>");
        try {
            boolean useTopic = req.getParameterMap().keySet().contains("topic");
            final Destination destination = useTopic ? topic : queue;

            out.write("<p>Sending messages to <em>" + destination + "</em></p>");
            out.write("<h2>The following messages will be sent to the destination:</h2>");
            for (int i = 0; i < MSG_COUNT; i++) {
                String text = "This is message " + (i + 1);
                context.createProducer().send(destination, text);
                out.write("Message (" + i + "): " + text + "</br>");
            }
            out.write("<p><i>Go to your JBoss EAP server console or server log to see the result of messages processing.</i></p>");
        } finally {
            if (out != null) {
                out.close();
            }
        }
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
"""

formatted_complex_prompt = complex_prompt.format(
    **{
        "current_issue": "MDBs work completely differently in Quarkus. Do not use JMS, use Quarkus reactive messaging. Use JakartaEE 9 instead of javax libraries.",
        "current_issue_original_code": complex_code,
    }
)

llm = ChatOpenAI(streaming=True)

for chunk in llm.stream(formatted_complex_prompt):
    print(chunk.content, end="", flush=True)
