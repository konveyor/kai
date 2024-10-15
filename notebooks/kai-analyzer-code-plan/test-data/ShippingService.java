
package com.redhat.coolstore.service;

import java.math.BigDecimal;
import java.math.RoundingMode;

import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.core.MediaType;

import com.redhat.coolstore.model.ShoppingCart;

@Path("/shipping")
public class ShippingService {

    @POST
    @Path("/calculate")
    @Consumes(MediaType.APPLICATION_JSON)
    public double calculateShipping(ShoppingCart sc) {

        if (sc != null) {

            if (sc.getCartItemTotal() >= 0 && sc.getCartItemTotal() < 25) {

                return 2.99;

            } else if (sc.getCartItemTotal() >= 25 && sc.getCartItemTotal() < 50) {

                return 4.99;

            } else if (sc.getCartItemTotal() >= 50 && sc.getCartItemTotal() < 75) {

                return 6.99;

            } else if (sc.getCartItemTotal() >= 75 && sc.getCartItemTotal() < 100) {

                return 8.99;

            } else if (sc.getCartItemTotal() >= 100 && sc.getCartItemTotal() < 10000) {

                return 10.99;

            }

        }

        return 0;

    }

    @POST
    @Path("/insurance")
    @Consumes(MediaType.APPLICATION_JSON)
    public double calculateShippingInsurance(ShoppingCart sc) {

        if (sc != null) {

            if (sc.getCartItemTotal() >= 25 && sc.getCartItemTotal() < 100) {

                return getPercentOfTotal(sc.getCartItemTotal(), 0.02);

            } else if (sc.getCartItemTotal() >= 100 && sc.getCartItemTotal() < 500) {

                return getPercentOfTotal(sc.getCartItemTotal(), 0.015);

            } else if (sc.getCartItemTotal() >= 500 && sc.getCartItemTotal() < 10000) {

                return getPercentOfTotal(sc.getCartItemTotal(), 0.01);

            }

        }

        return 0;
    }

    private static double getPercentOfTotal(double value, double percentOfTotal) {
        return BigDecimal.valueOf(value * percentOfTotal)
                .setScale(2, RoundingMode.HALF_UP)
                .doubleValue();
    }

}
