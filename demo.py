from photo_checker import get_person_document
from data_extractor import get_data_from_image
import uuid
import cv2
import copy
image = cv2.imread("data/documents/document_1.png")

# Function to process the document, check if it is already in the database, and save it if not. Returns all documents in the database with the same face and the extracted fields from given image.
def process_document(image):
    all_documents= get_person_document(image)
    document_fields = get_data_from_image(image)
    all_documents_copy = copy.deepcopy(all_documents)
    for document in all_documents_copy:
        document.pop('FILENAME', None)
    if document_fields != {} and document_fields not in all_documents_copy:
        print("Data not found in the database. Saving the document.")
        cv2.imwrite("data/documents/" + str(uuid.uuid4() ) + ".png", image)
    else:
        print("Document already in the database.")
    return all_documents, document_fields

result = process_document(image)
print(result)

