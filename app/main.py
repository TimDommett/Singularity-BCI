import tkinter as tk
from neurosity_gui import NeurosityGUI

def main():
    root = tk.Tk()
    root.title("Neurosity Data Collector")
    app = NeurosityGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
