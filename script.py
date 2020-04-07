import requests
import datetime
import logging
import plotly.graph_objects as go

logging.basicConfig(level=logging.INFO)


def main():
    token_vk = 'MY_VK_TOKEN'
    url = 'https://api.vk.com/method/newsfeed.search'
    keyword = 'python junior'
    dates = get_dates()
    data = []
    for date in dates:
        params = {
            'q': keyword,
            'count': 10,
            'start_time': str(date['start_time']),
            'end_time': str(date['end_time']),
            'access_token': token_vk,
            'v': '5.103'
        }
        response = requests.get(url, params=params)
        if response.ok:
            content = response.json()
            data.append({
                'start_time': date['start_time'],
                'end_time': date['end_time'],
                'count': content['response']['count'],
                'start_human_date': date['start_human_date'],
                'end_human_date': date['end_human_date']
            })
            logging.info('{} {}'.format(str(date['start_human_date']), 'was processed'))
            logging.info('#' * 30)
        else:
            logging.info('{} {}'.format(str(date['start_human_date']), 'fail processed'))
            logging.info('#' * 30)
    build_graphic(data)


def build_graphic(data):
    x = [i['start_human_date'] for i in data]
    y = [i['count'] for i in data]

    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.show()


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
