package com.example.demo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util. List;

@Repository
public interface MovieRepository extends JpaRepository<Movie, String> {
    @Query(value="select * from movie_tbl m where m.title=:title limit 1",nativeQuery=true)
    public Movie findTitle(@Param(value="title") String title);

    @Query(value= "select * from movie_tbl m order by num limit 5", nativeQuery=true) 
    public List <Movie> findBoxOffice();
}
