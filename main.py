import cairosvg
import glob
import os
from tkinter import *
from PyPDF2 import PdfFileMerger
from tkinter import filedialog
from zipfile import ZipFile
import shutil

class svg2pdf():
    def main(self):
        folder_list = glob.glob("svg/*")
        print(folder_list)
        for folder in folder_list:
            projekt_list = glob.glob(folder+"/*")
            for projekt in projekt_list:
                file_list = []
                svg_list = []
                path_list = []
                # print(projekt)

                files_path = glob.glob(projekt+"/*")

                for file_path in files_path:
                    file = os.path.basename(file_path)
                    file_list.append(file)

                for index, file in enumerate(file_list):
                    print(file)
                    try:
                        if int(file[0]):
                            print("here")
                            svg_list.append(file)
                            path_list.append(files_path[index])

                    except ValueError:
                        pass
            if(path_list):
                self.generatePDF(path_list, projekt)

    def generatePDF(path_list, projekt,self):
        old_pdf_list = glob.glob("tmp/*.pdf")
        for i in old_pdf_list:
            os.remove(i)
        for index, svg_path in enumerate(path_list):
            print(svg_path)
            cairosvg.svg2pdf(url=svg_path, write_to='tmp/image' + str(index) + '.pdf')
        pdf_list = glob.glob("tmp/*.pdf")
        merger = PdfFileMerger()
        procesy = []
        for index, pdf in enumerate(pdf_list):
            procesy.append(open(pdf, "rb"))
            merger.append(procesy[index])

        unique_filename = projekt.replace("\\", "-")
        print()
        windowLog = Label(self.mainFrame, text=unique_filename, font=40)
        windowLog.pack()
        with open('pdf/out_' + unique_filename + '.pdf', 'wb') as fout:
            merger.write(fout)
        for proces in procesy:
            proces.close()

    def unpack(self):
        zipDirectories = filedialog.askopenfiles()
        print(zipDirectories)
        for zipDirectory in zipDirectories:
            zf = ZipFile(str(zipDirectory.name), 'r')
            zf.extractall('svg/')
            zf.close()

        #Rozpakować można na różne sposoby, później zastanowie się jaki jest najlepszy
        # with zipfile.ZipFile(zipDirectory, 'r') as zip_ref:
        #     zip_ref.extractall('/svg/')

        #shutil.unpack_archive(str(zipDirectory.name), '/svg/')

        # zf = ZipFile(str(zipDirectory.name), 'r')
        # zf.extractall('svg/')
        # zf.close()

    def gui(self):
        root = Tk()
        root.title('svg2pdf')
        root.geometry('300x250')
        root.resizable(width=False, height=False)
        mainFrame = Frame(root)
        mainFrame.place(relx="0.15", rely="0.15", relwidth="0.7", relheight="0.7")
        mainBtn = Button(mainFrame, text="Konwertuj obrazki w PDF", command=self.main)
        mainBtn.pack()
        mainBtn["state"] = "disabled"
        secBtn = Button(mainFrame, text="Gdzie masz zipy?", command=self.unpack)
        secBtn.pack()
        root.mainloop()

a = svg2pdf()
a.gui()



