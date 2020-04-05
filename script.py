import requests
import datetime
import pprint
import json
import plotly.graph_objects as go


def main():
    tokenVk = 'MY_TOKEN_VK'
    url = 'https://api.vk.com/method/newsfeed.search'
    keyword = 'кока-кола'
    dates = get_dates()
    data = []
    for date in dates:
        response = requests.get(url + '?q=' + keyword + '&count=10&start_time=' + str(date['start_time']) + '&end_time=' + str(date['end_time']) + '&access_token=' + tokenVk + '&v=5.103')
        if response.status_code == 200:
            content = response.content
            content = json.loads(content)
            data.append({
                'start_time': date['start_time'],
                'end_time': date['end_time'],
                'count': content['response']['count'],
                'start_human_date': date['start_human_date'],
                'end_human_date': date['end_human_date']
            })
            print(date['start_human_date'], 'was processed ')
            print('#'*30)
        else:
            print(date['start_human_date'], 'fail processed ')
            print('#'*30)
    # pprint.pprint(data)
    build_graphic(data)


# build graphic!
def build_graphic(data):
    x = []
    y = []
    for item in data:
        x.append(item['start_human_date'])
        y.append(item['count'])
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.show()


# default -10 days
def get_dates(start_day=1, end_day=11):
    dates = []
    while start_day < end_day:
        today = datetime.date.today() - datetime.timedelta(days=start_day-1)
        yesterday = datetime.date.today() - datetime.timedelta(days=start_day)
        start_time = int(datetime.datetime(year=yesterday.year, month=yesterday.month, day=yesterday.day).timestamp())
        end_time = int(datetime.datetime(year=today.year, month=today.month, day=today.day).timestamp())
        dates.append({
            'start_time': start_time,
            'end_time': end_time,
            'start_human_date': yesterday,
            'end_human_date': today
        })
        start_day += 1
    return dates


if __name__ == '__main__':
    main()
