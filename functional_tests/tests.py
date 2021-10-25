from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        #self.browser.quit()
        pass

    def check_for_row_in_list_table(self, row_text):
        #print('wywołano "check_for_row..."')
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta dowiedziała się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia.
        # Postanowia więc przejść na stronę główną tej aplikacji.
        self.browser.get('http://127.0.0.1:8000')

        # Zwróciła uwagę, że tytuł strony i nagłówek zawierają słowo "Listy", "lista".
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('lista', header_text)

        # Od razu zostaje zachęcona, aby wpisać rzecz do zrobienia.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Wpisz rzecz do zrobienia'
        )

        # W plu tekstowym wpisała "Kupić pawie pióra"
        # (hobby Edyty polega na tworzeniu ozdobnych przynęt)
        inputbox.send_keys('Kupić pawie pióra')

        # Po naciśnięciu klawisza Enter strona została uaktalniona i wyświela
        # "1: Kupić pawie pióra" jako element listy rzeczy do zrobienia.
        inputbox.send_keys(Keys.ENTER)
        print('1:', self.browser.current_url)
        time.sleep(1)
        edith_list_url = self.browser.current_url
        print('2:', edith_list_url)
        self.assertRegex(edith_list_url, 'lists/.+')
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

        # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
        # Edyta wpisała "Zrobić przynęty z pawich piór" 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Zrobić przynęty z pawich piór')
        inputbox.send_keys(Keys.ENTER)

        # Strona została ponownie auaktualniona i teraz wyświetla dwa elementy na liście rzeczy do zrobienia.
        self.check_for_row_in_list_table('1: Kupić pawie pióra')
        self.check_for_row_in_list_table('2: Zrobić przynęty z pawich piór')

        # Teraz nowy użytkownik Franek zaczyna korzystać z wityryny.

        ## Używamy nowej sesji przegladarki internetowej, aby miec pewność, że żadne
        ## inrofmacje dotyczące Edyty nie zostaną ujawnione, na przykład przez cookies.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Franek odwiedza stronę główną.
        # Nie znajduje żadnych śladów listy Edyty.
        self.browser.get('http://127.0.0.1:8000')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertNotIn('przynęty', page_text)

        # Franek tworzy nową listę, wprowadzając nowy element.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Kupić mleko')
        inputbox.send_keys(Keys.ENTER)

        # Franek otrzymuje unikatowy adres URL prowadzący do listy.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Ponownie nie ma żadnego śladu po liście Edyty.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertIn('Kupić mleko', page_text)

        # Franek kończy korzystanie z aplikacji.
        self.fail('Zakończenie testu!')
