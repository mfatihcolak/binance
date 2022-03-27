import requests
import keys

def telegramBotSendText(botMessage,id):
    botToken = keys.telegramToken
    botChatId = id
    sendText = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + botChatId + "&parse_mode" \
                                                                                                 "=Markdown&text=" \
                                                                                                + botMessage

    response = requests.get(sendText)
    return response.json()

