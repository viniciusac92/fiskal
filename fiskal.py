from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class Fiskal:
    def __init__(self, dados):
        self.download_directory = "/var/www/html/vinicius/rpa-selenium"
        self.dados = dados
        self.chrome_prefs = {
        "download.default_directory": self.download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
        }
        self.chrome_options = Options() # instancia as opções do chrome
        self.primeira_vez = True # variavel para identificar primeira rodada (round1)
        self.submit_button = 'primeira vez' # variável definida para fazer as 10 tentativas

    # método private utilizado unicamente pela função run
    def __preenchimento_formulario(self, dados, primeira_vez, driver):
        # realiza iteração nos dados de entrada
        for key, value in dados.items():
            # identifica o
            input_field = driver.find_element(By.XPATH, f'//label[text()="{key}"]/following-sibling::input')
            input_field.clear()
            input_field.send_keys(value)
            
            # previne erro identificado no carregamento
            if (primeira_vez):
                try:
                    # botão Start
                    start_button2 = driver.find_element(By.CLASS_NAME, 'uiColorButton')
                    
                    time.sleep(2)

                except NoSuchElementException:
                    print('botao Start não encontrado')

                start_button2.click()

                # seta a variável e prossegue no loop for
                primeira_vez = False
            
            # após preencher o campo, aguarda 1 segundo para evitar erro na pagina
            time.sleep(1)

    def __submit_form(self, driver):
        submit_button = driver.find_element(By.XPATH, '//input[@value="Submit"]')
        submit_button.click()

    # método que executa o script do robô
    def run(self):

        # adiciona as configurações ao chrome
        self.chrome_options.add_experimental_option("prefs", self.chrome_prefs)

        # Inicia o browser com as configurações (options) atualizadas
        driver = webdriver.Chrome(options=self.chrome_options)
        
        # site destino do robô
        driver.get("https://rpachallenge.com/")

        #validação do botão start
        try:
            # botão Start
            start_button = driver.find_element(By.CLASS_NAME, 'uiColorButton')
            
            # temporizador para evitar erro de carregamento no browser
            time.sleep(2)

        except NoSuchElementException:
            print('________Erro encontrado:Botão Start não encontrado________')
            
            # encerra robô se não encontrado start
            driver.quit()


        # inicia a rodada
        start_button.click()

        time.sleep(2)

        # enquanto houver o botão submit na pagina, prossegue o preenchimento da pagina
        # caso contrario, segue para o encerramento 
        while self.submit_button is not None:

            # inicia o preenchimento do formulario
            self.__preenchimento_formulario(self.dados, self.primeira_vez, driver)

            # apos da rodada ele, submite o formulario
            self.__submit_form(driver)

            time.sleep(2)

            # se não houver mais o submit, encerra o loop while para prosseguir e finalizar
            try:
                self.submit_button = driver.find_element(By.XPATH, '//input[@value="Submit"]')
            except NoSuchElementException:
                # encerra o while
                self.submit_button = None

        # utiliza esse try except aqui para confirmar a finalização
        try:
            # método utilizado para encontrar o elemento HTML da página
            elemento_da_tela = driver.find_element(By.CLASS_NAME, 'message1')
            if 'Congratulations!' in elemento_da_tela.text:
                # faz o log de finalização do robô
                print('Mensagem de finalização:', elemento_da_tela.text)
            
                # segue para clicar na exportação
                download_button = driver.find_element(By.XPATH, '//a[contains(@href, "challenge.xlsx")]')
                if (download_button):
                    print('encontrou download')

                download_button.click()

                time.sleep(2)

        except NoSuchElementException:
            print('Mensagem de finalização não encontrada')

        # encerra robô
        driver.quit()