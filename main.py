import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarker")
        self.root.geometry("800x700")
        self.root.config(bg="#20232a")

        self.image_path = None
        self.image = None
        self.tk_image = None
        self.text_color = (255, 255, 255)
        self.position = tk.StringVar(value="Bottom Right")

        tk.Label(root, text="🖋️ Image Watermark App", font=("Arial", 22, "bold"),
                 fg="#61dafb", bg="#20232a").pack(pady=15)

        tk.Button(root, text="Upload Image", command=self.upload_image,
                  bg="#61dafb", fg="black", font=("Arial", 12, "bold"), width=15).pack(pady=5)

        self.canvas = tk.Canvas(root, width=600, height=350, bg="white", highlightthickness=2)
        self.canvas.pack(pady=10)

        self.text_entry = tk.Entry(root, width=40, font=("Arial", 14))
        self.text_entry.pack(pady=10)
        self.text_entry.insert(0, "Enter your watermark text")

        self.size_slider = tk.Scale(root, from_=20, to=100, orient="horizontal",
                                    label="Font Size", bg="#20232a", fg="white", troughcolor="#61dafb")
        self.size_slider.set(40)
        self.size_slider.pack(pady=5)

        color_pos_frame = tk.Frame(root, bg="#20232a")
        color_pos_frame.pack(pady=5)

        tk.Button(color_pos_frame, text="Choose Color", command=self.choose_color,
                  bg="#9c27b0", fg="white", font=("Arial", 12, "bold"), width=15).grid(row=0, column=0, padx=5)
        tk.OptionMenu(color_pos_frame, self.position, "Top Left", "Top Right", "Center", "Bottom Left", "Bottom Right").grid(row=0, column=1, padx=5)

        btn_frame = tk.Frame(root, bg="#20232a")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Watermark", command=self.add_watermark,
                  bg="#00c853", fg="white", font=("Arial", 12, "bold"), width=15).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Reset Image", command=self.reset_image,
                  bg="#ff9800", fg="black", font=("Arial", 12, "bold"), width=15).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Save Image", command=self.save_image,
                  bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=15).grid(row=0, column=2, padx=5, pady=5)

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not path:
            return
        self.image_path = path
        self.image = Image.open(path).convert("RGBA")
        self.display_image(self.image)
        messagebox.showinfo("Success", "Image uploaded successfully!")

    def display_image(self, img):
        self.canvas.delete("all")
        display_image = img.copy()
        display_image.thumbnail((600, 350))
        self.tk_image = ImageTk.PhotoImage(display_image)
        self.canvas.create_image(300, 175, image=self.tk_image)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Text Color")
        if color_code and color_code[0] is not None:
            r, g, b = color_code[0]
            self.text_color = (int(r), int(g), int(b))

    def add_watermark(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        text = self.text_entry.get().strip()
        if not text:
            messagebox.showerror("Error", "Please enter watermark text!")
            return
        base = Image.open(self.image_path).convert("RGBA")
        txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        try:
            font = ImageFont.truetype("arial.ttf", self.size_slider.get())
        except:
            font = ImageFont.load_default()
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        pos = self.position.get()
        if pos == "Top Left":
            x, y = 20, 20
        elif pos == "Top Right":
            x, y = base.width - text_width - 20, 20
        elif pos == "Center":
            x, y = (base.width - text_width) / 2, (base.height - text_height) / 2
        elif pos == "Bottom Left":
            x, y = 20, base.height - text_height - 20
        else:
            x, y = base.width - text_width - 20, base.height - text_height - 20
        draw.text((x, y), text, font=font, fill=self.text_color + (150,))
        combined = Image.alpha_composite(base, txt_layer)
        self.image = combined.convert("RGB")
        self.display_image(self.image)
        messagebox.showinfo("Success", "Watermark added!")

    def reset_image(self):
        if self.image_path:
            self.image = Image.open(self.image_path).convert("RGBA")
            self.display_image(self.image)
            messagebox.showinfo("Reset", "Image reset to original!")

    def save_image(self):
        if not self.image:
            messagebox.showerror("Error", "No image to save!")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if save_path:
            self.image.save(save_path)
            messagebox.showinfo("Saved", f"Image saved as {os.path.basename(save_path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
