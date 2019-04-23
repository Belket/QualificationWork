from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors


def export_df_to_pdf(df, filename):
    elements = []
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename + '.pdf')
    elements.append(Paragraph("Report Title", styles['Title']))
    df_data = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()

    ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
          ('FONT', (0,0), (-1,0), 'Times-Roman'),
          ('BOX', (0,0), (-1,-1), 0.8, colors.black),
          ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
          ('BOX', (0,0), (-1,0), 0.8, colors.red),
          ('INNERGRID', (0,0), (-1,0), 0.25, colors.red)]

    table = Table(data=df_data, style=ts)
    elements.append(table)
    doc.build(elements)
