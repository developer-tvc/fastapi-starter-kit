class UserDeviceEntity:
    def __init__(self, user_id: int, device_id: str, device_name: str, user_agent: str, ip_address: str):
        self.user_id = user_id
        self.device_id = device_id
        self.device_name = device_name
        self.user_agent = user_agent
        self.ip_address = ip_address