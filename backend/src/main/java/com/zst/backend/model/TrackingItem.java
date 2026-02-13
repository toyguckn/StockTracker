package com.zst.backend.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Table(name = "tracking_items")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class TrackingItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(nullable = false)
    private String productUrl;

    private String productName;

    @Column(nullable = false)
    private String targetSize;

    @Enumerated(EnumType.STRING)
    private StockStatus lastStatus = StockStatus.OUT_OF_STOCK;

    private boolean isActive = true;

    private int notificationCount = 0;
}
