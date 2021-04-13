



        def check_params(self):
            for key,val in self.polyConfig['customParams'].items():
            a = key
            if a == "isy":
                self.isy = str(val)
            elif a == "user":
                self.user = str(val)
            elif a == "password":
                self.password = str(val)
            elif a == "parseDelay":
                self.parseDelay = float(val)
            elif a == "pullDelay":
                self.pullDelay = float(val)
            elif a.isdigit():
                if val == 'switch':
                    _name = str(val) + ' ' + str(key)
                    self.addNode(VirtualSwitch(self, self.address, key, _name))
                elif val == 'temperature':
                    _name = str(val) + ' ' + str(key)
                    self.addNode(VirtualTemp(self, self.address, key, _name))
                elif val == 'temperaturec' or val == 'temperaturecr':
                    _name = str(val) + ' ' + str(key)
                    self.addNode(VirtualTempC(self, self.address, key, _name))
                elif val == 'generic' or val == 'dimmer':
                    _name = str(val) + ' ' + str(key)
                    self.addNode(VirtualGeneric(self, self.address, key, _name))
                else:
                    pass
            else:
                pass
        LOGGER.info('Check Params is complete')