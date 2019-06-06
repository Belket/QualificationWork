from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A3, A2
import pandas as pd


def export_df_to_pdf(df, filename):
    elements = []
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename + '.pdf', pagesizes=A3)
    df_columns_names = pd.Series(['Название', 'Компания', 'Класс', 'Группа', 'Подгруппа', 'Средняя наработка на отказ',
                                  'Средний срок сохраняемости', 'Средний ресурс (ч)', 'Среднее время восстановления (ч)',
                                  'Дополнительная Информация', 'Дата добавления', 'Подтверждающая ссылка'])
    df.columns = df_columns_names
    df_data = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()
    pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', 'static/ReportLabFonts/DejaVuSerif-Italic.ttf'))
    ts = [('ALIGN', (1, 1), (-1, -1), 'CENTER'),
          ('FONT', (0, 0), (-1, -1), 'DejaVuSerif-Italic'),
          ('BOX', (0, 0), (-1, -1), 0.8, colors.black),
          ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
          ('BOX', (0, 0), (-1, 0), 0.8, colors.red),
          ('INNERGRID', (0, 0), (-1, 0), 0.25, colors.red)]

    table = Table(df_data, style=ts)
    elements.append(table)
    doc.build(elements)