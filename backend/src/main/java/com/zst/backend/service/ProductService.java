package com.zst.backend.service;

import com.zst.backend.dto.TrackingRequest;
import com.zst.backend.model.TrackingItem;
import com.zst.backend.model.User;
import com.zst.backend.model.StockStatus;
import com.zst.backend.repository.TrackingItemRepository;
import com.zst.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class ProductService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TrackingItemRepository trackingItemRepository;

    @Autowired
    private ScraperService scraperService;

    public void createTracking(TrackingRequest request) {
        User user = null;
        
        // Find or create user
        if (request.getEmail() != null && !request.getEmail().isEmpty()) {
            user = userRepository.findByEmail(request.getEmail()).orElse(null);
        }
        
        if (user == null && request.getTelegramChatId() != null && !request.getTelegramChatId().isEmpty()) {
            user = userRepository.findByTelegramChatId(request.getTelegramChatId()).orElse(null);
        }
        
        if (user == null) {
            user = new User();
            user.setEmail(request.getEmail());
            user.setTelegramChatId(request.getTelegramChatId());
            user.setNotificationPreference(request.getPreference());
            user = userRepository.save(user);
        } else {
            // Update user info if needed
            if (request.getTelegramChatId() != null && !request.getTelegramChatId().isEmpty()) {
                user.setTelegramChatId(request.getTelegramChatId());
            }
            if (request.getPreference() != null) {
                user.setNotificationPreference(request.getPreference());
            }
            userRepository.save(user);
        }

        TrackingItem item = new TrackingItem();
        item.setUser(user);
        item.setProductUrl(request.getUrl());
        item.setTargetSize(request.getSize());
        item.setLastStatus(StockStatus.OUT_OF_STOCK);
        item.setActive(true);
        item.setProductName("Zara Product"); // Ideally fetch from scraper

        trackingItemRepository.save(item);
    }
}
