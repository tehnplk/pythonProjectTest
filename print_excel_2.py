import win32com.client
import os


def print_excel(file_path):
    # Create an instance of the Excel application
    excel = win32com.client.Dispatch("Excel.Application")
    # Open the workbook
    workbook = excel.Workbooks.Open(file_path)
    # Print the workbook to the default printer

    worksheet = workbook.Worksheets(1)

    # Set up the page layout for an 80mm wide printer
    worksheet.PageSetup.PaperSize = 9  # xlPaperUser (custom paper size)
    worksheet.PageSetup.Zoom = False  # Disable zoom to fit to page size
    worksheet.PageSetup.FitToPagesWide = 1
    worksheet.PageSetup.FitToPagesTall = False  # Fit to width, not height

    # Set margins (optional)
    worksheet.PageSetup.TopMargin = excel.Application.CentimetersToPoints(0.5)
    worksheet.PageSetup.BottomMargin = excel.Application.CentimetersToPoints(0.5)
    worksheet.PageSetup.LeftMargin = excel.Application.CentimetersToPoints(0)
    worksheet.PageSetup.RightMargin = excel.Application.CentimetersToPoints(0)

    workbook.PrintOut()
    # Close the workbook without saving
    workbook.Close(False)
    # Quit the Excel application
    excel.Quit()


if __name__ == '__main__':
    # Path to the Excel file
    _path = os.getcwd()
    _file = "test.xlsx"
    file_path = f"{_path}/{_file}"

    # Print the Excel file
    print_excel(file_path)
