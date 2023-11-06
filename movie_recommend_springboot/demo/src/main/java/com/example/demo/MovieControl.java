package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.json.JSONArray;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import java.util.*;
import org.apache.hc.client5.http.classic.methods.*;
import org.apache.hc.client5.http.entity.*;
import org.apache.hc.client5.http.impl.classic.*;
import org.apache.hc.core5.http.io.entity.*;
import org.apache.hc.core5.http.message.*;
import java.nio.charset.Charset;


@Controller
public class MovieControl {
    @Autowired
    private MovieRepository repository;

    @RequestMapping(value="/box_office")
    @ResponseBody
    public String boxOffice() throws Exception{
        List<Movie> boxOfficeList = repository.findBoxOffice();
        List<Map> allMovie = new ArrayList<Map>();

        for (int i=0; i<boxOfficeList.size(); i++){
            Map oneMovie = new HashMap();
            Movie movie = boxOfficeList.get(i);
            oneMovie.put("movie", movie);
            
            ArrayList <Movie> recommendMovieList = new ArrayList<Movie>();
            String movieTitle = movie.getTitle();
            System.out.println("movieTitle="+movieTitle);

            HttpPost httpPost = new HttpPost("http://3.34.47.211:5000/movie_recommend");

            List<BasicNameValuePair> nvps = new ArrayList<>();
            nvps.add(new BasicNameValuePair("title", movieTitle));

            httpPost.setEntity(
                new UrlEncodedFormEntity(nvps, Charset.forName("UtF-8")));
                //Flask 에 접속해서 실행 결과클 가져을 객체 생성
                CloseableHttpClient httpclient = HttpClients. createDefault();
                //Flask에 접속해서 실행 결과를 가져옴
                CloseableHttpResponse response2 = httpclient.execute(httpPost);
                //Flask 실행 결과를 가저음
                String flaskResult =
                        EntityUtils.toString(response2.getEntity(),
                            Charset. forName("UTF-8"));
                System.out.println("flaskResult=" + flaskResult);
                
                httpclient.close();

            try{
                JSONArray jsonArray = new JSONArray (flaskResult);

                for (int j = 0; j < jsonArray. length(); j++) {
                    String recommendTitle = jsonArray.getString(j);
                
                    // JSONArray recommend = jsonArray.getJSONArray(j);
                
                    // String recommendTitle = recommend.getString (0) ;
                    
                    Movie recommendMovie = repository.findTitle(recommendTitle);
            
                    recommendMovieList.add(recommendMovie);
                }
                oneMovie.put("recommend", recommendMovieList);
                allMovie.add(oneMovie);
            }catch(Exception e){
                System.out.println("e="+e);
            }
        }
        return new JSONArray(allMovie).toString();
    }
}