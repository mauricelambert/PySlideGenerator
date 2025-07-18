#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    little GUI to generate my slides
#    Copyright (C) 2025  PySlidesGenerator

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
little GUI to generate my slides
"""

__version__ = "0.0.2"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
little GUI to generate my slides
"""
__url__ = "https://github.com/mauricelambert/PySlidesGenerator"

# __all__ = []

__license__ = "GPL-3.0 License"
__copyright__ = """
PySlidesGenerator  Copyright (C) 2025  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
copyright = __copyright__
license = __license__

print(copyright)

from tkinter import (
    Menu,
    Frame,
    Label,
    Entry,
    Event,
    Listbox,
    Button,
    IntVar,
    StringVar,
    Toplevel,
    END,
    Radiobutton,
    Text,
    Tk,
    Canvas,
    Scrollbar,
    Misc,
)
from tkinter.messagebox import showerror, showinfo, showwarning, askokcancel
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Dict, List, Union
from string import Template
from json import dump, load

table_of_content_subtitle = Template(
    """<li><a href="#slide-${id}">${title}</a>
            <ul>
              ${titles}
            </ul>
          </li>"""
)

table_of_content_content = Template(
    '<li><a href="#slide-${id}">${title}</a></li>'
)

subtitle = Template(
    """<header>
        <img src="${icon}" alt="MauriceLambert icon" />
      </header>
      <article>
        <h2>${title}</h2>
      </article>"""
)

content = Template(
    """<header>
        <img src="${icon}" alt="MauriceLambert icon" />
        <h3>${title}</h3>
      </header>
      <article>
        <div class="text">
          ${text}
        </div>
        <img src="${image}" alt="Illustration" />
      </article>
      <aside>${aside}</aside>"""
)

paragraph = Template("<p>${content}</p>")
list_element = Template("<li>${content}</li>")
ordered_list = Template(
    """<ol>
            ${list_content}
          </ol>"""
)
bullet_points = Template(
    """<ul>
            ${list_content}
          </ul>"""
)
section = Template(
    """<section id="slide-${index}" class="${class_name}">
      ${content}
    </section>"""
)

template = Template(
    """<!DOCTYPE html>
<!--
  Copyright (C) 2025 MauriceLambert

  This file is part of PySlidesGenerator.

  PySlidesGenerator is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  PySlidesGenerator is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with PySlidesGenerator.  If not, see <https://www.gnu.org/licenses/>.
-->
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="index, follow">
  <meta name="description" content="${description}" />
  <meta name="keywords" content="${keywords}" />
  <meta name="author" content="${author}" />
  <title>${title}</title>
  <link rel="stylesheet" href="../styles.css" />
  <script defer src="../script.js"></script>
</head>
<body>
  <main>
    <section id="slide-1" class="title-slide">
      <div id="terminal-overlay">
        <pre id="terminal-output"></pre>
      </div>
      <header>
        <img src="${default_icon}" alt="MauriceLambert icon" />
      </header>
      <article>
        <h1>${title}</h1>
      </article>
    </section>
    <section class="table-content" id="slide-2">
      <header>
        <img src="${default_icon}" alt="MauriceLambert icon" />
      </header>
      <nav>
        <ul>
          ${table_of_content}
        </ul>
      </nav>
    </section>
    ${slides}
    <section class="timeline-slide content-slide" id="timeline-slide">
      <header>
        <img src="https://mauricelambert.github.io/MauriceLambert.png" alt="MauriceLambert icon" />
        <h3>My path, my passion: cybersecurity</h3>
      </header>
      <article>
        <div id="timeline-container"></div>
        <div id="timeline-progress"></div>
      </article>
    </section>
  </main>
  <footer>
    <p><a href="https://www.gnu.org/licenses/">&copy; ${author}</a></p>
  </footer>
</body>
</html>"""
)


class ScrollableFrame(Frame):
    """
    This class implements a scrollable frame.
    """

    def __init__(self, container: Misc, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self, bg="#2e2e2e", highlightthickness=0)
        self.scrollbar = Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = Frame(self.canvas, bg="#2e2e2e")

        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.scrollable_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind(
            "<Enter>", lambda e: self._bind_mousewheel()
        )
        self.scrollable_frame.bind(
            "<Leave>", lambda e: self._unbind_mousewheel()
        )

    def _on_frame_configure(self, event: Event = None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event: Event = None):
        # canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_window)  # , width=canvas_width

    def _bind_mousewheel(self):
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )

    def _unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class SlideGeneratorApp:
    """
    This class is the main class for the application,
    it manage GUI, data and files events.
    """

    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Slide Editor")
        self.root.geometry("800x600")
        self.data = {
            "title": "",
            "keywords": [],
            "description": "",
            "author": "Maurice Lambert",
            "default icon": "https://mauricelambert.github.io/MauriceLambert.png",
            "default aside": 'References: <a href="https://github.com/mauricelambert/">Github MauriceLambert</a>, <a href="https://mauricelambert.github.io/">MauriceLambert WebSite</a>.',
            "slides": [],
        }
        self.file_path = None
        self.export_path = None
        self.modified = False
        self.setup_ui()
        self.populate_fields()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self) -> None:
        """
        This method create the main UI page.
        """

        self.root.configure(bg="#2e2e2e")

        menu_bar = Menu(self.root, bg="#2e2e2e", fg="#dd8a12")
        file_menu = Menu(menu_bar, tearoff=0, bg="#2e2e2e", fg="#dd8a12")
        file_menu.add_command(label="New (Ctrl+N)", command=self.new_file)
        file_menu.add_command(label="Open (Ctrl+O)", command=self.load_file)
        file_menu.add_command(label="Save (Ctrl+S)", command=self.save_file)
        file_menu.add_command(
            label="Generate (Ctrl+G)", command=self.generate_slides
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit (Ctrl+Q)", command=self.on_close)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

        scroll_frame = ScrollableFrame(self.root)
        scroll_frame.pack(fill="both", expand=True, pady=10)
        self.main_frame = scroll_frame.scrollable_frame

        self.entries = {}
        for field in [
            "title",
            "description",
            "author",
            "default icon",
            "default aside",
        ]:
            label = Label(
                self.main_frame,
                text=field.capitalize(),
                bg="#2e2e2e",
                fg="#dd8a12",
            )
            label.pack(anchor="w")
            entry = Entry(
                self.main_frame,
                bg="#1e1e1e",
                fg="#dd8a12",
                insertbackground="#dd8a12",
            )
            entry.pack(fill="x")
            entry.bind("<KeyRelease>", self.mark_modified)
            self.entries[field] = entry

        keywords_label = Label(
            self.main_frame, text="Keywords", bg="#2e2e2e", fg="#dd8a12"
        )
        keywords_label.pack(anchor="w")

        self.keyword_labels = []
        self.keyword_entries = []
        self.keyword_frame = Frame(self.main_frame, bg="#2e2e2e")
        self.keyword_frame.pack(fill="x", pady=5)
        self.add_keyword_entry()

        self.slides_label = Label(
            self.main_frame, text="Slides", bg="#2e2e2e", fg="#dd8a12"
        )
        self.slides_label.pack(anchor="w")
        self.slides_listbox = Listbox(
            self.main_frame, bg="#1e1e1e", fg="#dd8a12"
        )
        self.slides_listbox.pack(fill="both", expand=True, pady=5)

        slide_buttons_frame = Frame(self.main_frame, bg="#2e2e2e")
        slide_buttons_frame.pack(fill="x")

        self.add_slide_button = Button(
            slide_buttons_frame,
            text="Add Slide",
            command=self.add_slide_dialog,
            bg="#1e1e1e",
            fg="#dd8a12",
            activebackground="#444444",
            activeforeground="#dd8a12",
        )
        self.add_slide_button.pack(side="left", padx=5, pady=5)

        self.edit_slide_button = Button(
            slide_buttons_frame,
            text="Edit Slide",
            command=self.edit_selected_slide,
            bg="#1e1e1e",
            fg="#dd8a12",
            activebackground="#444444",
            activeforeground="#dd8a12",
        )
        self.edit_slide_button.pack(side="left", padx=5, pady=5)

        self.remove_slide_button = Button(
            slide_buttons_frame,
            text="Remove Selected Slide",
            command=self.remove_selected_slide,
            bg="#1e1e1e",
            fg="#dd8a12",
            activebackground="#444444",
            activeforeground="#dd8a12",
        )
        self.remove_slide_button.pack(side="left", padx=5, pady=5)

        self.move_up_button = Button(
            slide_buttons_frame,
            text="Move Up",
            command=self.move_slide_up,
            bg="#1e1e1e",
            fg="#dd8a12",
            activebackground="#444444",
            activeforeground="#dd8a12",
        )
        self.move_up_button.pack(side="left", padx=5, pady=5)

        self.move_down_button = Button(
            slide_buttons_frame,
            text="Move Down",
            command=self.move_slide_down,
            bg="#1e1e1e",
            fg="#dd8a12",
            activebackground="#444444",
            activeforeground="#dd8a12",
        )
        self.move_down_button.pack(side="left", padx=5, pady=5)

        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-o>", lambda event: self.load_file())
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-q>", lambda event: self.on_close())
        self.root.bind("<Control-g>", lambda event: self.generate_slides())

    def mark_modified(self, event: Event = None) -> None:
        """
        Simple method to set the modified attibrute on event.
        """

        self.modified = True

    def on_close(self) -> None:
        """
        This method manages windows destruction
        and unsaved data.
        """

        if self.modified:
            result = askokcancel(
                "Unsaved Changes",
                "There are unsaved changes. Do you want to continue without saving?",
            )
            if not result:
                return
        self.root.destroy()

    def add_keyword_entry(self) -> None:
        """
        This method adds a new keyword entry.
        """

        entry = Entry(
            self.keyword_frame,
            bg="#1e1e1e",
            fg="#dd8a12",
            insertbackground="#dd8a12",
        )
        entry.pack(fill="x", pady=2)
        entry.bind("<KeyRelease>", self.keyword_entry_updated)
        entry.bind("<KeyRelease>", self.mark_modified, add="+")
        self.keyword_entries.append(entry)

    def keyword_entry_updated(self, event: Event) -> None:
        """
        This method is the callback event to define
        when the app should add a new keyword entry.
        """

        for entry in self.keyword_entries:
            if not entry.get().strip():
                break
        else:
            self.add_keyword_entry()

    def new_file(self) -> None:
        """
        This method defines a new file content.
        """

        self.file_path = None
        self.data = {
            "title": "",
            "keywords": [],
            "description": "",
            "author": "Maurice Lambert",
            "default icon": "../MauriceLambert.jpg",
            "default aside": 'References: <a href="https://github.com/mauricelambert/">Github MauriceLambert</a>, <a href="https://mauricelambert.github.io/">MauriceLambert WebSite</a>.',
            "slides": [],
        }
        for key in self.entries:
            self.entries[key].delete(0, END)
        for entry in self.keyword_entries:
            entry.destroy()
        self.keyword_entries.clear()
        self.add_keyword_entry()
        self.slides_listbox.delete(0, END)
        self.modified = False

    def load_file(self) -> None:
        """
        This method loads slides from a saved file.
        """

        path = askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not path:
            return
        try:
            with open(path, "r") as file:
                self.data = load(file)
            self.populate_fields()
        except Exception as e:
            showerror("Error", f"Could not load file:\n{e}")
        else:
            self.file_path = path
            self.modified = False

    def generate_slides(self) -> None:
        """
        This method generates slides from current data.
        """

        if not self.export_path:
            path = asksaveasfilename(
                defaultextension=".html", filetypes=[("HTML Files", "*.html")]
            )
            if not path:
                return
            self.export_path = path

        self.update_data_from_fields()

        slides = ""
        titles = ""
        last_subtitle = ""
        table_of_content = ""
        for index, slide in enumerate(self.data["slides"]):
            if slide["type"] == "content":
                texts = ""
                for text in slide["texts"]:
                    if text["type"] == "p":
                        texts += paragraph.safe_substitute(
                            content=text["content"]
                        )
                    else:
                        list_content = ""
                        for element in text["content"]:
                            list_content += list_element.safe_substitute(
                                content=element
                            )
                        if text["type"] == "ul":
                            texts += bullet_points.safe_substitute(
                                list_content=list_content
                            )
                        elif text["type"] == "ol":
                            texts += ordered_list.safe_substitute(
                                list_content=list_content
                            )
                section_content = content.safe_substitute(
                    icon=slide["icon"],
                    title=slide["title"],
                    text=texts,
                    aside=slide["aside"],
                    image=slide["image"],
                )
                titles += table_of_content_content.safe_substitute(
                    title=slide["title"], id=index + 3
                )
                class_name = "content-slide"
            elif slide["type"] == "title":
                if last_subtitle:
                    table_of_content += (
                        table_of_content_subtitle.safe_substitute(
                            title=last_subtitle,
                            titles=titles,
                            id=last_subtitle_index,
                        )
                    )
                    titles = ""
                last_subtitle = slide["title"]
                last_subtitle_index = index + 3
                section_content = subtitle.safe_substitute(
                    title=last_subtitle, icon=slide["icon"]
                )
                class_name = "subtitle-slide"
            slides += section.safe_substitute(
                index=str(index + 3),
                class_name=class_name,
                content=section_content,
            )

        table_of_content += table_of_content_subtitle.safe_substitute(
            title=last_subtitle, titles=titles, id=last_subtitle_index
        )

        file_content = template.safe_substitute(
            description=self.data["description"],
            keywords=", ".join(self.data["keywords"]),
            title=self.data["title"],
            default_icon=self.data["default icon"],
            table_of_content=table_of_content,
            slides=slides,
            author=self.data["author"],
        )

        try:
            with open(self.export_path, "w") as file:
                file.write(file_content)
        except Exception as e:
            showerror("Error", f"Could not generate file:\n{e}")
        else:
            showinfo("Generated", "File generated successfully!")

    def save_file(self) -> None:
        """
        This method saves data into JSON file.
        """

        if not self.file_path:
            path = asksaveasfilename(
                defaultextension=".json", filetypes=[("JSON Files", "*.json")]
            )
            if not path:
                return
            self.file_path = path

        self.update_data_from_fields()
        try:
            with open(self.file_path, "w") as file:
                dump(self.data, file, indent=4)
        except Exception as e:
            showerror("Error", f"Could not save file:\n{e}")
        else:
            showinfo("Saved", "File saved successfully!")
            self.modified = False

    def populate_fields(self) -> None:
        """
        This method fills elements values in the GUI.
        """

        for key in self.entries:
            self.entries[key].delete(0, END)
            self.entries[key].insert(0, self.data.get(key, ""))
        for entry in self.keyword_entries:
            entry.destroy()
        self.keyword_entries.clear()
        for keyword in self.data.get("keywords", []):
            entry = Entry(
                self.keyword_frame,
                bg="#1e1e1e",
                fg="#dd8a12",
                insertbackground="#dd8a12",
            )
            entry.insert(0, keyword)
            entry.pack(fill="x", pady=2)
            entry.bind("<KeyRelease>", self.keyword_entry_updated)
            entry.bind("<KeyRelease>", self.mark_modified, add="+")
            self.keyword_entries.append(entry)
        self.add_keyword_entry()
        self.slides_listbox.delete(0, END)
        for idx, slide in enumerate(self.data.get("slides", [])):
            self.slides_listbox.insert(END, f"{idx+1}: {slide['type']}")

    def update_data_from_fields(self) -> None:
        """
        This method updates data with main windows
        entries content.
        """

        for key in self.entries:
            self.data[key] = self.entries[key].get()
        self.data["keywords"] = [
            entry.get()
            for entry in self.keyword_entries
            if entry.get().strip()
        ]

    def add_slide_dialog(self) -> None:
        """
        This method manages the new slide GUI and data.
        """

        dialog = Toplevel(self.root)
        dialog.title("Add Slide")
        dialog.geometry("300x200")
        dialog.configure(bg="#2e2e2e")

        Label(dialog, text="Position", bg="#2e2e2e", fg="#dd8a12").pack(pady=5)
        position_var = IntVar(value=len(self.data["slides"]) + 1)
        position_entry = Entry(
            dialog,
            textvariable=position_var,
            bg="#1e1e1e",
            fg="#dd8a12",
            insertbackground="#dd8a12",
        )
        position_entry.pack(fill="x", padx=10)

        Label(dialog, text="Type", bg="#2e2e2e", fg="#dd8a12").pack(pady=5)
        type_var = StringVar(value="title")

        type_frame = Frame(dialog, bg="#2e2e2e")
        type_frame.pack(pady=5)

        title_button = Radiobutton(
            type_frame,
            text="Title",
            variable=type_var,
            value="title",
            bg="#2e2e2e",
            fg="#dd8a12",
            selectcolor="#1e1e1e",
            activebackground="#2e2e2e",
            activeforeground="#dd8a12",
        )
        content_button = Radiobutton(
            type_frame,
            text="Content",
            variable=type_var,
            value="content",
            bg="#2e2e2e",
            fg="#dd8a12",
            selectcolor="#1e1e1e",
            activebackground="#2e2e2e",
            activeforeground="#dd8a12",
        )
        title_button.pack(side="left", padx=10)
        content_button.pack(side="left", padx=10)

        def submit() -> None:
            """
            This function adds the new slide.
            """

            try:
                pos = int(position_var.get())
                if not (1 <= pos <= len(self.data["slides"]) + 1):
                    raise ValueError
            except ValueError:
                showerror("Invalid", "Position must be a valid number.")
                return

            slide_type = type_var.get()
            slide = {"type": slide_type, "icon": self.data["default icon"]}
            if slide_type == "title":
                slide["title"] = ""
            else:
                slide.update(
                    {
                        "aside": self.data["default aside"],
                        "title": "",
                        "image": "",
                        "texts": [],
                    }
                )

            self.update_data_from_fields()
            self.data["slides"].insert(pos - 1, slide)
            self.populate_fields()
            dialog.destroy()
            self.modified = True

        Button(
            dialog,
            text="Add Slide",
            command=submit,
            bg="#1e1e1e",
            fg="#dd8a12",
            activebackground="#444444",
            activeforeground="#dd8a12",
        ).pack(pady=10)

    def edit_selected_slide(self) -> None:
        """
        This method starts the GUI page to edit a selected slide.
        """

        selection = self.slides_listbox.curselection()
        if not selection:
            showwarning("No selection", "Please select a slide to edit.")
            return
        index = selection[0]
        slide = self.data["slides"][index]
        self.open_slide_editor(slide, index)

    def remove_selected_slide(self) -> None:
        """
        This method removes the selected slide.
        """

        selection = self.slides_listbox.curselection()
        if not selection:
            showwarning("No selection", "Please select a slide to remove.")
            return
        index = selection[0]
        del self.data["slides"][index]
        self.populate_fields()
        self.modified = True

    def move_slide_up(self) -> None:
        """
        This method moves up the selected slide.
        """

        selection = self.slides_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        index = selection[0]
        self.data["slides"][index - 1], self.data["slides"][index] = (
            self.data["slides"][index],
            self.data["slides"][index - 1],
        )
        self.populate_fields()
        self.slides_listbox.select_set(index - 1)
        self.modified = True

    def move_slide_down(self) -> None:
        """
        This method moves down the selected slide.
        """

        selection = self.slides_listbox.curselection()
        if not selection or selection[0] == len(self.data["slides"]) - 1:
            return
        index = selection[0]
        self.data["slides"][index + 1], self.data["slides"][index] = (
            self.data["slides"][index],
            self.data["slides"][index + 1],
        )
        self.populate_fields()
        self.slides_listbox.select_set(index + 1)
        self.modified = True

    def open_slide_editor(
        self,
        slide: Dict[str, Union[List[Dict[str, str]], str]],
        index: int = None,
    ) -> None:
        """
        This method manages the slide edition GUI and data.
        """

        def modify(event: Event) -> None:
            nonlocal unsaved_slide
            unsaved_slide = True

        dialog = Toplevel(self.root)
        dialog.title("Edit Slide")
        dialog.geometry("600x600")
        dialog.configure(bg="#2e2e2e")

        form_frame = Frame(dialog, bg="#2e2e2e")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = Frame(dialog, bg="#2e2e2e")
        button_frame.pack(fill="both", padx=10, pady=10)

        fields = {}
        for field in (
            ("icon", "aside", "title", "image")
            if slide["type"] == "content"
            else ("icon", "title")
        ):
            Label(
                form_frame, text=field.capitalize(), bg="#2e2e2e", fg="#dd8a12"
            ).pack(anchor="w")
            entry = Entry(
                form_frame,
                bg="#1e1e1e",
                fg="#dd8a12",
                insertbackground="#dd8a12",
            )
            entry.insert(0, slide.get(field, "") if slide else "")
            entry.bind("<KeyRelease>", modify)
            entry.pack(fill="x")
            fields[field] = entry

        scroll_frame = ScrollableFrame(form_frame)
        scroll_frame.pack(fill="both", expand=True, pady=10)
        text_container = scroll_frame.scrollable_frame

        unsaved_slide = False

        if slide["type"] == "content":
            Label(
                text_container, text="Texts", bg="#2e2e2e", fg="#dd8a12"
            ).pack(anchor="w")
            texts = {}

        def add_text_block(text_data: Dict[str, str] = None, modify=True):
            """
            This function adds the GUI components
            to configure a text content.
            """

            nonlocal unsaved_slide
            unsaved_slide = modify

            text_type = StringVar(
                value=(text_data["type"] if text_data else "p")
            )
            frame = Frame(text_container, bg="#1e1e1e")
            frame.pack(fill="x", pady=5)

            type_frame = Frame(frame, bg="#1e1e1e")
            type_frame.pack(fill="x")
            for t_human, t_html in [
                ("paragraph", "p"),
                ("bullet points", "ul"),
                ("ordered list", "ol"),
            ]:
                Radiobutton(
                    type_frame,
                    text=t_human,
                    variable=text_type,
                    value=t_html,
                    bg="#1e1e1e",
                    fg="#dd8a12",
                    selectcolor="#2e2e2e",
                ).pack(side="left")

            content_frame = Frame(frame, bg="#2e2e2e")
            content_frame.pack(fill="both")
            content_widget = []

            def render_content_widget() -> None:
                """
                This function can modify the text content type and GUI components.
                """

                for widget in content_frame.winfo_children():
                    widget.destroy()

                nonlocal content_widget
                content_widget = []

                if text_type.get() == "p":
                    text = Text(
                        content_frame,
                        height=3,
                        bg="#1e1e1e",
                        fg="#dd8a12",
                        insertbackground="#dd8a12",
                    )
                    if text_data and text_data["type"] == "p":
                        text.insert("1.0", text_data["content"])
                    text.pack(fill="x")
                    content_widget = text
                else:
                    entries = []
                    initial = (
                        text_data["content"]
                        if text_data and isinstance(text_data["content"], list)
                        else [""]
                    )
                    for item in initial:
                        entry = Entry(
                            content_frame,
                            bg="#1e1e1e",
                            fg="#dd8a12",
                            insertbackground="#dd8a12",
                        )
                        entry.insert(0, item)
                        entry.pack(fill="x", pady=2)
                        entries.append(entry)

                    def check_to_add_new(
                        event: Event, last_entry: Entry
                    ) -> None:
                        """
                        This function adds a new entry for list content.
                        """

                        if last_entry.get() and last_entry == entries[-1]:
                            new_entry = Entry(
                                content_frame,
                                bg="#1e1e1e",
                                fg="#dd8a12",
                                insertbackground="#dd8a12",
                            )
                            new_entry.pack(fill="x", pady=2)
                            new_entry.bind(
                                "<KeyRelease>",
                                lambda e: check_to_add_new(e, new_entry),
                            )
                            entries.append(new_entry)

                        nonlocal unsaved_slide
                        unsaved_slide = event is not None

                    if entries:
                        entries[-1].bind(
                            "<KeyRelease>",
                            lambda e: check_to_add_new(e, entries[-1]),
                        )

                    check_to_add_new(None, entries[-1])
                    content_widget = entries

                texts[text_type._name] = (text_type, content_widget)

            text_type.trace_add("write", lambda *_: render_content_widget())
            render_content_widget()
            scroll_frame._on_frame_configure()
            scroll_frame._on_canvas_configure()

        if slide["type"] == "content":
            for text_block in slide["texts"]:
                add_text_block(text_block, False)

            Button(
                button_frame,
                text="Add Text",
                command=add_text_block,
                bg="#1e1e1e",
                fg="#dd8a12",
            ).pack(side="left", padx=5, pady=5)

        def save() -> None:
            """
            This method saves the texts contents.
            """

            if slide["type"] == "content":
                for t_type, content_widget in texts.values():
                    if t_type.get() == "p":
                        content = content_widget.get("1.0", "end").strip()
                        if content:
                            new = {"type": "p", "content": content}
                            for text in slide["texts"]:
                                if text == new:
                                    break
                            else:
                                slide["texts"].append(new)
                    else:
                        content = [
                            entry.get().strip()
                            for entry in content_widget
                            if entry.get().strip()
                        ]
                        new = {"type": t_type.get(), "content": content}
                        for text in slide["texts"]:
                            if text == new:
                                break
                        else:
                            slide["texts"].append(new)

            for field, value in fields.items():
                if data := value.get().strip():
                    slide[field] = data
            self.populate_fields()
            self.modified = True
            dialog.destroy()

            nonlocal unsaved_slide
            unsaved_slide = False

        Button(
            button_frame,
            text="Save Slide",
            command=save,
            bg="#1e1e1e",
            fg="#dd8a12",
        ).pack(side="left", padx=5, pady=10)

        def on_close_dialog() -> None:
            if unsaved_slide:
                if not askokcancel(
                    "Unsaved Slide",
                    "This slide has unsaved changes. Close anyway?",
                ):
                    return
            dialog.destroy()

        dialog.protocol("WM_DELETE_WINDOW", on_close_dialog)


if __name__ == "__main__":
    root = Tk()
    app = SlideGeneratorApp(root)
    root.mainloop()
