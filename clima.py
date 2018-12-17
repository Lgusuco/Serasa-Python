import time, json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

#Gera um araquivo para cada cidade em seu estado. No diretório /DADOS
def geraCSV(estado, header,contentCity):
    with open("dados/%s.csv"%estado,"w") as f:
        s = "".join(estado)
        f.write(s + "\n")
        for l in header:
            f.write(l + "\n")

        for l in contentCity:
            f.write(l + "\n")

def main():

    #Configura para iniciar o Google com ADBLOCK caso necessário
    chrome_options = Options()
    chrome_options.add_extension('driver/AdBlock_v3.36.0.crx')

    #permite notificações do Google.
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(chrome_options=chrome_options)

    #Abre URL do site
    driver.get("https://www.climatempo.com.br/climatologia/2713/alemparaiba-mg")

    #Aguarda o carregamento do site
    time.sleep(10)

    #Abre arquivo JSON com as cidades para a busca
    arquivo = open('cidades.json', 'r', encoding="utf8")
    dataJson = json.load(arquivo)

    #Faz um laço entre todos os estados e cidades para a busca
    for estado in dataJson['estados']:

        for cidade in estado['cidades']:

            time.sleep(6)
            #Clica no form Geolocalização para realizar a busca
            climaForm = driver.find_element_by_xpath('//*[@id="mega-destaque"]/div[2]/div[1]/div[1]/p[1]')
            climaForm.click()

            #Aguarda carregamento do FORM
            time.sleep(3)

            #Insere o estado
            select = Select(driver.find_element_by_name("sel-state-geo"))
            select.select_by_value(estado['sigla'])

            time.sleep(3)

            #Insere a cidade
            select = Select(driver.find_element_by_name("sel-city-geo"))
            select.select_by_visible_text(cidade)

            #Clica no para realizar a busca
            filtrar = driver.find_element_by_id('btn-confirm-geo')
            filtrar.click()
            time.sleep(6)

            #Armazena a DIV que possue os dados para a coleta
            dados = driver.find_element_by_class_name('sticky2Equalizer')

            html = dados.get_attribute("innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            table = soup.select_one("table")

            header = []
            data = [d for d in table.select("thead tr")]

            #Aqui realizo a coleta do HEADER da table que está dentro da DIV armazenada
            for d in data:
                linha = ""
                for t in d.select("th"):
                    linha += t.text+"|"
                header.append(linha)

            contentCity = []
            data = [d for d in table.select("tbody tr")]

            # Aqui realizo a coleta dos valores da table que está dentro da DIV armazenada
            for d in data:
                linha = ""
                for t in d.select("td"):
                    linha += t.text+"|"
                contentCity.append(linha)

            estCid = estado['sigla'] +' - '+cidade

            geraCSV(estCid, header, contentCity)
        time.sleep(15)

    driver.close()

if __name__ == '__main__':
    main()