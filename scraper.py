# -*- coding: utf-8 -*-
from __future__ import print_function
import scraperwiki
import lxml.html
import time
import cvm_captura_informacoes_zip
import os
import pandas as pd


def get_df_consolidado(lista_csv):
    li = []
    for file_path in lista_csv:
        df = pd.read_csv(file_path, sep=';', encoding='latin1', error_bad_lines=False)

        # transforma o campo CO_PRD
        df['CO_PRD'] = df['CNPJ_FUNDO'].str.replace('.','')
        df['CO_PRD'] = df['CO_PRD'].str.replace('/','')
        df['CO_PRD'] = df['CO_PRD'].str.replace('-','')
        df['CO_PRD'] = df['CO_PRD'].str.zfill(14)
        
        df['DT_COMPTC'] = pd.to_datetime(df['DT_COMPTC'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        df['DT_REF'] = df['DT_COMPTC']

        li.append(df)

    return pd.concat(li, axis=0, ignore_index=True)


def main():
    # faz o download e extrai todos os arquivos
    cvm_captura_informacoes_zip.main()

    folder_path = os.path.join('downloads')
    lamina_fi = []
    lamina_fi_carteira = []
    lamina_fi_rentab_ano = []
    lamina_fi_rentab_mes = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if 'lamina_fi_carteira' in file_name:
            lamina_fi_carteira.append(file_path)
            continue
        
        if 'lamina_fi_rentab_ano' in file_name:
            lamina_fi_rentab_ano.append(file_path)
            continue
        
        if 'lamina_fi_rentab_mes' in file_name:
            lamina_fi_rentab_mes.append(file_path)
            continue            
        
        lamina_fi.append(file_path)

    lamina_fi = sorted(lamina_fi)
    df_lamina_fi = get_df_consolidado(lamina_fi)
    print(len(df_lamina_fi))

    for row in df_lamina_fi.to_dict('records'):
        scraperwiki.sqlite.save(
            unique_keys=df_lamina_fi.columns.values.tolist(),
            data=row
        )

    lamina_fi_carteira = sorted(lamina_fi_carteira)
    df_lamina_fi_carteira =  get_df_consolidado(lamina_fi_carteira)
    print(len(df_lamina_fi_carteira))

    lamina_fi_rentab_ano = sorted(lamina_fi_rentab_ano)
    df_lamina_fi_rentab_ano =  get_df_consolidado(lamina_fi_rentab_ano)
    print(len(df_lamina_fi_rentab_ano))

    lamina_fi_rentab_mes = sorted(lamina_fi_rentab_mes)
    df_lamina_fi_rentab_mes =  get_df_consolidado(lamina_fi_rentab_mes)
    print(len(df_lamina_fi_rentab_mes))


if __name__ == '__main__':
    main()