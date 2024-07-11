from __init__ import create_app
import grpc
from concurrent import futures
import user_service_pb2_grpc
from services import UserService

app = create_app()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    import threading
    threading.Thread(target=serve).start()
    app.run(debug=True)
