import cairosvg
import glob
import os
from tkinter import *
from PyPDF2 import PdfFileMerger
from tkinter import filedialog
from zipfile import ZipFile
import shutil

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

import time
# Rozpakować można na różne sposoby, później zastanowie się jaki jest najlepszy

# with zipfile.ZipFile(zipDirectory, 'r') as zip_ref:
#     zip_ref.extractall('/svg/')

# shutil.unpack_archive(str(zipDirectory.name), '/svg/')

# zf = ZipFile(str(zipDirectory.name), 'r')
# zf.extractall('svg/')
# zf.close()


class svg2pdf():
    def gui(self):
        root = Tk()
        root.title('svg2pdf')
        root.geometry('300x250')
        root.resizable(width=False, height=False)
        self.mainFrame = Frame(root)
        self.mainFrame.place(relx="0.15", rely="0.15", relwidth="0.7", relheight="0.7")
        self.mainBtn = Button(self.mainFrame, text="Konwertuj obrazki w PDF", command=self.main)
        self.mainBtn.pack()
        self.testBtn = Button(self.mainFrame, text="Test", command=self.test_selenium)
        self.testBtn.pack()
        self.mainBtn["state"] = "disabled"
        ZipBtn = Button(self.mainFrame, text="Gdzie masz zipy?", command=self.unpack)
        ZipBtn.pack()
        root.mainloop()

    def unpack(self):
        #self.removeOldFiles("svg/*")
        shutil.rmtree("svg")
        os.mkdir("svg", mode=0o777)
        zipDirectories = filedialog.askopenfiles()
        for zipDirectory in zipDirectories:
            zf = ZipFile(str(zipDirectory.name), 'r')
            zf.extractall('svg/')
            zf.close()
        self.mainBtn["state"] = "active"

    def main(self):
        folder_list = glob.glob("svg/*")
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
                    try:
                        if int(file[0]):
                            svg_list.append(file)
                            path_list.append(files_path[index])

                    except ValueError:
                        pass

                if(path_list):
                    self.generatePDF(path_list, projekt)

    def generatePDF(self,path_list, projekt):
        print("generate")
        old_pdf_list = glob.glob("tmp/*.pdf")
        for i in old_pdf_list:
            print(i)
            os.remove(i)

        for index, svg_path in enumerate(path_list):
            cairosvg.svg2pdf(url=svg_path, write_to='tmp/image' + str(index) + '.pdf', dpi=72)
        pdf_list = glob.glob("tmp/*")
        merger = PdfFileMerger()
        procesy = []
        for index, pdf in enumerate(pdf_list):
            print(pdf_list)
            procesy.append(open(pdf, "rb"))
            merger.append(procesy[index])

        unique_filename = projekt.replace("\\", "-")
        windowLog = Label(self.mainFrame, text=unique_filename, font="10px")
        windowLog.pack()
        with open('pdf/out_' + unique_filename + '.pdf', 'wb') as fout:
            merger.write(fout)
        for proces in procesy:
            proces.close()
    def test_selenium(self):
        print("start test")
        PATH = "C:/Users/Saven/Desktop/chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        driver.get("http://veraprinteu:81/admin/")
        login = driver.find_element_by_id("signin_username")
        login.send_keys("rodion.savenko@veraprint.pl")
        password = driver.find_element_by_id("signin_password")
        password.send_keys("Rodion123456")
        password.send_keys(Keys.RETURN)

        try:
            testLol = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "structFilter"))
            )
            print(testLol)
        except:
            driver.close()

        time.sleep(5)
        driver.close()


svg2pdf().gui()



