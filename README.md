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

#Consumers   消费者
What is a consumer?  什么是消费者？
A consumer typically refers to an entity that consumes or uses the APIs managed by Kong Gateway. Consumers can be applications, services, or users who interact with your APIs. Since they are not always human, Kong Gateway calls them consumers, because they “consume” the service. Kong Gateway allows you to define and manage consumers, apply access control policies, and monitor their API usage.
消费者通常是指使用或使用由 Kong Gateway 管理的 API 的实体。消费者可以是与您的 API 交互的应用程序、服务或用户。由于他们并不总是人类，因此 Kong Gateway 称他们为消费者，因为他们“消费”服务。Kong Gateway 允许您定义和管理消费者、应用访问控制策略以及监控他们的 API 使用情况。

Consumers are essential for controlling access to your APIs, tracking usage, and ensuring security. They are identified by key authentication, OAuth, or other authentication and authorization mechanisms. For example, adding a Basic Auth plugin to a service or route allows it to identify a consumer, or block access if credentials are invalid.
使用者对于控制对 API 的访问、跟踪使用情况和确保安全性至关重要。它们通过密钥身份验证、OAuth 或其他身份验证和授权机制进行标识。例如，将 Basic Auth 插件添加到服务或路由中，可以使其识别使用者，或在凭据无效时阻止访问。

You can choose to use Kong Gateway as the primary datastore for consumers, or you can map the consumer list to an existing database to keep consistency between Kong Gateway and your existing primary datastore.
您可以选择使用 Kong Gateway 作为使用者的主数据存储，也可以将使用者列表映射到现有数据库，以保持 Kong Gateway 与现有主数据存储之间的一致性。

By attaching a plugin directly to a consumer, you can manage specific controls at the consumer level, such as rate limits.
通过将插件直接附加到使用者，您可以在使用者级别管理特定控制，例如速率限制。

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

