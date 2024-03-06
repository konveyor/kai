
package org.jboss.as.quickstarts.greeter;

import java.util.logging.Logger;

import jakarta.enterprise.inject.spi.InjectionPoint;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;

public class Resources {

    // Inject an entity manager provided by Quarkus
    @Inject
    private EntityManager em;

    public EntityManager getEm() {
        return em;
    }

    public Logger getLogger(InjectionPoint ip) {
        String category = ip.getMember().getDeclaringClass().getName();
        return Logger.getLogger(category);
    }

    public FacesContext getFacesContext() {
        return FacesContext.getCurrentInstance();
    }

}
