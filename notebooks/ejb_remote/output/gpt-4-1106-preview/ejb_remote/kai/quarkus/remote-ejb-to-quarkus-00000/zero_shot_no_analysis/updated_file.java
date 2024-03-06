
package org.jboss.as.quickstarts.ejb.remote.stateful;

import javax.enterprise.context.ApplicationScoped;

/**
 * A simple counter bean that can increment and decrement a count.
 * This is a Quarkus version of the previous Java EE stateful bean.
 */
@ApplicationScoped
public class CounterBean {

    private int count = 0;

    public void increment() {
        this.count++;
    }

    public void decrement() {
        this.count--;
    }

    public int getCount() {
        return this.count;
    }
}
