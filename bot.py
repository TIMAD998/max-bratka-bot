import asyncio
import random
from python_max_client import MaxClient
import os

YOUR_PHONE = os.getenv('YOUR_PHONE')
MASTER_PHONE = os.getenv('MASTER_PHONE')

async def main():
    client = MaxClient()
    await client.connect()
    
    phone = YOUR_PHONE
    sms_token = await client.send_code(phone)
    code = input("Введи код из смс: ")
    await client.sign_in(sms_token, int(code))

    async def message_handler(client, packet):
        # Проверяем, что это новое сообщение
        if packet['opcode'] == 128:
            # 🚨 ВОТ ТУТ МЫ ЛОВИМ ID ГРУППЫ 🚨
            chat_id = packet['payload']['chatId']
            sender_phone = packet['payload']['message']['from']['phone']
            message_text = packet['payload']['message']['text'].strip()
            
            # Временная печать ID в консоль (для нас)
            print(f"🔍 [ТЕСТ] ID этой группы: {chat_id}")
            print(f"👤 Отправитель: {sender_phone}")
            print(f"💬 Текст: {message_text}")
            print("-" * 30)

            # Тут потом будет основной код с ответами
            # Пока закомментировали, чтобы не мешал
            """
            if sender_phone == MASTER_PHONE:
                if message_text == "я же прав братки ?" or message_text == "я же прав братки, прав?":
                    answers = ["конечно прав братка", "определенно прав братка"]
                    random_answer = random.choice(answers)
                    await client.send_message(chat_id=chat_id, text=random_answer)
                    print(f"✅ Ответил: {random_answer}")
            """

    await client.set_callback(message_handler)
    print("🕵️‍♂️ Бот запущен в режиме поиска ID. Напиши что-нибудь в группе...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
