
# OAuth2.0
OAuth2.0客户端的关键配置，需要从Kong Gateway管理端获取和设置：

1. client-id : 这是在Kong Gateway中注册OAuth2.0应用时获得的客户端ID。需要通过Kong Admin API创建，例如：
执行后，Kong会返回一个 client_id ，将其填入配置文件。

2. client-secret : 同样在创建OAuth2.0应用时由Kong生成的密钥，与client-id一起返回。
3. authorization-grant-type : 这里使用 authorization_code 是最常见的OAuth2.0授权方式，通常不需要修改。
修改后的配置应该类似这样：

获取步骤：

1. 首先在Kong中创建一个Consumer：
2. 为该Consumer创建OAuth2.0凭证：
```bash
curl.exe -X POST http://localhost:8001/consumers/kong-integration-api/oauth2 --data "name=kong-integration-api" --data "redirect_uris=http://localhost:8080/login/oauth2/code/kong"

```

3. Kong会返回类似这样的响应：
```json
{
	"created_at": 1741674847,
	"client_secret": "YTQhYPj9iyeJSKGLD3Nb2LAea9eL9rHx",
	"redirect_uris": [
		"http://localhost:8080/login/oauth2/code/kong"
	],
	"consumer": {
		"id": "74beba5c-8773-430d-a946-0ab770233192"
	},
	"name": "kong-integration-api",
	"hash_secret": false,
	"client_type": "confidential",
	"id": "7a83e132-25e0-49cf-8ca4-810a3fa400ee",
	"tags": null,
	"client_id": "IZRxqm5D3qXmVjhXwrCXtfS8xWbLLeMM"
}
 ```
```

4. 将返回的client_id和client_secret复制到application.yml中对应的位置。
注意：

- 请妥善保管client_secret，不要泄露
- redirect_uri必须与application.yml中配置的一致
- 建议在生产环境中使用环境变量或配置中心来管理这些敏感信息，而不是直接写在配置文件中


# Kong Gateway 启动步骤（Docker）

### 1. 创建 Docker 网络
```bash
docker network create kong-net
```

### 2. 启动 PostgreSQL 数据库（Kong 需要）
```bash
docker run -d --name kong-database   --network=kong-net   -e "POSTGRES_USER=kong"   -e "POSTGRES_DB=kong"   -e "POSTGRES_PASSWORD=kongpass"   postgres:13
```

### 3. 初始化 Kong 数据库

```bash
docker run --rm --network=kong-net  -e "KONG_DATABASE=postgres"  -e "KONG_PG_HOST=kong-database"  -e "KONG_PG_USER=kong"  -e "KONG_PG_PASSWORD=kongpass"  kong:latest kong migrations bootstrap
```

4. 启动 Kong Gateway
```bash
docker run -d --name kong --network=kong-net -e "KONG_DATABASE=postgres" -e "KONG_PG_HOST=kong-database" -e "KONG_PG_USER=kong" -e "KONG_PG_PASSWORD=kongpass" -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" -e "KONG_PROXY_ERROR_LOG=/dev/stderr" -e "KONG_ADMIN_ERROR_LOG=/dev/stderr"  -e "KONG_ADMIN_LISTEN=0.0.0.0:8001"  -e "KONG_ADMIN_GUI_URL=http://localhost:8002"  -p 8000:8000  -p 8443:8443  -p 8001:8001  -p 8444:8444  -p 8002:8002  -p 8445:8445   kong:latest
```  
5. 验证 Kong 是否启动成功
```
curl http://localhost:8001/status
```

### 端口说明：
8000：Kong 监听 HTTP 请求的代理端口
8443：Kong 监听 HTTPS 请求的代理端口
8001：Kong Admin API 端口
8444：Kong Admin API HTTPS 端口
8002：Kong Manager (GUI) 端口
8445：Kong Manager (GUI) HTTPS 端口

注意事项：1. 确保您的机器已经安装了 Docker2. 端口 8000-8445 没有被其他程序占用3. 需要至少 4GB 的可用内存4. Kong Gateway 启动后，可以通过访问 http://localhost:8002 进入 Kong Manager 界面5. 所有的 Kong Admin API 操作都可以通过 http://localhost:8001 进行访问


# 测试
## 注册API到Kong
### 1. 创建Service（指向你的Spring Boot应用）

```bash
curl.exe -i -X POST http://localhost:8001/services --data name=books-service --data url='http://127.0.0.1:8080'
```
### 2.创建Route
```bash
curl.exe -i -X POST http://localhost:8001/services/books-service/routes --data 'paths[]=/api/v1/books' --data name=books-route
```

此时通过Kong访问API：
```bash
curl.exe http://localhost:8000/api/v1/books
```

# 生成JWT凭证
Windows PowerShell:
```powershell
$body = @{
    key = "kong-integration-api-jwt"
    algorithm = "HS256"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8001/consumers/kong-integration-api/jwt" -Body $body -ContentType "application/json"
```
response
```
created_at     : 1741676781
rsa_public_key :
algorithm      : HS256
id             : 38565556-8f38-46a1-944c-326d12df0fa9
consumer       : @{id=74beba5c-8773-430d-a946-0ab770233192}
key            : kong-integration-api-jwt
secret         : Vjv87HcUIwMgirpYPy9cTGt482s8Oy8q
tags           :
```
  
  