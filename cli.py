#!/usr/bin/env python3
#
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

import argparse

import rows

import marmeleiro


DEFAULT_ENCODING = 'utf-8'
slug = rows.plugins.utils.slug


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ano')
    parser.add_argument('unidade_gestora',
                        choices=marmeleiro.crawler.UNIDADES_GESTORAS)
    args = parser.parse_args()

    unidade = 'MUNICIPIO DE MARMELEIRO'

    # Faz download de todas as páginas para essa busca
    htmls = marmeleiro.crawler.busca_licitacoes(
            'MUNICIPIO DE MARMELEIRO', args.ano, args.unidade_gestora)
    htmls = [html.encode(DEFAULT_ENCODING) for html in htmls]

    # Salva os HTMLs de cada página, exemplo:
    # `licitacoes-2017-CONSOLIDADA-pagina-001.html`
    for number, html in enumerate(htmls, start=1):
        filename = 'licitacoes-{}-{}-pagina-{:03d}.html'.format(
                args.ano, args.unidade_gestora, number)
        with open(filename, mode='wb') as fobj:
            fobj.write(html)

    # Extrai a informação desejada dos HTMLs e salva o resultado final em CSV
    data = []
    for html in htmls:
        table = marmeleiro.parser.extrai_tabela(html,
                                                encoding=DEFAULT_ENCODING)
        data.extend([row._asdict() for row in table])
    final = rows.import_from_dicts(data)
    arquivo = 'licitacoes-{}-{}.csv'.format(args.ano, args.unidade_gestora)
    rows.export_to_csv(final, arquivo)


if __name__ == '__main__':
    main()
