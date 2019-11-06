import vk_api
import  sscBotFunctions as sscbf

# Запуск программы
vk_session = vk_api.VkApi(token=token)

vk = vk_session.get_api()
longpoll = vk_api.longpoll.VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW and event.to_me and event.text:
        response = event.text.lower()

        msg = sscbf.cmdback(response)

        vk.messages.send(
            random_id = vk_api.utils.get_random_id(),
            user_id = event.user_id,
            message = msg
        )
