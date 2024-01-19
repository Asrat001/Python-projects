import time
import json
from telethon import errors
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest


def load_config(file_path):
    try:
        with open(file_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return []

def save_config(file_path, config_data):
    with open(file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=2)

def add_and_login(config_data):
    api_id = input("Enter API ID: ")
    api_hash = input("Enter API Hash: ")
    phone_number = input("Enter Phone Number (e.g., +123456789): ")
    session_name = input("Enter Session Name: ")

    # Create a TelegramClient instance
    with TelegramClient(session_name, api_id, api_hash) as client:
        # Ensure you have the necessary session file or log in if it doesn't exist
        if not client.is_user_authorized():
            client.connect()  # Connect to the Telegram servers
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter the code: '))

        # Get the "me" information outside the if block
        me = client.get_me()
        print(f'Logged in as {me.username}')

        # Save the session
        client.session.save()

        # Add the new account to the configuration
        new_config = {
            "api_id": api_id,
            "api_hash": api_hash,
            "phone_number": phone_number,
            "session_name": session_name
        }
        config_data.append(new_config)

        print("Account added and logged in successfully!")



def join_groups_from_file(client, file_path):
    try:
        # Ensure the client is connected before proceeding
        if not client.is_connected():
            client.connect()

        # Read the invite links from the file
        with open(file_path, 'r') as invites_file:
            invite_links = invites_file.read().splitlines()

        for invite_link in invite_links:
            try:
                # Ensure the client is connected before each join attempt
                if not client.is_connected():
                    client.connect()

                # Import the chat using the invite link
                result = client(ImportChatInviteRequest(invite_link))

                # Get the chat ID from the result
                chat_id = result.chat.id

                # Join the group
                client(JoinChannelRequest(chat_id))

                print(f'Successfully joined the group from invite link: {invite_link}')
                time.sleep(5)
            except Exception as e:
                print(f'Failed to join the group from invite link {invite_link}: {e}')

    except errors.rpcerrorlist.ChatWriteForbiddenError as e:
        print(f"Cannot send message to {dialog.title}: {e}")


def run_bot(config_data):
    for account in config_data:
        api_id = account["api_id"]
        api_hash = account["api_hash"]
        phone_number = account["phone_number"]
        session_name = account["session_name"]

        with TelegramClient(session_name, api_id, api_hash) as client:
            if not client.is_user_authorized():
                client.connect()
                client.send_code_request(phone_number)
                client.sign_in(phone_number, input('Enter the code: '))

            me = client.get_me()
            print(f'Logged in as {me.username}')

            client.session.save()

            dialogs = client.get_dialogs()

            for dialog in dialogs:
                if dialog.is_group:
                    try:
                        print(f"Sending a message to {dialog.title}")
                        # Try to send a message to the group
                        # client.send_message(dialog.id, 'Hello from your bot!')

                        # Pause for 10 seconds before sending the next message
                        time.sleep(0.3)

                    except errors.rpcerrorlist.ChatWriteForbiddenError as e:
                        print(f"Cannot send message to {dialog.title}: {e}")

def show_accounts(config_data):
    for account in config_data:
        api_id = account["api_id"]
        api_hash = account["api_hash"]
        phone_number = account["phone_number"]
        session_name = account["session_name"]

        with TelegramClient(session_name, api_id, api_hash) as client:
            if not client.is_user_authorized():
                client.connect()
                client.send_code_request(phone_number)
                client.sign_in(phone_number, input('Enter the code: '))

            me = client.get_me()
            print(f'Logged in as {me.username}')

            client.session.save()

            dialogs = client.get_dialogs()
            print("Groups: ")

            for dialog in dialogs:
                if dialog.is_group:
                    try:
                        print(f"-{dialog.title}")

                    except errors.rpcerrorlist.ChatWriteForbiddenError as e:
                        print(f"Cannot send message to {dialog.title}: {e}")

            print("\n")

# Path to the configuration file
config_file_path = 'config.json'

# Load existing configuration
config_data = load_config(config_file_path)

while True:
    print("\nMenu:")
    print("1. Add and Login")
    print("2. Join Groups from File")
    print("3. Run Bot")
    print("4. Show accounts")
    print("5. Exit")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        add_and_login(config_data)
        save_config(config_file_path, config_data)

    elif choice == '2':
        # Prompt user to choose an account
        print("Choose an account to join groups:")
        for idx, account in enumerate(config_data, 1):
            print(f"{idx}. {account['session_name']}")

        selected_account_index = int(input("Enter the number of the account: ")) - 1

        # Use the selected account to join groups
        selected_account = config_data[selected_account_index]
        api_id = selected_account["api_id"]
        api_hash = selected_account["api_hash"]
        phone_number = selected_account["phone_number"]
        session_name = selected_account["session_name"]
        
        # Create a new client instance for the selected account
        client = TelegramClient(session_name, api_id, api_hash)

        # Join groups using the selected account
        join_groups_from_file(client, 'invite_ids.txt')

        # Disconnect the client after joining groups
        client.disconnect()


    elif choice == '3':
        run_bot(config_data)

    elif choice == '4':
        show_accounts(config_data)

    elif choice == '5':
        print("Exiting the script. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number.")
