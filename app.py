from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return render_template('index.html')

def generateSession(self, clientCode, password):

    params = {"clientcode": clientCode, "password": password}
    loginResultObject = self._postRequest("api.login", params)

    if loginResultObject['status'] == True:
        jwtToken = loginResultObject['data']['jwtToken']
        self.setAccessToken(jwtToken)
        refreshToken = loginResultObject['data']['refreshToken']
        feedToken = loginResultObject['data']['feedToken']
        self.setRefreshToken(refreshToken)
        self.setFeedToken(feedToken)
        user = self.getProfile(refreshToken)

        id = user['data']['clientcode']
        # id='D88311'
        self.setUserId(id)
        user['data']['jwtToken'] = "Bearer " + jwtToken
        user['data']['refreshToken'] = refreshToken

        return user
    else:
        return loginResultObject

def login(clientCode, password):

    import datetime

    from SmartApi import SmartConnect

    # ---------for smartExceptions---------
    # import smartapi.smartExceptions
    # or
    # from smartapi import smartExceptions

    smartApi = SmartConnect(api_key="4NUrxtuq")

    #login = smartApi.generateSession('B79682', 'avatar2012')
    login = smartApi.generateSession(clientCode, password)

    refreshToken = login['data']['refreshToken']

    feedToken = smartApi.getfeedToken()

    smartApi.getProfile(refreshToken)

    smartApi.generateToken(refreshToken)

    smartApi.terminateSession(clientCode)


    return login


@app.route('/', methods=['POST'])
def task():
    if request.method == 'POST':
        id = str(request.form['username'])
        password = str(request.form['password'])

        result = login(id, password)
        return render_template('output.html', result=result)


if __name__ == '__main__':
    app.run()
