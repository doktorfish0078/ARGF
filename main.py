from flask import Flask, render_template, url_for, request

from random import randint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import os


app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def show_home_page():
    if request.method == 'GET':
        url = request.args.get('url')
        count_loops = request.args.get('count_loops')
        if url and count_loops:
            auto_recording_forms(url, int(count_loops))
        return render_template("home.html")


def auto_recording_forms(URL, count_loops):
    options = Options()
    options.add_argument("--headless")
    options.binary_location = os.environ.get("PATH")
    driver = webdriver.Firefox(executable_path=os.environ.get("GECKO_PATH"), options=options)

    try:
        driver.get(URL)

        for i in range(0, count_loops):
            all_questions_containers = driver.find_elements_by_class_name("freebirdFormviewerViewNumberedItemContainer")
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

        print('its all')
    except:
        print('abasralc9')


if __name__ == '__main__':
    app.run(debug=False)