# Threemonths
- 뜨리먼뜨(Threemonths)의 홈페이지 사이트
- 사이트 : http://threemonths.net/

## 기술스택
- Python
- Django / Django Rest Framework
- MYSQL
- Github
- Nginx(reverse-proxy)
- Docker

## 구현 기능
- DRF의 genericview기반의 로직 구현
- select_related, prefetch_related, prefetch 등을 활용한 ORM 최적화
- API testcode 구현
- drf-spectacular를 활용한 API문서화(http://15.164.163.31:8001/api/schema/swagger-ui/)
- Docker 기반의 Nginx Reverse Proxy 서버 구축 및 이를 활용한 HTTPS 기능 구현


## API
- Announcement, Order, Products, Images, Users 관련 API 구현
- Swagger 사이트 : http://15.164.163.31:8001/api/schema/swagger-ui/
