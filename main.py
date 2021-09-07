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

        download_links = []

        path_driver = "chromedriver-93.exe"
        path_zip_folder = os.getcwd() + "\zip"
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': path_zip_folder}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(path_driver, options=chrome_options)

        driver.get("http://veraprinteu:81/admin/")
        login = driver.find_element_by_id("signin_username")
        login.send_keys("rodion.savenko@veraprint.pl")
        password = driver.find_element_by_id("signin_password")
        password.send_keys("Rodion123456")
        password.send_keys(Keys.RETURN)

        try:
            to_do_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "TO DO"))
            )
            to_do_btn.click()
            time.sleep(3)
            to_do_table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "indexform"))
            )
            to_do_zamowienia = to_do_table.find_elements_by_tag_name("tr")
            # testTrs = testAnother[0].find_elements_by_tag_name("tr")
            for zamowienie in to_do_zamowienia:
                id_zamowienie = zamowienie.get_attribute('id')
                if "zamowienie" in id_zamowienie:
                    zamowienie_numer = id_zamowienie.replace('zamowienie_', '')
                    # driver.execute_script("window.open('about:blank','secondtab');")
                    # driver.switch_to.window("secondtab")
                    download_links.append('http://veraprinteu:81/admin/index.php/zamowienia/download/id/' +
                                         zamowienie_numer)
                    # time.sleep(3)
                    # with urllib.request.urlopen('http://veraprinteu:81/admin/index.php/zamowienia/download/id/'+testWynnik) as f:
                    #     html = f.read().decode('utf-8')
                else:
                    print("nie to")

            print(download_links)
            for download_link in download_links:
                driver.execute_script("window.open('about:blank','secondtab');")
                driver.switch_to.window("secondtab")
                driver.get(download_link)
                time.sleep(1)

        except:
            driver.close()

        time.sleep(3)
        driver.quit()
        Unpack().get_downloaded_zip()


class Unpack:
    def start(self):
        self.zip_paths = []
        shutil.rmtree("svg")
        os.mkdir("svg", mode=0o777)

    def get_downloaded_zip(self):
        self.start()
        zip_directory = os.getcwd() + "\zip"  # filedialog.askopenfiles()
        for root, dirs, files in os.walk(zip_directory):
            for file in files:
                self.zip_paths.append(os.path.join(root, file))
        self.main()

    def get_local_zip(self):
        self.start()
        zip_dir_objects = filedialog.askopenfiles()
        for zip_dir_object in zip_dir_objects:
            self.zip_paths.append(zip_dir_object.name)
        print(self.zip_paths)
        self.main()

    def main(self):
        for zip_path in self.zip_paths:
            zf = ZipFile(str(zip_path), 'r')
            zf.extractall('svg/')
            zf.close()
        self.gui()

    def gui(self):
        # projectCountText = "Wybrano "+str(len(self.zip_paths))+" projektów"
        # self.projectCount = Label(mainFrame, text=projectCountText, font="10px")
        # self.projectCount.pack()
        StatusChange().convert()


class SVG2PDF:
    def main(self):
        list_folder = glob.glob("svg/*")
        for folder in list_folder:
            list_projekt = glob.glob(folder+"/*")
            for projekt in list_projekt:
                list_file = []
                list_svg = []
                list_path = []
                # print(projekt)

                path_files = glob.glob(projekt+"/*")

                for path_file in path_files:
                    file = os.path.basename(path_file)
                    list_file.append(file)

                for index, file in enumerate(list_file):
                    try:
                        if int(file[0]):
                            list_svg.append(file)
                            list_path.append(path_files[index])

                    except ValueError:
                        pass

                if list_path:
                    self.GeneratePDF(list_path, projekt)
        Reset().main()

    def GeneratePDF(self, list_path, projekt):
        print("generate")
        list_old_pdf = glob.glob("tmp/*.pdf")
        for i in list_old_pdf:
            print(i)
            os.remove(i)

        for index, svg_path in enumerate(list_path):
            cairosvg.svg2pdf(url=svg_path, write_to='tmp/image' + str(index) + '.pdf', dpi=72)
        list_pdf = glob.glob("tmp/*")
        merger = PdfFileMerger()
        procesy = []
        for index, pdf in enumerate(list_pdf):
            print(list_pdf)
            procesy.append(open(pdf, "rb"))
            merger.append(procesy[index])

        unique_filename = projekt.replace("\\", "-")
        window_log = Label(mainFrame, text=unique_filename, font="10px")
        window_log.pack()
        with open('pdf/out_' + unique_filename + '.pdf', 'wb') as fout:
            merger.write(fout)
        for proces in procesy:
            proces.close()


class Reset:
    def main(self):
        shutil.rmtree("svg")
        os.mkdir("svg", mode=0o777)
        shutil.rmtree("tmp")
        os.mkdir("tmp", mode=0o777)
        shutil.rmtree("zip")
        os.mkdir("zip", mode=0o777)
        StatusChange().unpack()
        print("refreshed")


class StatusChange():
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
mainBtn = Button(mainFrame, text="Konwertuj obrazki w PDF", command=lambda:threading.Thread(target=SVG2PDF().main).start())
mainBtn.pack()
seleniumBtn = Button(mainFrame, text="Automatycznie pobierz projekty z filtru 'TO DO'",
                     command=lambda: threading.Thread(target=AutoDownload().main).start())
seleniumBtn.pack()
mainBtn["state"] = "disabled"
zipBtn = Button(mainFrame, text="Znajdź zipy na swoim komputerze",
                command=lambda: threading.Thread(target=Unpack().get_local_zip()).start())
zipBtn.pack()
resetBtn = Button(mainFrame, text="Zresetuj wybrane zamowienia",
                  command=lambda: threading.Thread(target=Reset().main).start())
resetBtn.pack()
resetBtn["state"] = "disabled"
root.mainloop()




