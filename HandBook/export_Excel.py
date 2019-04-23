import numpy as np
import pandas as pd
import xlsxwriter


# Вычисляем длины названий колонок
def columns_names_sizes(df):
    columns_names_lens = []
    for column in df.columns:
        columns_names_lens.append(len(column))
    return columns_names_lens


# Вычисляем длины максимальных элементов каждой колонки
def columns_max_element_sizes(df):
    sizes_list = []
    for column in df.columns:
        if type(df[column][0]) == str:
            sizes_list.append(len(max(df[column], key=len)))
        else:
            sizes_list.append(len(str(max(df[column]))))
    return sizes_list


# Выбираем минимально необходимую ширину колонки для excel
def excel_columns_size(df):
    names_sizes = columns_names_sizes(df)
    elements_sizes = columns_max_element_sizes(df)
    return np.max([names_sizes, elements_sizes], axis=0)


# Устанавливаем ширину колонок
def set_excel_column_sizes(worksheet, sizes):
    for excel_column, size in enumerate(sizes):
        worksheet.set_column(excel_column, excel_column, int(size) + 1)


def export_df_to_excel(df, filename, sheetname='Sheet1'):
    sizes_list = excel_columns_size(df)
    writer = pd.ExcelWriter(filename + '.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheetname, index=False)
    worksheet = writer.sheets[sheetname]
    set_excel_column_sizes(worksheet=worksheet, sizes=sizes_list)
    writer.save()
