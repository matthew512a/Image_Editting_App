import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editing App")
        self.root.geometry("1120x600")
        self.root.configure(bg="tan")

        self.image = None
        self.edited_image = None
        self.undo_stack = []  # For undo functionality

        # Frames
        self.frame_left = tk.Frame(root, bg="tan")
        self.frame_left.place(x=15, y=20, width=500, height=500)

        self.frame_right = tk.Frame(root, bg="tan")
        self.frame_right.place(x=600, y=20, width=500, height=500)

        # Canvas for Original and Edited Images
        tk.Label(self.frame_left, text="Original Image", font=("Arial", 14), bg="tan").pack(pady=5)
        self.original_canvas = tk.Canvas(self.frame_left, width=300, height=300, bg="white")
        self.original_canvas.pack(pady=10)

        tk.Label(self.frame_right, text="Edited Image", font=("Arial", 14), bg="tan").pack(pady=5)
        self.edited_canvas = tk.Canvas(self.frame_right, width=300, height=300, bg="white")
        self.edited_canvas.pack(pady=10)

        # Buttons and Controls
        tk.Button(root, text="Browse a File", bg="yellow", command=self.open_image).place(x=50, y=400, width=100)
        tk.Button(root, text="Save", bg="green", command=self.save_image).place(x=50, y=450, width=100)
        tk.Button(root, text="Reset", bg="orange", command=self.reset_image).place(x=50, y=500, width=100)
        tk.Button(root, text="Undo", bg="blue", command=self.undo_last_change).place(x=50, y=550, width=100)
        tk.Button(root, text="Exit", bg="red", command=root.quit).place(x=50, y=600, width=100)

        # Sliders for Adjustments
        self.brightness_slider = self.add_slider("Brightness", 80 , 450, lambda e: self.adjust_brightness())
        self.color_slider = self.add_slider("Colors", 130, 450, lambda e: self.adjust_color())
        self.contrast_slider = self.add_slider("Contrast", 180, 450, lambda e: self.adjust_contrast())
        self.sharpen_slider = self.add_slider("Sharpen", 230, 450, lambda e: self.adjust_sharpen())
        self.blur_slider = self.add_slider("Blur", 260, 450, lambda e: self.apply_blur())

        # Dropdown for Rotation
        tk.Label(root, text="Rotation", bg="tan", font=("Arial", 10)).place(x=450, y=330)
        self.rotation_combo = ttk.Combobox(root, values=["90°", "180°", "270°", "Flip Horizontal", "Flip Vertical"])
        self.rotation_combo.place(x=525, y=330)
        self.rotation_combo.bind("<<ComboboxSelected>>", self.rotate_image)

        # Dropdown for Filters
        tk.Label(root, text="Filters", bg="tan", font=("Arial", 10)).place(x=450, y=370)
        self.filter_combo = ttk.Combobox(root, values=["BLACK AND WHITE", "BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE"])
        self.filter_combo.place(x=525, y=370)
        self.filter_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        # Resize Options
        tk.Label(root, text="Resize Image", bg="tan", font=("Arial", 10)).place(x=500, y=410)
        tk.Label(root, text="Width:", bg="tan").place(x=450, y=440)
        self.width_entry = tk.Entry(root, width=5)
        self.width_entry.place(x=500, y=440)
        tk.Label(root, text="Height:", bg="tan").place(x=550, y=440)
        self.height_entry = tk.Entry(root, width=5)
        self.height_entry.place(x=600, y=440)
        tk.Button(root, text="Apply", bg="pink", command=self.resize_image).place(x=500, y=470, width=100)

    def add_slider(self, label, y, x_offset, command):
        tk.Label(self.root, text=label, bg="tan", font=("Arial", 10)).place(x=x_offset, y=y)
        slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, orient="horizontal", bg="tan", command=command)
        slider.set(1)
        slider.place(x=x_offset + 100, y=y - 10)
        return slider

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.edited_image = self.image.copy()
            self.undo_stack = []  # Reset undo stack
            self.update_images()

    def save_image(self):
        if self.edited_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                self.edited_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showwarning("Warning", "No image to save!")

    def reset_image(self):
        if self.image:
            self.edited_image = self.image.copy()
            self.undo_stack = []  # Reset undo stack
            self.update_images()

    def scale_image_to_canvas(self, image, canvas):
        canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
        if canvas_width == 1 and canvas_height == 1:
            canvas_width, canvas_height = 300, 300  # Default for first display
        scaled_image = image.copy()
        scaled_image.thumbnail((canvas_width, canvas_height))
        return scaled_image

    def update_images(self):
        if self.image:
            scaled_original = self.scale_image_to_canvas(self.image, self.original_canvas)
            original_image_tk = ImageTk.PhotoImage(scaled_original)
            self.original_canvas.create_image(150, 150, image=original_image_tk)
            self.original_canvas.image = original_image_tk

            scaled_edited = self.scale_image_to_canvas(self.edited_image, self.edited_canvas)
            edited_image_tk = ImageTk.PhotoImage(scaled_edited)
            self.edited_canvas.create_image(150, 150, image=edited_image_tk)
            self.edited_canvas.image = edited_image_tk

    def adjust_brightness(self):
        if self.image:
            self.save_state_for_undo()
            enhancer = ImageEnhance.Brightness(self.image)
            self.edited_image = enhancer.enhance(self.brightness_slider.get())
            self.update_images()

    def adjust_color(self):
        if self.image:
            self.save_state_for_undo()
            enhancer = ImageEnhance.Color(self.image)
            self.edited_image = enhancer.enhance(self.color_slider.get())
            self.update_images()

    def adjust_contrast(self):
        if self.image:
            self.save_state_for_undo()
            enhancer = ImageEnhance.Contrast(self.image)
            self.edited_image = enhancer.enhance(self.contrast_slider.get())
            self.update_images()

    def adjust_sharpen(self):
        if self.image:
            self.save_state_for_undo()
            enhancer = ImageEnhance.Sharpness(self.image)
            self.edited_image = enhancer.enhance(self.sharpen_slider.get())
            self.update_images()

    def apply_blur(self):
        if self.image:
            self.save_state_for_undo()
            self.edited_image = self.image.filter(ImageFilter.GaussianBlur(radius=self.blur_slider.get()))
            self.update_images()

    def apply_filter(self, event=None):
        if self.image:
            self.save_state_for_undo()
            filter_name = self.filter_combo.get()
            if filter_name == "BLUR":
                self.edited_image = self.image.filter(ImageFilter.GaussianBlur(radius=2))
            elif filter_name == "CONTOUR":
                self.edited_image = self.image.filter(ImageFilter.CONTOUR)
            elif filter_name == "DETAIL":
                self.edited_image = self.image.filter(ImageFilter.DETAIL)
            elif filter_name == "EDGE_ENHANCE":
                self.edited_image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_name == "BLACK AND WHITE":
                self.edited_image = self.image.convert("L")
            self.update_images()

    def rotate_image(self, event):
        if self.image:
            self.save_state_for_undo()
            rotation_option = self.rotation_combo.get()
            if rotation_option == "90°":
                self.edited_image = self.image.rotate(-90, expand=True)
            elif rotation_option == "180°":
                self.edited_image = self.image.rotate(180, expand=True)
            elif rotation_option == "270°":
                self.edited_image = self.image.rotate(90, expand=True)
            elif rotation_option == "Flip Horizontal":
                self.edited_image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            elif rotation_option == "Flip Vertical":
                self.edited_image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
            self.update_images()

    def resize_image(self):
        if self.image:
            self.save_state_for_undo()
            try:
                new_width = int(self.width_entry.get())
                new_height = int(self.height_entry.get())
                self.edited_image = self.image.resize((new_width, new_height))
                self.update_images()
            except ValueError:
                messagebox.showerror("Error", "Invalid width or height")

    def save_state_for_undo(self):
        if self.edited_image:
            self.undo_stack.append(self.edited_image.copy())

    def undo_last_change(self):
        if self.undo_stack:
            self.edited_image = self.undo_stack.pop()
            self.update_images()
        else:
            messagebox.showwarning("Undo", "No more actions to undo!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
