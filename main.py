import cairosvg
import glob
import os
from tkinter import *
from PyPDF2 import PdfFileMerger
from tkinter import filedialog

folder_list = glob.glob("svg/*")
print(folder_list)
#def filter_file_list(file_list,files_path):


    # print(file_list)
        # print("loop")
        # print(file)
        # print(i)
        # print(new_svg_list)
        # if file[0] == str(i):
        #     print(file[0])
        #     print(file)
        #     print(file[0]==str(i))
        #     i += 1
        #     print(i)
        #     print(new_svg_list)
        #     new_svg_list.append(file)

def main():
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
            generatePDF(path_list, projekt)


def generatePDF(path_list,projekt):
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
    windowLog = Label(mainFrame, text=unique_filename, font=40)
    windowLog.pack()
    with open('pdf/out_' + unique_filename + '.pdf', 'wb') as fout:
        merger.write(fout)
    for proces in procesy:
        proces.close()


root = Tk()
root.title('svg2pdf')
root.geometry('300x250')
root.resizable(width=False, height=False)
def unpack():
    root.directory = filedialog.askdirectory()
    print(root.directory)
mainFrame = Frame(root)
mainFrame.place(relx="0.15",rely="0.15",relwidth="0.7",relheight="0.7")
mainBtn = Button(mainFrame, text="Konwertuj obrazki w PDF", command=main)

mainBtn.pack()
mainBtn["state"] = "disabled"
secBtn = Button(mainFrame, text="Gdzie masz zipy?", command=unpack)
secBtn.pack()

root.mainloop()




