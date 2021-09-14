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
    def main(self,download_type,*ids):
        shutil.rmtree("zip")
        os.mkdir("zip", mode=0o777)

        path_driver = "chromedriver-93.exe"
        path_zip_folder = os.getcwd() + "\\zip"
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': path_zip_folder}
        chrome_options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(path_driver, options=chrome_options)

        self.driver.get("http://veraprint.eu/admin/")
        login = self.driver.find_element_by_id("signin_username")
        login.send_keys("rodion.savenko@veraprint.pl")
        password = self.driver.find_element_by_id("signin_password")
        password.send_keys("Rodion123456")
        password.send_keys(Keys.RETURN)
        self.download_links = []
        if download_type == "direct":
            self.create_download_links(ids)
        elif download_type == "to_do":
            self.get_zamowienia()
    def get_zamowienia(self):
        try:
            to_do_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "TO DO"))
            )
            to_do_btn.click()
            time.sleep(3)
            to_do_table = WebDriverWait(self.driver, 10).until(
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
                    self.download_links.append(
                        'http://veraprint.eu/admin/index.php/zamowienia/download/id/' + zamowienie_numer)
                    # time.sleep(3)
                    # with urllib.request.urlopen('http://veraprinteu:81
                    # /admin/index.php/zamowienia/download/id/'+testWynnik) as f:
                    #     html = f.read().decode('utf-8')
                else:
                    print("nie to")

            print(self.download_links)
            self.download()

        except:
            self.driver.close()

    def create_download_links(self, *ids):
        for id in ids[0][0]:
            print(id)
            self.download_links.append(
                'http://veraprint.eu/admin/index.php/zamowienia/download/id/' + id)
        print(self.download_links)
        self.download()
    def download(self):
        for download_link in self.download_links:
            self.driver.execute_script("window.open('about:blank','secondtab');")
            self.driver.switch_to.window("secondtab")
            self.driver.get(download_link)
            time.sleep(1)
        time.sleep(3)
        self.driver.quit()
        StatusChange().convert()

class Unpack:
    def start(self):
        self.zip_paths = []
        shutil.rmtree("svg")
        os.mkdir("svg", mode=0o777)

    def get_downloaded_zip(self):
        self.start()
        zip_directory = os.getcwd() + "\\zip"  # filedialog.askopenfiles()
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
                    self.generate_pdf(list_path, projekt)
        Reset().main()

    def generate_pdf(self, list_path, projekt):
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


class StatusChange:
    def unpack(self):
        mainBtn["state"] = "disabled"
        resetBtn["state"] = "disabled"
        seleniumBtn["state"] = "active"
        zipBtn["state"] = "active"
        newWindowBtn["state"] = "active"

    def convert(self):
        mainBtn["state"] = "active"
        resetBtn["state"] = "active"
        seleniumBtn["state"] = "disabled"
        zipBtn["state"] = "disabled"
        newWindowBtn["state"] = "disabled"

class TestWindow:
    def main(self):
        self.test_number = 1
        root.withdraw()
        self.new_window = Toplevel(root)
        self.new_window.title("New Window")
        self.new_window.geometry("400x400")
        self.new_frame = Frame(self.new_window)
        self.new_frame.place(relx="0.15", rely="0.15", relwidth="0.7", relheight="0.7")
        self.test_entry = Entry(self.new_frame)
        self.test_entry.pack()
        btn_confirm = Button(
            self.new_frame, text="Podtwierdz", command=self.add_value)
        btn_confirm.pack()
        anotherBtn = Button(
            self.new_frame, text="Pobierz wybrane zamowienia", command=lambda: threading.Thread(target=self.another).start())
        anotherBtn.pack()
        backBtn = Button(
            self.new_frame, text="Wróć", command=self.destroy)
        backBtn.pack()

    def add_value(self):
        test_entry1 =Entry(self.new_frame)
        test_entry1.insert(0,self.test_entry.get())
        test_entry1['state'] = 'disable'
        test_entry1.pack()
        print("which one?")
        self.test_number+=1
        print(self.test_number)

        btn_remove = Button(
            self.new_frame, text="X", command=lambda btn_id=self.test_number: self.remove(btn_id))
        btn_remove.pack()


    def remove(self,btn_id):
        print(btn_id)
        for child in self.new_frame.winfo_children():
            print(child.winfo_name())
            if child.winfo_name() == "!entry"+str(btn_id):
                child.destroy()
            elif child.winfo_name() == "!button"+str(btn_id+2):
                child.destroy()

    def destroy(self):
        root.deiconify()
        self.new_window.destroy()
    def another(self):
        temp_arr = []
        print(self.test_entry.get())
        for child in self.new_frame.winfo_children():
            if child['state'] == "disabled":
                temp_arr.append(child.get())
        self.destroy()
        AutoDownload().main("direct",temp_arr)


root = Tk()
root.title('svg2pdf')
root.geometry('400x400')
root.resizable(width=False, height=False)
mainFrame = Frame(root)
mainFrame.place(relx="0.15", rely="0.15", relwidth="0.7", relheight="0.7")
mainBtn = Button(mainFrame, text="Konwertuj obrazki w PDF", command=lambda: threading.Thread(target=SVG2PDF().main).start())
mainBtn.pack()
seleniumBtn = Button(mainFrame, text="Automatycznie pobierz projekty z filtru 'TO DO'",
                     command=lambda: threading.Thread(target=AutoDownload().main("to_do")).start())
seleniumBtn.pack()
mainBtn["state"] = "disabled"
newWindowBtn = Button(
    mainFrame, text="Pobierz zamówienia wprowadzając id", command=TestWindow().main)
newWindowBtn.pack()
zipBtn = Button(mainFrame, text="Znajdź zipy na swoim komputerze",
                command=Unpack().get_local_zip)
zipBtn.pack()
resetBtn = Button(mainFrame, text="Zresetuj wybrane zamowienia",
                  command=Reset().main)
resetBtn.pack()
resetBtn["state"] = "disabled"
root.mainloop()




