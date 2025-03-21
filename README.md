# run kong gateway

```bash
# 创建网络
docker network create kong-net

# 启动PostgreSQL
docker run -d --name kong-db  --network=kong-net  -p 5432:5432  -e POSTGRES_DB=kong  -e POSTGRES_USER=kong  -e POSTGRES_PASSWORD=kong -v /c/WorkSpace/docker/kong/postgres:/var/lib/postgresql/data postgres:13

# 初始化数据库
docker run --rm  --network=kong-net  -e "KONG_DATABASE=postgres"  -e "KONG_PG_HOST=kong-db"  -e "KONG_PG_USER=kong"  -e "KONG_PG_PASSWORD=kong"  kong:3.4.1 kong migrations bootstrap

# 启动Kong
docker run -d --name kong  --network=kong-net  -e "KONG_DATABASE=postgres"  -e "KONG_PG_HOST=kong-db"  -e "KONG_PG_USER=kong"  -e "KONG_PG_PASSWORD=kong"  -e "KONG_PROXY_ACCESS_LOG=/dev/stdout"  -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout"  -e "KONG_PROXY_ERROR_LOG=/dev/stderr"  -e "KONG_ADMIN_ERROR_LOG=/dev/stderr"  -e "KONG_ADMIN_LISTEN=0.0.0.0:8001"  -p 8000:8000  -p 8443:8443  -p 8001:8001  -p 8444:8444  kong:3.4.1
```

# enable jwt plugin
1. gateway service -> enable jwt plugin
2. add consumers -> for example: BookKey/BookSecret
3. generate token > https://jwt.io/ https://www.epochconverter.com/
![img3.png](images%2Fimg3.png)



# issues
## An invalid response was received from the upstream server
本地非容器内运行服务：http://127.0.0.1:8080/api/v1/books
请求kong代理的服务 http://127.0.0.1:8000/api/v1/books 报错如下：

```
2025-03-12 15:33:34 172.18.0.1 - - [12/Mar/2025:07:33:34 +0000] "GET /api/v1/books HTTP/1.1" 502 126 "-" "-" kong_request_id: "712716108691652b90a4ab6f282a2835"
2025-03-12 15:33:08 2025/03/12 07:33:08 [error] 1411#0: *20594 connect() failed (111: Connection refused) while connecting to upstream, client: 172.18.0.1, server: kong, request: "GET /api/v1/books HTTP/1.1", upstream: "http://127.0.0.1:8080/api/v1/books", host: "localhost:8000", request_id: "5ffcd27fdbe1e60f39bbcb13efbf0468"
2025-03-12 15:33:08 2025/03/12 07:33:08 [error] 1411#0: *20594 connect() failed (111: Connection refused) while connecting to upstream, client: 172.18.0.1, server: kong, request: "GET /api/v1/books HTTP/1.1", upstream: "http://127.0.0.1:8080/api/v1/books", host: "localhost:8000", request_id: "5ffcd27fdbe1e60f39bbcb13efbf0468"
2025-03-12 15:33:08 2025/03/12 07:33:08 [error] 1411#0: *20594 connect() failed (111: Connection refused) while connecting to upstream, client: 172.18.0.1, server: kong, request: "GET /api/v1/books HTTP/1.1", upstream: "http://127.0.0.1:8080/api/v1/books", host: "localhost:8000", request_id: "5ffcd27fdbe1e60f39bbcb13efbf0468"
```
fix:

kong的gateway配置host使用`host.docker.internal` 即可
![img_2.png](images%2Fimg_2.png)

