package com.example.kongintegrationapi.repository;

import com.example.kongintegrationapi.model.Book;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BookRepository extends JpaRepository<Book, Long> {
}