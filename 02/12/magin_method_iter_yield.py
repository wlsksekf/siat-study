class MyForder:
    def __init__(self, files):
        self.files = files

    def __iter__(self):
        print("__iter__")

        for file in self.files:
            yield f"Processing... {file}"
        
folder = MyForder(['doc1.pdf', 'image.png', 'data.csv'])

for f in folder:
    print(f)

for f in folder:
    print(f)