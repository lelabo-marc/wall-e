import time
from lib import vrep


class BaseClient(object):

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, client_id):
        self.__id = client_id

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = int(mode)

    def __init__(self, address, port):
        vrep.simxFinish(-1)
        self.address = address
        self.port = port
        self.__id = -1
        self.__mode = -1

    def connect(self):
        self.id = vrep.simxStart(self.address, self.port, True, True, 5000, 5)
        self.mode = vrep.simx_opmode_oneshot_wait

    def is_connected(self):
        return self.id != -1

    def disconnect(self):
        vrep.simxFinish(self.id)
        self.id = -1
        self.mode = -1

    def reconnect(self):
        self.disconnect()
        time.sleep(1)
        self.connect()


class RobotClient(BaseClient):

    def __init__(self, address='127.0.0.1', port=19997):
        BaseClient.__init__(self, address, port)

    def get_object(self, name):
        return vrep.simxGetObjectHandle(self.id, name, self.mode)

    def set_motor_position(self, handle, value):
        vrep.simxSetJointTargetPosition(self.id, handle, value, self.mode)

    def get_motor_position(self, handle):
        return vrep.simxGetJointPosition(self.id, handle, self.mode)

    def get_object_position(self, handle, buffer=True):
        if buffer:
            return vrep.simxGetObjectPosition(self.id, handle, -1, vrep.simx_opmode_buffer)
        return vrep.simxGetObjectPosition(self.id, handle, -1, vrep.simx_opmode_streaming)

    def get_object_orientation(self, handle, buffer=True):
        if buffer:
            return vrep.simxGetObjectOrientation(self.id, handle, -1, vrep.simx_opmode_buffer)
        return vrep.simxGetObjectOrientation(self.id, handle, -1, vrep.simx_opmode_streaming)
