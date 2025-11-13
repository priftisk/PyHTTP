class Headers:
    def __init__(self, headers_arr):
        self.__host = None
        self.__user_agent = None
        self.__accept = None
        self.__accept_lang = None
        self.__encoding = None
        self.__connection = None
        self.__referer = None
        self.parse(headers_arr)
        
    
    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def user_agent(self):
        return self.__user_agent

    @user_agent.setter
    def user_agent(self, value):
        self.__user_agent = value

    @property
    def accept(self):
        return self.__accept

    @accept.setter
    def accept(self, value):
        self.__accept = value

    @property
    def accept_lang(self):
        return self.__accept_lang

    @accept_lang.setter
    def accept_lang(self, value):
        self.__accept_lang = value

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        self.__encoding = value

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, value):
        self.__connection = value

    @property
    def referer(self):
        return self.__referer

    @referer.setter
    def referer(self, value):
        self.__referer = value
        
    def parse(self, headers_arr):
        for h in headers_arr:
            h_name = h[0].strip()
            h_value = h[1].strip()
            match h_name:
                case "Host":
                    self.host=h_value
                case "User-Agent":
                    self.user_agent=h_value
                case "Accept":
                    self.accept = h_value
                case "Accept-Language":
                    self.accept_lang = h_value
                case "Encoding":
                    self.encoding = h_value
                case "Connection":
                    self.connection = h_value
                case "Referer":
                    self.referer = h_value
                