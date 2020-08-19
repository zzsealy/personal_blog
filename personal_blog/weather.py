import requests, time, json


def get_weather():
    url = "https://way.jd.com/he/freeweather"
    appid = "72be550cfba50ce30e9678744f5d1d77"
    post_data = {"appkey":appid, "city":"beijing"}
    data = json.dumps(post_data)

    response = requests.post(url, post_data)

    r = response.text

    r =  json.loads(r)


    today = r["result"]["HeWeather5"][0]["daily_forecast"][0]

    print(today)
    





if __name__ == "__main__":
    get_weather()





