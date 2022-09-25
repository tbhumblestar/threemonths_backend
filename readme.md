# Project : Threemonths

### 개요
- 실제 베이커리인 뜨리먼뜨(Threemonths)의 웹 사이트 구현
- 사이트 : http://threemonths.net/

<br/>

### 프로젝트 멤버 및 역할
- 멤버 : 김영빈(Back) & 이현정(Front) &  장형원(Front)
- 맡은 역할 : Backend 전담

<br/>

### 사용한 기술스택(Backend)
- Python
- Django / Django Rest Framework
- MYSQL
- Github
- Nginx(reverse-proxy)
- Gunicorn
- Docker(docker-compose)
- AWS(EC2, RDS, S3)


<br/>

## API
---
- Announcement, Order, Product, Image, User, Announcement 관련 API 구현
- Swagger 사이트 : https://threemonths.shop/api/schema/swagger-ui/#/

<br/>
<br/>

## 구현기능
---

### Django/DRF
- AbstactBaseUser기반의 커스텀 유저모델
- 카카오톡 소셜로그인
- SIMPLE-JWT와 DRF Permission기능을 활용한 인증, 인가
- DRF의 genericview기반의 api구현
- to_representation 등을 활용한 serializer customizing
- select_related, prefetch_related, prefetch 등을 활용한 ORM 최적화
- API testcode 구현

<br/>

### 배포
- AWS의 EC2, RDS, S3 및 gunicorn을 사용
- Docker-compose를 활용한 Nginx Reverse Proxy 서버 구축 및 이를 활용한 HTTPS 기능 구현
    + docker github : https://github.com/tbhumblestar/threemonths_backend_docker)

<br/>

### 기타
- drf-spectacular를 활용한 API문서화(https://threemonths.shop/api/schema/swagger-ui/#/)
- Crontab을 사용한 HTTPS 인증서 자동갱신