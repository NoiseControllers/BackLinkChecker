import xlsxwriter

from src.Models.UrlModel import UrlModel


def read_file(path: str) -> list:
    data = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            data.append(line.strip())

    return data


def output_file(filename: str, data_list: list):
    outfile = xlsxwriter.Workbook(filename)
    sheet = outfile.add_worksheet()

    header_format = outfile.add_format({'bold': True, 'align': 'center'})
    cell_format = outfile.add_format({'align': 'center'})
    sheet.set_column(0, 0, 120)
    sheet.set_column(1, 1, 10)
    sheet.set_column(2, 2, 15)
    sheet.write("A1", "URL", header_format)
    sheet.write("B1", "FOUND", header_format)
    sheet.write("C1", "TYPE", header_format)

    for pos, item in enumerate(data_list):
        sheet.write(pos+1, 0, item[0])
        sheet.write(pos+1, 1, item[2], cell_format)
        sheet.write(pos+1, 2, item[3], cell_format)

    outfile.close()
