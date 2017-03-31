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

import io

from collections import OrderedDict

import rows


extract_text = rows.plugins.html.extract_text


class PtBrDateField(rows.fields.DateField):
    'Parser de data no formato brasileiro, exemplo: 23/12/2016'

    INPUT_FORMAT = '%d/%m/%Y'

    @classmethod
    def deserialize(cls, value):
        value = value.strip()
        if value == '':
            return ''
        else:
            return super(PtBrDateField, cls).deserialize(extract_text(value))


class PtBrDecimalField(rows.fields.DecimalField):
    'Parser de valores em Reais brasileiros, exemplo: R$ 1.234,56'

    @classmethod
    def deserialize(cls, value):
        value = extract_text(value).replace('R$', '')\
                                   .replace('.', '')\
                                   .replace(',', '.')\
                                   .strip()
        return super(PtBrDecimalField, cls).deserialize(value)


class StripHtmlField(rows.fields.TextField):
    'Limpa tags HTML e retorna apenas o conteúdo'

    @classmethod
    def deserialize(cls, value):
        if '<' and '>' in value:
            value = extract_text(value)
        return value


class AnexoBoolField(rows.fields.BoolField):
    'BoolField para a imagem que diz se a licitação possui ou não anexo'

    @classmethod
    def deserialize(cls, value):
        return 'Imagens/anexo.png' in value


FIELDS = OrderedDict([
    ('unidade_gestora', StripHtmlField),
    ('nr_do_processo', StripHtmlField),
    ('modalidade', StripHtmlField),
    ('tipo', StripHtmlField),
    ('situacao_do_processo', StripHtmlField),
    ('data_de_julgamento', PtBrDateField),
    ('data_de_homologacao', PtBrDateField),
    ('objeto_desc', StripHtmlField),
    ('valor', PtBrDecimalField),
    ('possui_anexo', AnexoBoolField), ])


def extrai_tabela(html, encoding):
    'Extrai dados da tabela a partir de um HTML e retorna `rows.Table`'

    inicio_tabela = html.find(b'<table id="tbTabela"')
    fim_tabela = html.find(b'</table>', inicio_tabela) + len(b'</table>')
    html = html[inicio_tabela:fim_tabela]

    return rows.import_from_html(io.BytesIO(html),
                                 encoding=encoding,
                                 preserve_html=True,
                                 fields=FIELDS)
