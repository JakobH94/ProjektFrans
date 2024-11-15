## BIBLIOTEK ##
import argparse
from cryptography.fernet import Fernet, InvalidToken
import pyfiglet
from colorama import init, Fore, Back, Style
import os

init(autoreset=True)

ascii_art = pyfiglet.figlet_format("FRANS PROJEKT")
print(ascii_art)

## GENERERA NYCKEL ##
def generate_key(file_path):
    try:
        key = Fernet.generate_key()
        with open(file_path, 'wb') as key_file:
            key_file.write(key)
        print(Back.GREEN + f"Du lyckades att spara nyckel till '{file_path}'" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Fel vid generering av nyckel '{e}'\n" + Style.RESET_ALL)

## KRYPTERA ##
def encrypt_file(key_path, file_path, output_path):
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        with open(file_path, 'rb') as file:
            data = file.read()
        encrypted_data = fernet.encrypt(data)
        with open(output_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        print("Du " + Fore.GREEN + "lyckades " + Style.RESET_ALL + f"att kryptera och spara filen till '{output_path}'\n")
    except FileNotFoundError as e:
        print(Fore.RED + f"Filen kunde inte hittas '{e}'\n" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Ett fel inträffade vid kryptering '{e}'\n" + Style.RESET_ALL)

## DEKRYPTERA ##
def decrypt_file(key_path, encrypted_path, output_path):
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        with open(encrypted_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except InvalidToken:
            print(Fore.RED + "Felaktig nyckel eller fil. Kontrollera att du använder rätt nyckel och försök igen.\n" + Style.RESET_ALL)
            return
        with open(output_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print("Du " + Fore.GREEN + "lyckades " + Style.RESET_ALL + f"att dekryptera och spara filen till '{output_path}'\n")
    except FileNotFoundError as e:
        print(Fore.RED + f"Filen kunde inte hittas '{e}'\n" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Ett fel inträffade vid dekryptering '{e}'\n" + Style.RESET_ALL)

## HUVUD ##
def main():
    parser = argparse.ArgumentParser(description="Kryptera och dekryptera filer med symmetrisk nyckel.")

## Hjälp för att använda rätt kommando genom att lägga till "--" inför varje kommando dvs --generate, --encrypt, --decrypt ##
    parser.add_argument('--generate', help="Generera och spara krypteringsnyckel till en fil", type=str)
    parser.add_argument('--encrypt', nargs=3, metavar=('key_path', 'file_path', 'output_path'),
                        help="Kryptera en fil med en nyckel")
    parser.add_argument('--decrypt', nargs=3, metavar=('key_path', 'encrypted_path', 'output_path'),
                        help="Dekryptera en krypterad fil med en nyckel")

    args = parser.parse_args()

## Funktioner beroende på vad som körs ##
    if args.generate:
        generate_key(args.generate)
    elif args.encrypt:
        encrypt_file(*args.encrypt)
    elif args.decrypt:
        decrypt_file(*args.decrypt)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()