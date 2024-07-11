from concurrent import futures
import grpc
import user_service_pb2
import user_service_pb2_grpc
from models import db, User
from sqlalchemy.exc import SQLAlchemyError

class UserService(user_service_pb2_grpc.UserServiceServicer):
    def AddUser(self, request, context):
        try:
            new_user = User(name=request.name, email=request.email, age=request.age)
            db.session.add(new_user)
            db.session.commit()
            return user_service_pb2.UserResponse(
                id=new_user.id, name=new_user.name, email=new_user.email, age=new_user.age)
        except SQLAlchemyError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_service_pb2.UserResponse()

    def GetUser(self, request, context):
        user = User.query.get(request.id)
        if user:
            return user_service_pb2.UserResponse(
                id=user.id, name=user.name, email=user.email, age=user.age)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_service_pb2.UserResponse()

    def UpdateUser(self, request, context):
        user = User.query.get(request.id)
        if user:
            user.name = request.name
            user.email = request.email
            user.age = request.age
            db.session.commit()
            return user_service_pb2.UserResponse(
                id=user.id, name=user.name, email=user.email, age=user.age)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_service_pb2.UserResponse()
