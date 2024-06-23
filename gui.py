import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from demo import process_document


class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection App")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.label = tk.Label(self.frame, text="Upload an image to detect face and show details")
        self.label.grid(row=0, column=0, columnspan=2)

        self.upload_button = tk.Button(self.frame, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(row=1, column=0, padx=10, pady=10)

        self.details_frame = tk.Frame(self.frame)
        self.details_frame.grid(row=2, column=0, columnspan=2)

        self.person_details = []
        self.documents = []

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.clear_details_frame()

        # Load and display the main uploaded image
        image = Image.open(file_path)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)

        main_image_label = tk.Label(self.details_frame, image=photo)
        main_image_label.image = photo  # Keep a reference to avoid garbage collection
        main_image_label.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Process document to get details and documents
        self.documents, self.person_details = process_document(cv2.imread(file_path))
        self.display_details()

    def clear_details_frame(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

    def display_details(self):
        # Display personal details
        details_text = "\n".join([f"{key}: {value}" for key, value in self.person_details.items()])
        details_label = tk.Label(self.details_frame, text=details_text, justify=tk.LEFT)
        details_label.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

        # Display each document
        for i, document in enumerate(self.documents, start=1):
            # Create a new frame for each document
            doc_frame = tk.Frame(self.details_frame, bd=2, relief=tk.SUNKEN)
            doc_frame.grid(row=i, column=0, padx=10, pady=10, sticky='nw')
            print(document)
            # Display the document image
            if 'FILENAME' in document:
                doc_image = Image.open(document['FILENAME'])
                doc_image.thumbnail((100, 100))
                doc_photo = ImageTk.PhotoImage(doc_image)
                image_label = tk.Label(doc_frame, image=doc_photo)
                image_label.image = doc_photo  # Keep a reference to avoid garbage collection
                image_label.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

            # Display the document details
            doc_details_text = "\n".join([f"{key}: {value}" for key, value in document.items() if key != 'FILENAME'])
            doc_details_label = tk.Label(doc_frame, text=doc_details_text, justify=tk.LEFT)
            doc_details_label.grid(row=0, column=1, padx=5, pady=5, sticky='nw')


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()
