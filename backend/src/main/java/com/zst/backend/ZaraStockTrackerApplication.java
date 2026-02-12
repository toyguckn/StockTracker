package com.zst.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ZaraStockTrackerApplication {

	public static void main(String[] args) {
		SpringApplication.run(ZaraStockTrackerApplication.class, args);
	}

}
