from docsvision.vision.pipeline import process_document

doc = process_document("samples/samples.pdf")
print(doc[:10])
