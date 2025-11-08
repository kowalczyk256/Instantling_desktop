from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
import sqlite3
import time
from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
import threading
from tkinter import messagebox
import random
from tkinter import simpledialog
import os

class instantling:
    def __init__(self, root):
        self.root = root
        self.root.title("Instantling")
        self.g_menu = Menu(root)
        root.config(menu=self.g_menu)
        self.opcje_menu = Menu(self.g_menu, tearoff=False)
        self.g_menu.add_cascade(label="Opcje", menu=self.opcje_menu)
        self.opcje_menu.add_command(label="Podaj login i hasło", command=self.login_password)
        self.opcje_menu.add_command(label="Tryb bota", command=self.bot)
        self.opcje_menu.add_command(label="Tryb symulacji człowieka", command=self.human)
        self.bot_type = tk.Label(text="Wybrany tryb: bot")
        self.bot_type.grid(column=1, row=2)
        self.start_button = tk.Button(root, text="Rozpocznij sesje", bg="green", fg="white", font="10", command=self.play)
        self.info_button = tk.Button(root, text="?", command=self.info)
        self.start_button.grid(column=1, row=1)
        self.info_button.grid(column=4, row=1)
        self.output_info = tk.Label(text="Powiadomienia skryptu:")
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.output_text.grid(column=3, row=3)
        self.output_info.grid(column=3, row=2)
        self.user = tk.Label(text="")
        self.user.grid(column=1, row=3)
        self.read_credentials()
        messagebox.showinfo("Cześć!","Pamiętaj, że używając tego programu niczego się nie nauczysz! Jednak gdy nie masz czasu lub poprostu Ci się nie chce korzystaj :)")
        self.work = 0

    def read_credentials(self):
        try:
            with open('login.txt', 'r') as file1:
                loginl = file1.read()
                file1.close()
            with open('password.txt', 'r') as file2:
                passwordl = file2.read()
                file2.close()

            textf = "L: " + loginl + ", " + "H: " + passwordl + ""
            self.user.config(text=textf)
            return loginl, passwordl
        except FileNotFoundError:
            messagebox.showinfo("Halo!", "Najpierw wpisz swój login i hasło w zakładce opcje")
            return None

    def login_password(self):
        login = simpledialog.askstring("Login", "Wprowadź Twój login:")
        if login:
            with open("login.txt", "w") as file3:
                file3.write(f"{login}")
                file3.close()
        else:
            messagebox.showinfo("Halo!", "Nie wpisałeś loginu :)")

        password = simpledialog.askstring("Hasło", "Wprowadwź Twoje hasło:")
        if password:
            with open("password.txt", "w") as file4:
                file4.write(f"{password}")
                file4.close()
                self.read_credentials()
        else:
            messagebox.showinfo("Halo!", "Nie wpisałeś hasła :)")

    def bot (self):
        self.bot_type["text"] = "Wybrany tryb: bot"
        self.work = 0

    def human (self):
        self.bot_type["text"] = "Wybrany tryb: człowiek"
        self.work = 1
    
    def work_type(self):
        if self.work == 1:
            sleep = random.randint(3, 20)
            return sleep
        else:
            return random.randint(1, 2)
    

    def info(self):
        messagebox.showinfo("Informacja","By slomkaDziadziusia Team, wersja 1.2.1 (open source)")

    def sessions(self):
            session = simpledialog.askinteger("Sesja", "Podaj ilość sesji:")
            if session:
                return session
            else:
                session = 0
                messagebox.showinfo("Halo!", "Nie wpisałeś ilości sesji")
                return session

    def play(self):
        try:
            self.number_loops = self.sessions() 
            
            if self.number_loops <= 0:
                return
                
            test = self.read_credentials()
            if test: 
                threading.Thread(target=self.run_session).start()
        except AttributeError:
            self.log_to_gui("Błąd: Najpierw ustaw login i hasło w Opcjach.")
            self.read_credentials()

    def log_to_gui(self, message):
        log_message = message + "\n"
        self.output_text.insert(tk.END, log_message)
        self.output_text.see(tk.END)
        print(log_message, end='')

    def introduce_typo(self, word):
        if len(word) > 1 and random.random() < 0.2:
            index = random.randint(0, len(word) - 1)
            typo_letter = random.choice('abcdefghijklmnopqrstuvwxyz')
            word = word[:index] + typo_letter + word[index + 1:]
        return word

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        return driver

    def setup_database(self):
        db = sqlite3.connect('instaling.db')
        c = db.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS dane (
                polski text, 
                angielski text,
                info text
            )
        ''')
        return db, c

    def remove_incomplete_entries(self, c, db):
        try:
            c.execute("DELETE FROM dane WHERE polski IS NULL OR polski = '' OR angielski IS NULL OR angielski = '' OR info IS NULL OR info = ''")
            db.commit()
        except sqlite3.Error as e:
            self.log_to_gui(f"Błąd podczas usuwania niekompletnych wpisów: {e}")

    def add_word(self, driver, c, db, a_polish, info):
        self.log_to_gui("Rozpoczynam dodawanie do bazy.")
        self.remove_incomplete_entries(c, db) 

        try:
            try:
                answer = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, 'answer'))
                )
                answer.clear()
            except Exception as e:
                pass 

            WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.ID, 'check'))).click()
            WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="word"]')))
            
            time.sleep(1) 

            english = driver.find_element(By.XPATH, '//*[@id="word"]').get_attribute("textContent")
            self.log_to_gui(f"Slowo po angielsku to: {english}")
            self.log_to_gui(f"Slowo po polsku to: {a_polish}")
            
            if english.strip() and a_polish.strip() and info.strip():
                try:
                    c.execute("INSERT or IGNORE INTO dane (polski, angielski, info) VALUES (?, ?, ?)", (a_polish, english, info))
                    self.log_to_gui("Wprowadzam do bazy danych.")
                except sqlite3.IntegrityError:
                    self.log_to_gui("To slowo już istnieje")
                db.commit()
            else:
                self.log_to_gui("Dane są puste, nie dodaję do bazy.")
            
            WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="next_word"]'))).click()
        except Exception as e:
            self.log_to_gui(f"Błąd podczas dodawania słowa: {e}")
        
    def start(self, driver):
        request_element = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="question"]/div[2]/div[2]'))
        )
        info_element = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[8]/div[1]/div[1]'))
        )
        request = request_element.get_attribute("textContent")
        r_info = info_element.get_attribute("textContent")
        
        self.log_to_gui(f"Szukane slowo: {request}")
        self.log_to_gui(f"Opis slowa to: {r_info}")
        return request, r_info

    def check_translation(self, driver, c, db, request, r_info):
        self.remove_incomplete_entries(c, db)
        
        try: 
            knownew_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="know_new"]'))
            )
            knownew_button.click()
            skip_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="skip"]'))
            )
            skip_button.click()
            return "SKIPPED"
        except:
            c.execute("SELECT angielski FROM dane WHERE polski=? and info=?", (request, r_info))
            result = c.fetchone()
            if result:
                self.log_to_gui(f"Tlumaczenie to: {result[0]}")
                return result[0]
            else:
                self.log_to_gui("Nie mam tlumaczenia.")
                return None
    
    def run_session(self):
        logpas = self.read_credentials()
        if not logpas:
            self.log_to_gui("Błąd: Nie można odczytać loginu i hasła. Ustaw w Opcjach.")
            return
        
        log = logpas[0]
        pas = logpas[1]
        number_of_sessions = self.number_loops
        
        if self.work == 1:
            mode = "human"
        else:
            mode = "bot"

        self.log_to_gui(f"Uruchamianie sesji: {log}, Sesje: {number_of_sessions}, Tryb: {mode}")

        for i in range(number_of_sessions):
            self.log_to_gui(f"--- Rozpoczynanie sesji {i+1} / {number_of_sessions} ---")
            driver = None
            db = None
            try:
                driver = self.setup_driver()
                db, c = self.setup_database()
                
                driver.get("https://instaling.pl/teacher.php?page=login")

                try:
                    agree_button = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/button[1]/p'))
                    )
                    agree_button.click()
                except Exception:
                    pass
                
                login_field = driver.find_element(By.NAME, 'log_email')
                login_field.send_keys(log)
                passwd_field = driver.find_element(By.NAME, 'log_password')
                passwd_field.send_keys(pas)
                passwd_field.send_keys(Keys.RETURN)
                self.log_to_gui("Zalogowano.")

                try:
                    x_button_post = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="streak-button-close"]'))
                    )
                    x_button_post.click()
                except Exception:
                    pass

                step_1_success = False
                try:
                    session_btn = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.big_button.btn.btn-session.sesion'))
                    )
                    session_btn.click()
                    step_1_success = True

                except Exception as e_session:
                    try:
                        daily_session_btn = WebDriverWait(driver, 7).until(
                            EC.element_to_be_clickable((By.LINK_TEXT, 'Rozpocznij codzienną sesję'))
                        )
                        daily_session_btn.click()
                        step_1_success = True

                    except Exception as e_daily:
                        try:
                            next_session_btn = WebDriverWait(driver, 7).until(
                                EC.element_to_be_clickable((By.LINK_TEXT, 'Rozpocznij kolejną sesję'))
                            )
                            next_session_btn.click()
                            step_1_success = True
                        
                        except Exception as e_next:
                            try:
                                finish_session_btn = WebDriverWait(driver, 7).until(
                                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Dokończ sesję'))
                                )
                                finish_session_btn.click()
                                step_1_success = True
                                
                            except Exception as e_finish:
                                self.log_to_gui(f"Błąd uruchomienia sesji. Nie znaleziono przycisku start.")
                                continue 
                            
                if step_1_success:
                    try:
                        continue_btn = WebDriverWait(driver, 7).until(
                            EC.element_to_be_clickable((By.ID, 'continue_session_button'))
                        )
                        continue_btn.click()
                        self.log_to_gui("Rozpoczęto sesję.")
                    except Exception as e_continue:
                        try:
                            start_btn = WebDriverWait(driver, 7).until(
                                EC.element_to_be_clickable((By.ID, 'start_session_button'))
                            )
                            start_btn.click()
                            self.log_to_gui("Rozpoczęto sesję.")
                        except Exception as e_start:
                            self.log_to_gui(f"Nie można rozpocząć sesji (błąd krok 2).")
                            continue 

                time.sleep(random.randint(2, 4)) 

                while True:
                    try:
                        request, r_info = self.start(driver)
                        translation = self.check_translation(driver, c, db, request, r_info)
                        
                        if translation and translation != "SKIPPED":
                            
                            original_translation = translation
                            if mode == "human":
                                translation = self.introduce_typo(translation)
                                if translation != original_translation:
                                    self.log_to_gui("Wprowadzono celową literówkę...")
                                time.sleep(random.randint(5, 25))

                            answer = WebDriverWait(driver, 7).until(
                                EC.element_to_be_clickable((By.ID, 'answer'))
                            )
                            answer.send_keys(translation)
                            time.sleep(1) 
                            WebDriverWait(driver, 7).until(
                                EC.element_to_be_clickable((By.ID, 'check'))
                            ).click()
                            
                            WebDriverWait(driver, 7).until(
                                EC.element_to_be_clickable((By.XPATH, '//*[@id="next_word"]'))
                            ).click()

                            self.log_to_gui("---------------------------------------")
                        
                        elif translation is None: 
                            self.add_word(driver, c, db, request, r_info)
                            self.log_to_gui("---------------------------------------")
                        
                        elif translation == "SKIPPED": 
                            self.log_to_gui("Pominięto nowe słowo.")
                            self.log_to_gui("---------------------------------------")

                        time.sleep(random.randint(2, 4)) 

                    except ElementNotInteractableException:
                        self.log_to_gui("Element nie jest interaktywny, kończę sesję.\n### Koniec sesji ###")
                        break
                    except Exception as e:
                        self.log_to_gui("\n### Koniec sesji ###")
                        break
            
            except Exception as e:
                self.log_to_gui(f"Błąd krytyczny podczas konfiguracji sesji: {e}")
            
            finally:
                if driver:
                    driver.quit()
                if db:
                    db.close()
                self.log_to_gui(f"--- Zakończono sesję {i+1} / {number_of_sessions} ---")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    
    try:
        icon = tk.PhotoImage(file="instantling_icon2.png")
        root.iconphoto(False, icon)
    except tk.TclError:
        print("Nie znaleziono pliku ikony 'instantling_icon2.png'.")

    app = instantling(root)
    root.mainloop()