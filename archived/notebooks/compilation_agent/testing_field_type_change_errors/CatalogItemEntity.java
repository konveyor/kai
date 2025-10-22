package com.redhat.coolstore.model;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name = "PRODUCT_CATALOG", uniqueConstraints = @UniqueConstraint(columnNames = "itemId"))
public class CatalogItemEntity implements Serializable {

	private static final long serialVersionUID = -7304814269819778382L;

	@Id
	private String itemId;

    @Column(length = 80)
    private String name;

	@Column(name="description",columnDefinition = "text")
	private String desc;

    @Column
	private double price;

	@OneToOne(cascade = CascadeType.ALL,fetch=FetchType.EAGER)
    @PrimaryKeyJoinColumn
	private InventoryEntity inventory;

	public CatalogItemEntity() {
	}

	public String getItemId() {
		return itemId;
	}

	public void setItemId(String itemId) {
		this.itemId = itemId;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDesc() {
		return desc;
	}

	public void setDesc(String desc) {
		this.desc = desc;
	}

	public double getPrice() {
		return price;
	}

	public void setPrice(double price) {
		this.price = price;
	}

    public InventoryEntity getInventory() {
        return inventory;
    }

    public String getInventoryId() {
        return inventory.itemId;
    }

    public void setInventory(InventoryEntity inventory) {
        this.inventory = inventory;
    }

    @Override
	public String toString() {
		return "ProductImpl [itemId=" + itemId + ", name=" + name + ", desc="
				+ desc + ", price=" + price + "]";
    }

}
