class User:
    def __init__(self, userid, userpwd, userfname, userlname, useremail):
        self.userId = userid
        self.userPwd = userpwd
        self.userFName = userfname
        self.userLName = userlname
        self.userEmail = useremail
        self.userName = userfname+userlname

    def getId(self):
        return self.userId

    def setId(self, id):
        self.userId = id

    def getPwd(self):
        return self.userPwd

    def setPwd(self, pwd):
        self.userPwd = pwd

    def getFName(self):
        return self.userFName

    def setFName(self, fname):
        self.userFName = fname

    def getLName(self):
        return self.userFName

    def setLName(self, lname):
        self.userLName = lname

    def getEmail(self):
        return self.userEmail

    def setEmail(self, email):
        self.userEmail = email

    def getName(self):
        return self.userName

    # @property
    # def userId(self):
    #     return self._userId
    #
    # @userId.setter
    # def userId(self, userId):
    #     self._userId = userId
    #
    # @property
    # def userPwd(self):
    #     return self._userPwd
    #
    # @userPwd.setter
    # def userPwd(self, userPwd):
    #     self._userPwd = userPwd
    #
    # @property
    # def userFName(self):
    #     return self._userFName
    #
    # @userFName.setter
    # def userFName(self, userFName):
    #     self._FName = userFName
    #
    # @property
    # def userLName(self):
    #     return self._userLName
    #
    # @userLName.setter
    # def userLName(self, userLName):
    #     self._LName = userLName
    #
    # @property
    # def userEmail(self):
    #     return self._userEmail
    #
    # @userEmail.setter
    # def userEmail(self, userEmail):
    #     self._userEmail = userEmail
