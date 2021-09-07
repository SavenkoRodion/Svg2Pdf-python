import cairosvg,glob,os,shutil,time,threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from tkinter import *
from PyPDF2 import PdfFileMerger
from tkinter import filedialog
from zipfile import ZipFile
import urllib.request

# Rozpakować można na różne sposoby, później zastanowie się jaki jest najlepszy

# with zipfile.ZipFile(zipDirectory, 'r') as zip_ref:
#     zip_ref.extractall('/svg/')

# shutil.unpack_archive(str(zipDirectory.name), '/svg/')

# zf = ZipFile(str(zipDirectory.name), 'r')
# zf.extractall('svg/')
# zf.close()


class AutoDownload:
    def main(self):
        shutil.rmtree("zip")
        os.mkdir("zip", mode=0o777)

        print("start test")
        downloadLinks = []

        driverPath = "chromedriver-93.exe"
        zipFolderPath = os.getcwd() + "\zip"
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': zipFolderPath}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(driverPath, options=chrome_options)

        driver.get("http://veraprinteu:81/admin/")
        login = driver.find_element_by_id("signin_username")
        login.send_keys("rodion.savenko@veraprint.pl")
        password = driver.find_element_by_id("signin_password")
        password.send_keys("Rodion123456")
        password.send_keys(Keys.RETURN)

        try:
            btnToDo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "TO DO"))
            )
            btnToDo.click()
            time.sleep(3)
            tableToDo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "indexform"))
            )
            zamowieniaToDo = tableToDo.find_elements_by_tag_name("tr")
            # testTrs = testAnother[0].find_elements_by_tag_name("tr")
            for zamowienie in zamowieniaToDo:
                zamowienieId = zamowienie.get_attribute('id')
                if "zamowienie" in zamowienieId:
                    zamowienieNumer = zamowienieId.replace('zamowienie_', '')
                    # driver.execute_script("window.open('about:blank','secondtab');")
                    # driver.switch_to.window("secondtab")
                    downloadLinks.append('http://veraprinteu:81/admin/index.php/zamowienia/download/id/' +
                                         zamowienieNumer)
                    # time.sleep(3)
                    # with urllib.request.urlopen('http://veraprinteu:81/admin/index.php/zamowienia/download/id/'+testWynnik) as f:
                    #     html = f.read().decode('utf-8')
                else:
                    print("nie to")

            print(downloadLinks)
            for downloadLink in downloadLinks:
                driver.execute_script("window.open('about:blank','secondtab');")
                driver.switch_to.window("secondtab")
                driver.get(downloadLink)
                time.sleep(1)

        except:
            driver.close()

        time.sleep(3)
        driver.quit()
        print()
        unpack().getDownloadedZip()

class unpack():
    def start(self):
        self.zipPaths = []
        shutil.rmtree("svg")
        os.mkdir("svg", mode=0o777)

    def getDownloadedZip(self):
        self.start()
        zipDirectory = os.getcwd() + "\zip"  # filedialog.askopenfiles()
        for root, dirs, files in os.walk(zipDirectory):
            for file in files:
                self.zipPaths.append(os.path.join(root, file))
        self.main()

    def getLocalZip(self):
        self.start()
        zipDirObjects = filedialog.askopenfiles()
        for zipDirObject in zipDirObjects:
            self.zipPaths.append(zipDirObject.name)
        print(self.zipPaths)
        self.main()

    def main(self):
        for zipPath in self.zipPaths:
            zf = ZipFile(str(zipPath), 'r')
            zf.extractall('svg/')
            zf.close()
        self.gui()
    def gui(self):
        # projectCountText = "Wybrano "+str(len(self.zipPaths))+" projektów"
        # self.projectCount = Label(mainFrame, text=projectCountText, font="10px")
        # self.projectCount.pack()
        statusChange().convert()

class svg2pdf():
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
        reset().main()

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
        windowLog = Label(mainFrame, text=unique_filename, font="10px")
        windowLog.pack()
        with open('pdf/out_' + unique_filename + '.pdf', 'wb') as fout:
            merger.write(fout)
        for proces in procesy:
            proces.close()


class reset():
    def main(self):
        shutil.rmtree("svg")
        os.mkdir("svg", mode=0o777)
        shutil.rmtree("tmp")
        os.mkdir("tmp", mode=0o777)
        shutil.rmtree("zip")
        os.mkdir("zip", mode=0o777)
        statusChange().unpack()
        print("refreshed")


class statusChange():
    def unpack(self):
        mainBtn["state"] = "disabled"
        resetBtn["state"] = "disabled"
        seleniumBtn["state"] = "active"
        zipBtn["state"] = "active"
    def convert(self):
        mainBtn["state"] = "active"
        resetBtn["state"] = "active"
        seleniumBtn["state"] = "disabled"
        zipBtn["state"] = "disabled"


root = Tk()
root.title('svg2pdf')
root.geometry('400x400')
root.resizable(width=False, height=False)
mainFrame = Frame(root)
mainFrame.place(relx="0.15", rely="0.15", relwidth="0.7", relheight="0.7")
mainBtn = Button(mainFrame, text="Konwertuj obrazki w PDF", command=lambda:threading.Thread(target=svg2pdf().main).start())
mainBtn.pack()
seleniumBtn = Button(mainFrame, text="Automatycznie pobierz projekty z filtru 'TO DO'",
                     command=lambda:threading.Thread(target=AutoDownload().main).start())
seleniumBtn.pack()
mainBtn["state"] = "disabled"
zipBtn = Button(mainFrame, text="Znajdź zipy na swoim komputerze", command=lambda:threading.Thread(target=unpack().getLocalZip).start())
zipBtn.pack()
resetBtn = Button(mainFrame, text="Zresetuj wybrane zamowienia", command=lambda:threading.Thread(target=reset().main).start())
resetBtn.pack()
resetBtn["state"] = "disabled"
root.mainloop()




