package com.zst.backend.controller;

import com.zst.backend.dto.ProductRequest;
import com.zst.backend.dto.TrackingRequest;
import com.zst.backend.service.ProductService;
import com.zst.backend.service.ScraperService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*") // Allow all for now
public class ProductController {

    @Autowired
    private ScraperService scraperService;

    @Autowired
    private ProductService productService;

    @PostMapping("/products/check-sizes")
    public ResponseEntity<List<String>> checkSizes(@RequestBody ProductRequest request) {
        List<String> sizes = scraperService.fetchAvailableSizes(request.getUrl());
        return ResponseEntity.ok(sizes);
    }

    @PostMapping("/tracking")
    public ResponseEntity<String> createTracking(@RequestBody TrackingRequest request) {
        productService.createTracking(request);
        return ResponseEntity.ok("Tracking created successfully");
    }
}
