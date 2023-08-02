import json
import os
import random
import sys
import time
import webbrowser
from tkinter import filedialog

import git
import qdarktheme
import pyjokes
from PyQt6.Qsci import QsciScintilla, QsciAPIs
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QActionGroup, QFileSystemModel, QPixmap, QIcon, QFontMetrics
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QDockWidget, QTreeView, QFileDialog, QSplashScreen, \
    QMessageBox, QMenu, QPlainTextEdit, QPushButton, QWidget, QVBoxLayout, QTextEdit

import Lexers
import datetime
import config_page
from Core import MenuConfig, terminal, WelcomeScreen
import Modules as ModuleFile
from Core.TabWidget import TabWidget
import threading

#######
########


path_file = open("Data/CPath_Project.txt", 'r+')
cpath = path_file.read()

with open("Data/config.json", "r") as json_file:
    json_data = json.load(json_file)

editor_bg = str(json_data["editor_theme"])
margin_bg = str(json_data["margin_theme"])
linenumber_bg = str(json_data["lines_theme"])
margin_fg = str(json_data["margin_fg"])
editor_fg = str(json_data["editor_fg"])
linenumber_fg = str(json_data["lines_fg"])
sidebar_bg = str(json_data["sidebar_bg"])
font = str(json_data["font"])
theme_color = str(json_data["theme"])
theme = str(json_data["theme_type"])

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__(parent=None)
        lexer = Lexers.PythonLexer()
        self.setLexer(lexer)
        self.setPaper(QColor(editor_bg))

        # Autocompletion
        apis = QsciAPIs(self.lexer())
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(True)
        self.setWrapMode(QsciScintilla.WrapMode.WrapNone)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionFillupsEnabled(True)


        # Setting up lexers
        lexer.setPaper(QColor(editor_bg))
        lexer.setColor(QColor('#808080'), lexer.Comment)
        lexer.setColor(QColor('#FFA500'), lexer.Keyword)
        lexer.setColor(QColor('#FFFFFF'), lexer.ClassName)
        lexer.setColor(QColor("#59ff00"), lexer.TripleSingleQuotedString)
        lexer.setColor(QColor("#59ff00"), lexer.TripleDoubleQuotedString)
        lexer.setColor(QColor("#3ba800"), lexer.SingleQuotedString)
        lexer.setColor(QColor("#3ba800"), lexer.DoubleQuotedString)
        lexer.setColor(QColor(editor_fg), lexer.Default)
        lexer.setFont(QFont(font))

        self.setTabWidth(4)
        self.setMarginLineNumbers(1, True)
        self.setAutoIndent(True)
        self.setMarginWidth(1, "#0000")
        left_margin_index = 0
        left_margin_width = 7
        self.setMarginsForegroundColor(QColor(linenumber_fg))
        self.setMarginsBackgroundColor(QColor(linenumber_bg))
        font_metrics = QFontMetrics(self.font())
        left_margin_width_pixels = font_metrics.horizontalAdvance(' ') * left_margin_width
        self.SendScintilla(self.SCI_SETMARGINLEFT, left_margin_index, left_margin_width_pixels)
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)
        self.setMarginSensitivity(2, True)
        self.setFoldMarginColors(QColor(margin_bg), QColor(margin_bg))
        self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#80d3d3d3"))
        self.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        self.setAutoCompletionThreshold(1)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)

        self.context_menu = QMenu(self)
        encrypt_menu = QMenu("Encryption", self.context_menu)
        self.context_menu.addAction("Cut        ").triggered.connect(self.cut)
        self.context_menu.addAction("Copy").triggered.connect(self.copy)
        self.context_menu.addAction("Paste").triggered.connect(self.paste)
        self.context_menu.addAction("Select All").triggered.connect(self.selectAll)
        self.context_menu.addSeparator()
        encrypt_menu.addAction("Encrypt Selection", self.encode)
        encrypt_menu.addAction("Decrypt Selection", self.decode)
        self.context_menu.addAction("Calculate", self.calculate)
        self.context_menu.addMenu(encrypt_menu)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, point):
        self.context_menu.popup(self.mapToGlobal(point))

    def calculate(self):
        ModuleFile.calculate(self)

    def encode(self):
        ModuleFile.encypt(self)

    def decode(self):
        ModuleFile.decode(self)

class Sidebar(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setFixedWidth(70)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

# noinspection PyUnresolvedReferences
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Splash Screen
        splash_pix = ""
        current_time = datetime.datetime.now().time()
        sunrise_time = current_time.replace(hour=6, minute=0, second=0, microsecond=0)
        sunset_time = current_time.replace(hour=18, minute=0, second=0, microsecond=0)

        # Check which time interval the current time falls into
        if sunrise_time <= current_time < sunrise_time.replace(hour=12):
            splash_pix = QPixmap("Core/Icons/splash_morning.png")
        elif sunrise_time.replace(hour=12) <= current_time < sunset_time:
            splash_pix = QPixmap("Core/Icons/splash_afternoon.png")
        else:
            splash_pix = QPixmap("Core/Icons/splash_night.png")

        splash = QSplashScreen(splash_pix)
        splash.show()
        time.sleep(1)
        splash.hide()

        self.tab_widget = TabWidget()
        self.current_editor = ""

        if cpath == "" or cpath == " ":
            welcome_widget = WelcomeScreen.WelcomeWidget(self)
            self.tab_widget.addTab(welcome_widget, "Welcome")
        else:
            self.treeview_viewmenu()

        self.tab_widget.setTabsClosable(True)

        self.md_dock = QDockWidget("Markdown Preview")
        self.mdnew = QDockWidget("Markdown Preview")

        # Sidebar
        self.sidebar_main = Sidebar("", self)
        self.sidebar_main.setTitleBarWidget(QWidget())
        self.sidebar_widget = QWidget(self.sidebar_main)
        self.sidebar_widget.setStyleSheet("""QWidget{background-color : #313335;}""")
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_main.setWidget(self.sidebar_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar_main)

        self.statusbar = Sidebar("", self)
        self.statusbar.setTitleBarWidget(QWidget())
        self.terminal_button = QPushButton(self.statusbar)
        self.statusbar_widget = QWidget(self.statusbar)
        self.statusbar_widget.setStyleSheet("""QWidget{background-color : #313335;}""")
        self.statusbar_layout = QVBoxLayout(self.statusbar_widget)
        self.statusbar_layout.addStretch()
        self.statusbar_layout.addWidget(self.terminal_button)
        self.statusbar_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.statusbar.setWidget(self.statusbar_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.statusbar)

        terminal_icon = QIcon('Core/Icons/terminal.png')
        self.terminal_button.setIcon(terminal_icon)
        self.terminal_button.setIconSize(QSize(20, 20))
        self.terminal_button.setFixedSize(30, 30)

        explorer_icon = QIcon('Core/Icons/explorer.png')
        self.explorer_button = QPushButton(self)
        self.explorer_button.setIcon(explorer_icon)
        self.explorer_button.setIconSize(QSize(30, 30))
        self.explorer_button.setFixedSize(50, 50)
        self.explorer_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius:10;
                align: botton;
            }
            QPushButton:hover {
                background-color: #3574f0;
            }
            """
        )

        settings_icon = QIcon('Core/Icons/settings.png')
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(settings_icon)
        self.settings_button.setIconSize(QSize(30, 30))
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius:10;
                align: botton;
            }
            QPushButton:hover {
                background-color: #3574f0;
            }
            """
        )

        self.sidebar_layout.insertWidget(0, self.explorer_button)
        self.statusbar_layout.insertWidget(2, self.settings_button)

        self.sidebar_layout.addStretch()
        self.statusbar_layout.addStretch()

        # Connect the button's clicked signal to the slot
        self.explorer_button.clicked.connect(self.expandSidebar__Explorer)
        self.terminal_button.clicked.connect(self.terminal_widget)
        self.settings_button.clicked.connect(self.expandSidebar__Settings)

        self.setCentralWidget(self.tab_widget)
        self.editors = []

        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        self.tab_widget.setStyleSheet("QTabWidget {border: none;}")

        self.tab_widget.currentChanged.connect(self.change_text_editor)
        self.tab_widget.tabCloseRequested.connect(self.remove_editor)
        #self.new_document()
        self.setWindowTitle('Aura Text')
        self.setWindowIcon(QIcon("Core/Icons/icon.ico"))
        self.configure_menuBar()
        self.showMaximized()

    def create_editor(self):
        self.text_editor = CodeEditor()
        return self.text_editor

    def onDockWidgetVisibilityChanged(self, visible, button):
        if visible:
            button.setStyleSheet(
                """
                QPushButton {
                    border: none;
                    border-radius:10;
                    background-color : #3574f0;
                }
                QPushButton:hover {
                    background-color: #3574f0;
                }
                """)
        else:
            button.setStyleSheet(
                """
                QPushButton {
                    border: none;
                    border-radius:10;
                }
                QPushButton:hover {
                    background-color: #3574f0;
                }
                """
            )

    def expandSidebar__Explorer(self):
        self.treeview_viewmenu()

    def create_snippet(self):
        ModuleFile.CodeSnippets.snippets_gen(self.current_editor)

    def import_snippet(self):
        ModuleFile.CodeSnippets.snippets_open(self.current_editor)

    def expandSidebar__Settings(self):
        self.settings_dock = QDockWidget("Settings", self)
        background_color = self.settings_button.palette().color(self.settings_button.backgroundRole()).name()
        if background_color == "#000000":
            self.settings_dock.destroy()
        else:
            self.settings_dock.visibilityChanged.connect(lambda visible: self.onDockWidgetVisibilityChanged(visible, self.settings_button))
            self.settings_dock.setStyleSheet("QDockWidget {background-color : #1b1b1b; color : white;}")
            self.settings_dock.setFixedWidth(200)
            self.settings_widget = config_page.ConfigPage()
            self.settings_layout = QVBoxLayout(self.settings_widget)
            self.settings_layout.addWidget(self.settings_widget)
            self.settings_dock.setWidget(self.settings_widget)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.settings_dock)

    def treeview_viewmenu(self):
        self.treeview_project(cpath)

    def new_project(self):
        new_folder_path = filedialog.askdirectory(title="Create New Folder", initialdir="./",
                                                  mustexist=False)
        with open('Data/CPath_Project.txt', 'w') as file:
            file.write(new_folder_path)

    def code_jokes(self):
        a =  pyjokes.get_joke(language='en', category='neutral')
        QMessageBox.information(self, "A Byte of Humour!", a)

    def treeview_project(self, path):
        dock = QDockWidget("Explorer", self)
        dock.visibilityChanged.connect(lambda visible: self.onDockWidgetVisibilityChanged(visible, self.explorer_button))
        dock.setStyleSheet("QDockWidget { background-color: #191a1b; color: white;}")
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        tree_view = QTreeView()
        self.model = QFileSystemModel()
        tree_view.setStyleSheet("QTreeView { background-color: #191a1b; color: white; border: none; }")
        tree_view.setModel(self.model)
        tree_view.setRootIndex(self.model.index(path))
        self.model.setRootPath(path)
        dock.setWidget(tree_view)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        tree_view.doubleClicked.connect(self.open_file)

    def terminal_widget(self):
        self.terminal_dock = QDockWidget("Terminal", self)
        self.terminal_dock.visibilityChanged.connect(lambda visible: self.onDockWidgetVisibilityChanged(visible, self.terminal_button))
        terminal_widget = terminal.AuraTextTerminalWidget()
        self.sidebar_layout_Terminal = QVBoxLayout(terminal_widget)
        self.terminal_dock.setWidget(terminal_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Save File',
            random.choice(
                ModuleFile.emsg_save_list),
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save)
        if reply == QMessageBox.StandardButton.Save:
            self.save_document()
            event.accept()
        elif reply == QMessageBox.StandardButton.Discard:
            event.accept()
        else:
            event.ignore()

    def gitClone(self):
        try:
            from git import Repo
            repo_url, ok = QInputDialog.getText(self, "Git Repo", "URL of the Repository")
            try:
                path = filedialog.askdirectory(title="Repo Path", initialdir="./",
                                                          mustexist=False)
            except:
                messagebox = QMessageBox()
                messagebox.setWindowTitle("Path Error"), messagebox.setText(
                    "The folder should be EMPTY! Please try again with an EMPTY folder")
                messagebox.exec()

            try:
                Repo.clone_from(repo_url, path)
                with open('Data/CPath_Project.txt', 'w') as file:
                    file.write(path)
                messagebox = QMessageBox()
                messagebox.setWindowTitle("Success!"), messagebox.setText(
                    "The repository has been cloned successfully!")
                messagebox.exec()
                self.treeview_project(path)
            except git.GitCommandError:
                pass

        except ImportError:
            messagebox = QMessageBox()
            messagebox.setWindowTitle("Git Import Error"), messagebox.setText("Aura Text can't find Git in your PC. Make sure Git is installed and has been added to PATH.")
            messagebox.exec()

    def markdown_open(self, path_data):
        #self.md_dock = QDockWidget("Markdown Preview")
        self.md_dock.setStyleSheet("QDockWidget {background-color : #1b1b1b; color : white;}")
        self.md_dock.setMinimumWidth(400)
        self.md_widget = QTextEdit()
        self.md_widget.setMarkdown(path_data)
        self.md_widget.setReadOnly(True)
        self.md_layout = QVBoxLayout(self.md_widget)
        self.md_layout.addWidget(self.md_widget)
        self.md_dock.setWidget(self.md_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.md_dock)

    def markdown_new(self):
        self.mdnew.setStyleSheet("QDockWidget {background-color : #1b1b1b; color : white;}")
        self.mdnew.setMinimumWidth(400)
        self.md_widget = QTextEdit()
        self.md_widget.setReadOnly(True)
        self.md_layout = QVBoxLayout(self.md_widget)
        self.md_layout.addWidget(self.md_widget)
        self.mdnew.setWidget(self.md_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.mdnew)

        def update():
            a = self.current_editor.text()
            self.md_widget.setMarkdown(a)

        self.current_editor.textChanged.connect(update)

    # TREEVIEW
    def open_file(self, index):
        path = self.model.filePath(index)
        image_extensions = ["png", "jpg", "jpeg", "ico", "gif", "bmp"]
        ext = path.split(".")[-1]

        def add_image_tab():
            ModuleFile.add_image_tab(self, self.tab_widget, path, os.path.basename(path))

        if path:

            try:
                if ext in image_extensions:
                    add_image_tab()
                    return

            except UnicodeDecodeError:
                messagebox = QMessageBox()
                messagebox.setWindowTitle("Wrong Filetype!"), messagebox.setText("This file type is not supported!")
                messagebox.exec()

            try:
                f = open(path, "r")
                try:
                    filedata = f.read()
                    if ext == "md" or ext == "MD":
                        self.markdown_open(filedata)
                    elif ext == "png" or ext == "PNG":
                        add_image_tab()
                    self.new_document(title=os.path.basename(path))
                    self.current_editor.insert(filedata)
                    f.close()
                except UnicodeDecodeError:
                    messagebox = QMessageBox()
                    messagebox.setWindowTitle("Wrong Filetype!"), messagebox.setText("This file type is not supported!")
                    messagebox.exec()
            except FileNotFoundError:
                return

    def speak_init(self):
        text = self.current_editor.text()
        ModuleFile.rightSpeak(text)

    def speak(self):
        speak_thread = threading.Thread(target=self.speak_init)
        speak_thread.start()

    def check_for_issues(self):
        ModuleFile.check_for_issues()

    def configure_menuBar(self):
        MenuConfig.configure_menuBar(self)

    def python(self):
        Lexers.python(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def csharp(self):
        Lexers.csharp(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def json(self):
        Lexers.json(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def duplicate_line(self):
        ModuleFile.duplicate_line(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def yaml(self):
        Lexers.yaml(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def xml(self):
        Lexers.xml(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def html(self):
        Lexers.html(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def cpp(self):
        Lexers.cpp(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def ruby(self):
        Lexers.ruby(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def perl(self):
        Lexers.perl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def pascal(self):
        Lexers.pascal(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def css(self):
        Lexers.css(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def sql(self):
        Lexers.sql(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def lua(self):
        Lexers.lua(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def cmake(self):
        Lexers.cmake(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def postscript(self):
        Lexers.postscript(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def asm(self):
        Lexers.asm(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def avs(self):
        Lexers.avs(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def coffeescript(self):
        Lexers.coffeescript(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def batch(self):
        Lexers.bat(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def bash(self):
        Lexers.bash(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def srec(self):
        Lexers.srec(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def idl(self):
        Lexers.idl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def matlab(self):
        Lexers.matlab(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def tcl(self):
        Lexers.tcl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def verilog(self):
        Lexers.verilog(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def spice(self):
        Lexers.spice(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def vhdl(self):
        Lexers.vhdl(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def octave(self):
        Lexers.octave(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def fortran77(self):
        Lexers.fortran77(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def tex(self):
        Lexers.tex(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def makefile(self):
        Lexers.makefile(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def markdown(self):
        Lexers.markdown(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def js(self):
        Lexers.js(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def fortran(self):
        Lexers.fortran(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def java(self):
        Lexers.java(self)
        self.current_editor.setMarginsBackgroundColor(QColor(margin_bg))
        self.current_editor.setMarginsForegroundColor(QColor("#FFFFFF"))

    def pastebin(self):
        ModuleFile.pastebin(self)

    def code_formatting(self):
        ModuleFile.code_formatting(self)

    def goto_line(self):
        line_number, ok = QInputDialog.getInt(self, "Goto Line", "Line:")
        if ok:
            self.setCursorPosition(line_number - 1, 0)

    def open_project(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        if dialog.exec():
            project_path = dialog.selectedFiles()[0]
            pathh = str(project_path)
            with open('Data/CPath_Project.txt', 'w') as file:
                file.write(pathh)
            messagebox = QMessageBox()
            messagebox.setWindowTitle("New Project"), messagebox.setText(f"New project created at {project_path}")
            messagebox.exec()
            self.treeview_project(project_path)

    def open_project_as_treeview(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        if dialog.exec():
            project_path = dialog.selectedFiles()[0]
            self.treeview_project(project_path)

    def new_document(self, checked=False, title="Scratch 1"):
        self.current_editor = self.create_editor()

        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, title)
        self.tab_widget.setCurrentWidget(self.current_editor)

    def custom_new_document(self, title, checked=False):
        self.current_editor = self.create_editor()
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, title)
        self.tab_widget.setCurrentWidget(self.current_editor)

    def cs_new_document(self, checked=False):
        text, ok = QInputDialog.getText(None, "New File", "Filename:")
        ext = text.split(".")[-1]
        self.current_editor = self.create_editor()
        self.editors.append(self.current_editor)
        self.tab_widget.addTab(self.current_editor, text)
        if ext == "md" or ext == "MD":
            self.markdown_new()
        self.tab_widget.setCurrentWidget(self.current_editor)

    def change_text_editor(self, index):
        if index < len(self.editors):
            # Set the previous editor as read-only
            if self.current_editor:
                self.current_editor.setReadOnly(True)

            self.current_editor = self.editors[index]

            self.current_editor.setReadOnly(False)

    def undo_document(self):
        self.current_editor.undo()

    def notes(self):
        note_dock = QDockWidget("Notes", self)
        terminal_widget = QPlainTextEdit(note_dock)
        note_dock.setWidget(terminal_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, note_dock)
        note_dock.show()

    def redo_document(self):
        self.current_editor.redo()

    def cut_document(self):
        self.current_editor.cut()

    def copy_document(self):
        self.current_editor.copy()

    def summary(self):
        lines = str(self.current_editor.lines())
        text = self.current_editor.text()
        text = "Number of Lines: " + lines
        messagebox = QMessageBox()
        messagebox.setText(text), messagebox.setWindowTitle("Summary")
        messagebox.exec()

    def paste_document(self):
        self.current_editor.paste()

    def remove_editor(self, index):
        self.tab_widget.removeTab(index)
        if index < len(self.editors):
            del self.editors[index]

    def open_document(self):
        a = ModuleFile.open_document(self)

    def save_document(self):
        ModuleFile.save_document(self)

    @staticmethod
    def about_github():
        webbrowser.open_new_tab("https://github.com/rohankishore/Aura-Notes")

    @staticmethod
    def version():
        text_ver = (
                "Aura Text"
                + "\n"
                + "Current Version: "
                + "4.0"
                + "\n"
                + "\n"
                + "Copyright © 2023 Rohan Kishore."
        )
        msg_box = QMessageBox()
        msg_box.setWindowTitle("About")
        msg_box.setText(text_ver)
        msg_box.exec()

    @staticmethod
    def getting_started():
        webbrowser.open_new_tab(
            "https://github.com/rohankishore/Aura-Text/wiki")

    @staticmethod
    def buymeacoffee():
        webbrowser.open_new_tab("https://www.buymeacoffee.com/auratext")

    def fullscreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showMaximized()

    @staticmethod
    def bug_report():
        webbrowser.open_new_tab(
            "https://github.com/rohankishore/Aura-Text/issues/new/choose"
        )

    @staticmethod
    def discord():
        webbrowser.open_new_tab("https://discord.gg/4PJfTugn")


def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme(theme, custom_colors={"primary" : theme_color})
    ex = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
