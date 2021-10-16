from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        print('000')
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta dowiedziała się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia.
        # Postanowia więc przejść na stronę główną tej aplikacji.
        self.browser.get('http://localhost:8000')

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
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

        # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
        # Edyta wpisała "Zrobić przynęty z pawich piór"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Zrobić przynęty z pawich piór')
        inputbox.send_keys(Keys.ENTER)

        # Strona została ponownie auaktualniona i teraz wyświetla dwa elementy na liście rzeczy do zrobienia.
        self.check_for_row_in_list_table('1: Kupić pawie pióra')
        self.check_for_row_in_list_table('2: Zrobić przynęty z pawich piór')

        # Edyta była ciekawa, czy witryna zapamięta jej listę. 
	# Zwróciłą uwagę na wygenerowany dla niej unikatowy adres URL, 
	# obok którego znajduje się pewien tekst z wyjaśnieniem.
        self.fail('Zakończenie testu!')

        # Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.

        # Edyta kończy używanie aplikacji, na dziś wystarczy.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
