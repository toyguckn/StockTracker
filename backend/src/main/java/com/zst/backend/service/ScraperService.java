package com.zst.backend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import java.util.List;
import java.util.Map;
import java.util.Collections;

@Service
public class ScraperService {

    @Value("${scraper.url:http://localhost:8000}")
    private String scraperUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    public List<String> fetchAvailableSizes(String url) {
        try {
            Map<String, String> request = Collections.singletonMap("url", url);
            ResponseEntity<List> response = restTemplate.postForEntity(scraperUrl + "/scrape-sizes", request, List.class);
            return response.getBody();
        } catch (Exception e) {
            e.printStackTrace();
            return Collections.emptyList();
        }
    }

    public boolean checkStock(String url, String size) {
        try {
            Map<String, String> request = Map.of("url", url, "size", size);
            ResponseEntity<Map> response = restTemplate.postForEntity(scraperUrl + "/check-stock", request, Map.class);
            return (Boolean) response.getBody().get("in_stock");
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}
