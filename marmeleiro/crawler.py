# Copyright 2017 Álvaro Justen <https://github.com/turicas>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time

import selenium.common
import splinter


URL_MARMELEIRO = 'http://portal.marmeleiro.pr.gov.br/pronimtb/index.asp?acao=1&item=2'
SLEEP_SECONDS = 0.01
UNIDADES_GESTORAS = (
        'CONSOLIDADA',
        'PREFEITURA MUNICIPAL',
        'FUNDO MUNICIPAL DE SAÚDE',
        'ASSISTÊNCIA SOCIAL',)


class MyBrowser(splinter.driver.webdriver.firefox.WebDriver):

    def aguardar(self):
        'Espera até que a mensagem de "Aguarde" saia da tela'

        finished = False
        while not finished:
            aguarde = self.find_by_id('aguardeinterno')
            try:
                if not aguarde or not aguarde.visible:
                    finished = True
                else:
                    time.sleep(SLEEP_SECONDS)
            except selenium.common.exceptions.StaleElementReferenceException:
                finished = True

        while self.evaluate_script('document.readyState') != 'complete':
            time.sleep(SLEEP_SECONDS)


def busca_licitacoes(unidade, data_vigencia, unidade_gestora):
    'Busca licitações e retorna HTML de todas páginas encontradas'

    if unidade_gestora not in UNIDADES_GESTORAS:
        raise ValueError('Unidade gestora "{}" inválida'
                         .format(unidade_gestora))

    browser = MyBrowser()
    browser.visit(URL_MARMELEIRO)

    while 'id="confirma"' not in browser.html:
        time.sleep(SLEEP_SECONDS)

    select_unidade = browser.find_by_id('cmbUnidadeLC').first
    select_unidade.select_by_text(unidade)

    select_ano = browser.find_by_id('cmbDataVigenciaLC').first
    select_ano.select_by_text(data_vigencia)

    select_unidade_gestora = browser.find_by_id('cmbUnidadeGestoraLC').first
    select_unidade_gestora.select_by_text(unidade_gestora)

    button_confirma = browser.find_by_id('confirma').first
    button_confirma.click()

    htmls = []
    finished = False
    while not finished:
        browser.aguardar()
        htmls.append(browser.html)

        next_page_link = browser.find_link_by_partial_text('Próxima')
        if not next_page_link:
            finished = True
        else:
            next_page_link[0].click()

    browser.quit()

    return htmls
