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

from pathlib import Path

import rows

import marmeleiro


DEFAULT_ENCODING = 'utf-8'
BASE_PATH = Path(__file__).parent
HTML_PATH = BASE_PATH.joinpath('data', 'html')
CSV_PATH = BASE_PATH.joinpath('data', 'csv')
slug = rows.plugins.utils.slug


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ano')
    parser.add_argument('unidade_gestora',
                        choices=marmeleiro.crawler.UNIDADES_GESTORAS)
    args = parser.parse_args()
    unidade = 'MUNICIPIO DE MARMELEIRO'
    slug_unidade_gestora = slug(args.unidade_gestora)

    HTML_PATH.mkdir(parents=True, exist_ok=True)
    CSV_PATH.mkdir(parents=True, exist_ok=True)

    print('Downloading data...', end='', flush=True)
    htmls = marmeleiro.crawler.busca_licitacoes(
            'MUNICIPIO DE MARMELEIRO', args.ano, args.unidade_gestora)
    htmls = [html.encode(DEFAULT_ENCODING) for html in htmls]
    print(' done.')

    print('Saving downloaded HTMLs on filesystem...', end='', flush=True)
    for number, html in enumerate(htmls, start=1):
        filepath = HTML_PATH.joinpath(
                'licitacoes-{}-{}-pagina-{:03d}.html'.format(
                    args.ano, slug_unidade_gestora, number))
        with filepath.open(mode='wb') as fobj:
            fobj.write(html)
    print(' done.')

    print('Extracting desired data...', end='', flush=True)
    data = []
    for html in htmls:
        table = marmeleiro.parser.extrai_tabela(html,
                                                encoding=DEFAULT_ENCODING)
        data.extend([row._asdict() for row in table])
    print(' done.')

    print('Exporting to a single CSV...', end='', flush=True)
    final = rows.import_from_dicts(data)
    filepath = CSV_PATH.joinpath('licitacoes-{}-{}.csv'
                                 .format(args.ano, slug_unidade_gestora))
    rows.export_to_csv(final, str(filepath))
    print(' done.')


if __name__ == '__main__':
    main()
