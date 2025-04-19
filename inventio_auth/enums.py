from enum import Enum


class RoleEnum(Enum):
    WORKER = 'worker'
    TECHNICIAN = 'technician'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]