package com.example.kongintegrationapi.controller;


import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/hello")
public class HelloController {

    @GetMapping("/world")
    public ResponseEntity helloWorld(@RequestParam String code) {
        System.out.println("Get response with code:"+code);
        return ResponseEntity.ok("Get response with code:"+code);
    }

}
