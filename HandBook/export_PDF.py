from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab.pdfgen.canvas


def calculate_max_df_width_height(df):
    lines = []
    for line_number in range(len(df)):
        lines.append(len(''.join([str(element) for element in df.loc[line_number].values])))
    max_width = max(lines)
    max_height = df.shape[0] + 1
    return max_width * 8.5, max_height * 200


def export_df_to_pdf(df, filename):
    width, height = calculate_max_df_width_height(df)

    pagesize = (width, height)
    canvas = reportlab.pdfgen.canvas.Canvas(filename + ".pdf", pagesize=pagesize)
    # c.scale(0.24, 0.24) # Scale so that the image exactly fits the canvas.
    # canvas.drawCentredString(width/2.0, height - 30, "Handbook: " + filename)

    pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', 'static/ReportLabFonts/DejaVuSerif-Italic.ttf'))
    ts = [('ALIGN', (1, 1), (-1, -1), 'CENTER'),
          ('FONT', (0, 0), (-1, -1), 'DejaVuSerif-Italic'),
          ('BOX', (0, 0), (-1, -1), 0.8, colors.black),
          ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
          ('BOX', (0, 0), (-1, 0), 0.8, colors.red),
          ('INNERGRID', (0, 0), (-1, 0), 0.25, colors.red)]

    df_data = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()  # values for pdf
    table = Table(df_data, style=ts)
    table_width, table_height = table.wrap(width, height)  # width and height of table
    margin = int((width - table_width) / 2)
    table.wrapOn(canvas, width, height)
    table.drawOn(canvas, margin, height - table_height - 50)
    canvas.save()