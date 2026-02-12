package com.zst.backend.repository;

import com.zst.backend.model.TrackingItem;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface TrackingItemRepository extends JpaRepository<TrackingItem, Long> {
    List<TrackingItem> findByIsActiveTrue();
    List<TrackingItem> findByUserEmail(String email);
}
