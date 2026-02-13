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

    @Scheduled(fixedDelay = 300000) // 5 minutes base delay
    public void checkStock() {
        // Random delay between 0 and 5 minutes (300000 ms) to mimic human behavior
        // (5-10 min interval total)
        try {
            long randomDelay = (long) (Math.random() * 300000);
            Thread.sleep(randomDelay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        List<TrackingItem> activeItems = trackingItemRepository.findByIsActiveTrue();

        for (TrackingItem item : activeItems) {
            boolean inStock = scraperService.checkStock(item.getProductUrl(), item.getTargetSize());

            if (inStock) {
                // Only send if we haven't reached the limit of 3
                if (item.getNotificationCount() < 3) {
                    notificationService.sendStockAlert(item);
                    item.setNotificationCount(item.getNotificationCount() + 1);
                }
                item.setLastStatus(StockStatus.IN_STOCK);
            } else {
                item.setLastStatus(StockStatus.OUT_OF_STOCK);
                // Reset counter ONLY if it was previously in stock?
                // Or always reset when out of stock so next time it comes back we notify again.
                item.setNotificationCount(0);
            }
            trackingItemRepository.save(item);
        }
    }
}
