# Project : Threemonths

### 프로젝트 개요
- 베이커리 뜨리먼뜨(Threemonths)의 홈페이지 사이트 구현
- 사이트 : http://threemonths.net/

### 프로젝트 멤버
- 김영빈(Back) 
- 이현정(Front)
- 장형원(Front)

### 기술스택
- Python
- Django / Django Rest Framework
- MYSQL
- Github
- Nginx(reverse-proxy)
- Docker(docker-compose)
- AWS(EC2, RDS, S3)

### 구현 기능
- AbstactBaseUser기반의 커스텀 유저모델
- 카카오톡 소셜로그인
- SIMPLE-JWT와 DRF Permission기능을 활용한 인증, 인가
- DRF의 genericview기반의 api구현
- to_representation 등을 활용한 serializer customizing
- select_related, prefetch_related, prefetch 등을 활용한 ORM 최적화
- API testcode 구현
- drf-spectacular를 활용한 API문서화(http://15.164.163.31:8001/api/schema/swagger-ui/)
- AWS의 EC2, RDS, S3를 사용
- Docker compose를 활용한 Nginx Reverse Proxy 서버 구축 및 이를 활용한 HTTPS 기능 구현


### API
- Announcement, Order, Products, Images, Users 리소스 관련 API 구현
- Swagger 사이트 : http://15.164.163.31:8001/api/schema/swagger-ui/
