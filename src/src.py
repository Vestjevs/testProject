from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from enum import Enum


class Credentials:
    def __init__(self):
        self.__username = ""
        self.__password = ""
        self.__domain = ""

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password

    def set__password(self, password):
        self.__password = password

    def get_domain(self):
        return self.__domain

    def set_domain(self, domain):
        self.__domain = domain


class Workload:
    def __init__(self):
        self.__ip = ""
        self.__storage = []  # contains list of instances of type MountPoint
        self.__credentials = Credentials()

    def get_ip(self):
        return self.__ip

    def set_ip(self, ip):
        self.__ip = ip

    def create_credentials(self, username, password, domain):
        self.__credentials.set_username(username)
        self.__credentials.set__password(password)
        self.__credentials.set_domain(domain)

    def get_credentials(self):
        return self.__credentials

    def add_to_storage(self, mount_point):
        self.__storage.append(mount_point)

    def remove_from_storage(self, mount_point):
        try:
            k = self.__storage.index(mount_point)
        except FileNotFoundError:
            k = -1

        if k != -1:
            self.__storage.remove(mount_point)


class MountPoint:
    def __init__(self, mount_point="", size=0):
        self.__mount_point = mount_point
        self.__total_size = size

    def get_mount_point(self):
        return self.__mount_point

    def set_mount_point(self, mount_point):
        self.__mount_point = mount_point

    def get_total_size(self):
        return self.__total_size

    def set_total_size(self, size):
        if size > 0:
            self.__total_size = size

    def __eq__(self, other):
        return self.__mount_point == other.__mount_point or self.__total_size == other.__total_size


class Source:
    def __init__(self, username, password, ip):
        self.__username = self.username_constraint(username)
        self.__password = self.password_constraint(password)
        self.__ip = self.ip_constraint(ip)

    @staticmethod
    def username_constraint(username):
        if username is None:
            raise ValueError
        else:
            return username

    @staticmethod
    def password_constraint(password):
        if password is None:
            raise ValueError
        else:
            return password

    @staticmethod
    def ip_constraint(ip):
        if ip is None:
            raise ValueError
        else:
            return ip


class State(Enum):
    NOT_STARTED = 1,
    RUNNING = 2,
    ERROR = 3,
    SUCCESS = 4


class MigrationTarget:
    def __init__(self, workload, uri="Uniform_resource_identifier"):
        self.__cloud = Client(uri=uri,
                              verify_ssl_certs=False,
                              log_file='pyvcloud.log',
                              log_requests=True,
                              log_headers=True,
                              log_bodies=True)
        self.__target_vm = workload
        cred = self.__target_vm.get_credentials()
        self.__credential = BasicLoginCredentials(cred.get_username(),
                                                  cred.get_domain(),
                                                  cred.get_password())
        self.__state = State.NOT_STARTED

    def get_workload(self):
        return self.__target_vm

    def get_state(self):
        return self.__state


class Migration:
    def __init__(self):
        self.__selected_mount_points = []
        self.__source = Workload()

    def create_workload(self, ip, storage, credential):
        self.__source.set_ip(ip)
        self.__source.create_credentials(credential.get_username(),
                                         credential.get_password(),
                                         credential.get_domain())
        for elem in storage:
            self.__selected_mount_points.append(elem)

    def add_selected_point(self, point):
        self.__selected_mount_points.append(point)

    def remove_unselected_point(self, point):
        try:
            k = self.__selected_mount_points.index(point)
        except FileNotFoundError:
            k = -1

        if k != -1:
            self.__selected_mount_points.remove(point)
