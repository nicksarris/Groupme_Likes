__author__ = 'Nick Sarris (ngs5st)'

import requests
import time

request_params = {'token': '',
                  'limit': 100}

def like_ratio(user_data):

    num_messages = 0
    num_likes = 0

    for data in user_data:
        for like in data['favorited_by']:
            num_likes += 1
        num_messages += 1

    ratio = float(num_likes / num_messages)
    return ratio

def map_ids(output_data, id_mapping):

    for message in output_data:
        if message['user_id'] in id_mapping.keys():
            continue
        id_mapping[message['user_id']] = message['name']

    return id_mapping

def collect_data(output_data, id_mapping, blacklisted):

    user_data = {}
    final_data = []

    for message in output_data:
        if message['user_id'] in user_data and \
                        id_mapping[message['user_id']] not in blacklisted:
            list.append(user_data[message['user_id']], message)
            continue
        if id_mapping[message['user_id']] not in blacklisted:
            user_data[message['user_id']] = [message]

    for user, data in user_data.items():
        list.append(final_data, [id_mapping[user], like_ratio(data)])

    final_data.sort(key=lambda x: x[1], reverse=True)
    return final_data

def main():

    id_mapping = {}
    blacklisted = ["GroupMe", "LikeRatioBot"]
    responded = []

    while True:

        url = 'https://api.groupme.com/v3/groups/''/messages'
        response = requests.get(url, params=request_params)

        output_data = []
        ln_break = "\r\n"

        if (response.status_code == 200):
            output_data = response.json()['response']['messages']

        id_mapping = map_ids(output_data, id_mapping)
        ratio_data = collect_data(output_data, id_mapping, blacklisted)

        for message in output_data:

            if message['text'] == "!likeratios" and message['id'] not in responded:
                list.append(responded, message['id'])

                post_data = "Personal Like Ratios: " + ln_break + \
                            "(Last 100 Messages): " + ln_break + ln_break

                for data in ratio_data[:-1]:
                    post_data += str(data[0]) + ": " + str(round(data[1], 4)) + ln_break

                post_data += str(ratio_data[-1][0]) + ": " + str(round(ratio_data[-1][1], 3))
                post_params = {'bot_id': '6b4aa88b05b8d942b2416f2d8c', 'text': post_data}
                requests.post('https://api.groupme.com/v3/bots/post', params=post_params)

        time.sleep(5)

if __name__ == '__main__':
    main()