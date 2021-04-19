from time import sleep

import os

from random import randint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from tkinter import *
import threading


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Автозаполнение форм")
        # window.geometry("400x120")

        self.frame0 = Frame(self)
        self.frame0.pack(fill=X)
        self.info_text = Label(self.frame0)
        self.info_text[
            'text'] = "Отвечает в формах только на checkbox и singlebox.\nМаксимальное количество циклов заполенния за 1 раз - 5, из-за какой-то фигни с google forms"
        self.info_text.pack(side=LEFT, padx=5, pady=5)
        self.frame1 = Frame(self)
        self.frame1.pack(fill=X)
        self.lbl = Label(self.frame1, text="URL-link google form")
        self.lbl.pack(side=LEFT, padx=5, pady=5)
        self.input_url = Entry(self.frame1)
        self.input_url.pack(fill=X, padx=5, expand=True)

        self.frame2 = Frame(self)
        self.frame2.pack(fill=X)
        self.lbl1 = Label(self.frame2, text='Number loop recording form')
        self.lbl1.pack(side=LEFT, padx=5, pady=5)
        self.input_count_loop = Entry(self.frame2)
        self.input_count_loop.pack(fill=X, side=LEFT, padx=5, expand=True)

        self.frame3 = Frame(self)
        self.frame3.pack(fill=X)
        self.lbl2 = Label(self.frame3, text='Info string:')
        self.lbl2.pack(side=LEFT, padx=3)
        self.info_label = Label(self.frame3, text='')
        self.info_label.pack(side=LEFT, padx=3)

        self.frame4 = Frame(self)
        self.frame4.pack(fill=X)
        self.button = Button(self.frame4, text='Start', command=self.start_action)
        self.button.pack(side=BOTTOM)

        self.frame5 = Frame(self)
        self.frame5.pack(fill=X)
        self.lbl3 = Label(self.frame5, text='Version product v.1.0.')
        self.lbl3.pack(side=RIGHT)

    def check_thread(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.check_thread(thread))
        else:
            self.button.config(state=NORMAL)

    def start_action(self):
        self.button.config(state=DISABLED)
        thread = threading.Thread(target=self.auto_recording_forms)
        thread.start()
        self.check_thread(thread)

    def auto_recording_forms(self):
        self.info_label['text'] = "Start"

        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Firefox()

        try:
            URL = self.input_url.get()
            count_loop = int(self.input_count_loop.get())
            driver.get(URL)

            for i in range(0, count_loop):
                self.info_label['text'] = "From #{}".format(i + 1)

                all_questions_containers = driver.find_elements_by_class_name(
                    "freebirdFormviewerViewNumberedItemContainer")
                for container in all_questions_containers:

                    variants_answer = container.find_elements_by_class_name('docssharedWizToggleLabeledContainer')
                    class_name_variant = variants_answer[0].get_attribute("class")
                    if 'Checkbox' in class_name_variant:
                        rand_count_answer = randint(1, len(variants_answer) - 1)
                        for current_ans in range(0, rand_count_answer):
                            rand_answer = randint(0, len(variants_answer) - 1)
                            variants_answer[rand_answer].click()

                    if 'Radio' in class_name_variant:
                        rand_answer = randint(0, len(variants_answer) - 1)
                        variants_answer[rand_answer].click()

                driver.find_elements_by_class_name('exportButtonContent')[-1].click()
                driver.find_element_by_class_name('freebirdFormviewerViewResponseConfirmContentContainer').find_element_by_tag_name('a').click()
            driver.close()

            self.info_label['text'] = "Success"
            print('its all')
        except:
            self.info_label['text'] = "Failure"


if __name__ == "__main__":
    app = App()
    app.mainloop()
