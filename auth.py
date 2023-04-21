import flask
import grpc
from concurrent import futures
import logging

import auth_pb2_grpc
import auth_pb2
import google.protobuf.wrappers_pb2 as wrappers

VALID_CREDITS = {
    "autotest": "123",
    "test_user": "4567"
}

def auth_user(login, password):
    if not login in VALID_CREDITS.keys():
        return False
    return VALID_CREDITS.get(login) == password

class AuthServicer(auth_pb2_grpc.AuthServiceServicer):
    def AuthUser(self, request, context):
        login = request.login
        password = request.password
        print(f"Trying to auth: {login} {password}")
        res = auth_user(login, password)
        print(f"Result: {res}")
        return wrappers.BoolValue(value=res)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    try:
        serve()
    except KeyboardInterrupt:
        print("Leaving")