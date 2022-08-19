from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self,request,view):
        
        is_staff = bool(request.user and request.user.is_staff)
        return request.method == 'GET' or is_staff
    

class IsAdminOrIsWriterOrForbidden(permissions.BasePermission):
    
    #인증(유저Login 돼있는지 확인)
    def has_permission(self,request,view):
        
        is_authenticated = bool(request.user and request.user.is_authenticated)
        
        return is_authenticated and request.method != 'PUT'
    
    #
    def has_object_permission(self,request,view,obj):
        
        is_staff = bool(request.user.is_staff)
        is_writer = bool(request.user == obj.user)

        return is_staff or is_writer



class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        return request.method == 'GET' or is_authenticated    


class OrderDetailPermission(permissions.BasePermission):
    
    """
    Put메서드 요청은 기본적으로 불가능
    
    관리자(is_staff=True)
        - 무엇이든 가능
    
    Order 작성자유저(request.user == obj.user)
        - Order.status가 not_confirmed이면 업데이트 및 삭제 가능
        - Order.status가 not_confirmed가 아니면 조회만 가능
        
    그외(비회원, 작성자가 아닌 유저)
        - 조회(Get), 수정, 삭제 모두 다 불가능
    """
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.method != 'PUT')
    
    def has_object_permission(self,request,view,obj):
        
        if request.user.is_staff:
            return True
        
        elif request.user == obj.user:
            return request.method == 'GET' or obj.status == "not_confirmed"
        
        else:
            return False