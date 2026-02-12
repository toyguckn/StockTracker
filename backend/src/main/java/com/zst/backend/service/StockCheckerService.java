package com.zst.backend.service;

import com.zst.backend.model.TrackingItem;
import com.zst.backend.model.StockStatus;
import com.zst.backend.repository.TrackingItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class StockCheckerService {

    @Autowired
    private TrackingItemRepository trackingItemRepository;

    @Autowired
    private ScraperService scraperService;

    @Autowired
    private NotificationService notificationService;

    @Scheduled(fixedRate = 600000) // 10 minutes
    public void checkStock() {
        List<TrackingItem> activeItems = trackingItemRepository.findByIsActiveTrue();

        for (TrackingItem item : activeItems) {
            boolean inStock = scraperService.checkStock(item.getProductUrl(), item.getTargetSize());

            if (inStock) {
                if (item.getLastStatus() == StockStatus.OUT_OF_STOCK) {
                    // Send notification
                    notificationService.sendStockAlert(item);
                }
                item.setLastStatus(StockStatus.IN_STOCK);
            } else {
                item.setLastStatus(StockStatus.OUT_OF_STOCK);
            }
            trackingItemRepository.save(item);
        }
    }
}
