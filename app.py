from customtkinter import *
from PIL import Image
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import showerror

from util import *
from time import time


from langchain.llms import Ollama
from langchain import PromptTemplate

D1 = '#2E073F'
D2 = '#7A1CAC'
L1 = '#EBD3F8'
L2 = '#AD49E1'

class ModelSelector(CTkToplevel):
    def __init__(self, master):

        models = list_models();
        n = len(models);

        super().__init__(master, fg_color=L1)  
        self.title("Model Selector")
        self.maxsize(350, 41*n+45)
        self.resizable =[False, True]

        self.attributes("-topmost", True)
        self.focus()


        CTkLabel(self, text="Choose a Model", width=320, font=("Roboto bold", 30), text_color=L1, fg_color=D1
            ).pack(side="top", fill='x')
        b = CTkLabel(self, text="Choose a Model", width=320, font=("Roboto bold", 30), text_color=L1, fg_color=D1
            )
        models_container= CTkScrollableFrame(self, fg_color=L1, scrollbar_button_color=L1, scrollbar_button_hover_color=D2)
        models_container.pack(fill="both", expand=True)

        for i, model_name in enumerate(models):
            b = CTkButton(models_container, text=model_name, command=lambda x=model_name: master.set_model(x), hover_color='#FFD700',
                      corner_radius=10, fg_color=L1, border_color=D2, text_color=D2, border_width=2, font=("Roboto", 18)
                      ).pack( fill="x", pady=3, padx=7, ipady=2)
            

class App(CTk):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, fg_color = L1,  **kwargs)
        self.geometry("1000x550")
        self.init_layout()
        self.init_setup()
        self.mainloop()

    def init_layout(self):
        navbar = CTkFrame(self, height=75, corner_radius=0, fg_color=D1, bg_color=D1)
        navbar.grid(row=0, column=0, sticky='NSEW')
        body = CTkFrame(self, height=525,  corner_radius=0, fg_color=L1)
        body.grid(row=1, column=0, sticky='NSEW')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)


        CTkLabel(navbar, text="Adept", font=("helvetica neue", 55), text_color="white"
            ).grid(row=0, column=0, sticky="NSEW", padx=20, pady=5)

        CTkButton(navbar, text="New Chat", font=("Roboto bold", 20), command=self.new_chat,
            height=50, width=110, corner_radius=10, text_color=D1, fg_color=L1, hover_color="#FFD700"
            ).grid(row=0, column=2, sticky="EW", pady=10)
        
        CTkButton(navbar, text="Clear Chat", font=("Roboto bold", 20), command=self.clear_chat,
            height=50, width=110, corner_radius=10, text_color=D1, fg_color=L1, hover_color="#DA0B58"
            ).grid(row=0, column=3, sticky="EW", pady=10, padx=10)

        navbar.columnconfigure(1, weight=1, minsize=1)
        navbar.rowconfigure(0, weight=1)
 
        container = CTkFrame(body, fg_color=L1, border_color=D2, border_width=2, corner_radius=18)
        container.pack(fill="both", expand=True, padx=15, pady=15)

        self.chats_container = CTkScrollableFrame(container, fg_color=L1, scrollbar_button_color=L1, scrollbar_button_hover_color=D2)
        self.chats_container.pack(fill="both", expand=True, padx=12, pady=10)

        input_container = CTkFrame(container, fg_color=L1, border_color=D2, border_width=2, corner_radius=11)
        input_container.pack(fill="x", padx=15, pady=15)

        self.inp = CTkTextbox(input_container, fg_color=L1, text_color=D2, font=("Roboto", 16), height=160)
        self.inp.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        buttons = CTkFrame(input_container, fg_color=L1)
        buttons.pack(side="right",  padx=7, pady=5, anchor="s", fill="y")


        self.model_btn = CTkImage(Image.open("assets/mistral.png"), size=(25, 25))
        send_icon = CTkImage(Image.open("assets/send.png"), size=(25, 25))
        files_icon = CTkImage(Image.open("assets/files.png"), size=(25, 25))


        CTkButton(buttons, fg_color=L1, text="", image=self.model_btn, width=25, hover=False, command=self.prompt_change_model).pack(side="top", pady=5)
        CTkButton(buttons, fg_color=L1, text="", image=send_icon, width=25, hover=False, command=self.send).pack(side="bottom", pady=5)
        CTkButton(buttons, fg_color=L1, text="", image=files_icon, width=25, hover=False, command=self.prompt_upload).pack(side="bottom", pady=5)

        self.bind('<Return>', self.callback_for_enter)


    def new_chat(self):
        self.chained = False;
        self.chain = None;
        self.documents = [];
        self.clear_chat();
    
    def clear_chat(self):
        for widget in self.chats_container.slaves():
            widget.destroy()

    def prompt_change_model(self):
        if not self.chained:
            showerror("No File Uploaded.", "Upload a pdf first.")
            return
        ModelSelector(self)

    def send(self):
        if not self.chained:
            showerror("No File Uploaded.", "Upload a pdf to chat with.")
            return
        if not self.loading:
            query = self.inp.get(1.0, END).strip()
            if query != "":
                self.loadinig = True
                self.append_message(query, True);
                response = get_response(query, self.chain);
                self.append_message(response, False);
            self.inp.delete(1.0, END);
            self.loading = False;
            self.after(1, self.chats_container._parent_canvas.yview_moveto, 1.0)

        

    def prompt_upload(self):
        paths  = askopenfilenames(filetypes=[(".pdf", 'PDF')], defaultextension='.pdf')
        for path in paths:
            self.append_message("Uploaded: "+path.split('/')[-1], True)
            docs = load_pdf_data(file_path=path)
            self.documents += split_docs(documents=docs)
        self.vectorstore = create_embeddings(self.documents, self.embed)
        self.retriever = self.vectorstore.as_retriever()
        self.chain = load_qa_chain(self.retriever, self.llm, self.prompt)
        self.chained = True

    def append_message(self, message, isUser):
        if isUser:
            CTkLabel(self.chats_container, text=message, fg_color=  D2, corner_radius=10, text_color=L1, font=("Roboto", 18), justify="right"
            ).pack(side="top", anchor= "e", padx=5, pady=2, ipadx=2, ipady=10)
        else:
            CTkLabel(self.chats_container, text=message, fg_color=  D2, corner_radius=10, text_color=L1, font=("Roboto", 18), justify="left"
            ).pack(side="top", anchor= "w", padx=5, pady=2, ipadx=10, ipady=10)

    def init_setup(self):
        self.loading = True
        self.chained = False
        self.embed = load_embedding_model(model_path="all-MiniLM-L6-v2")
        self.prompt = PromptTemplate.from_template(template)
        self.documents = []
        models = list_models();
        if models is None:
            showerror("No models", "No models found")
            self.destroy();
        self.model_name = "mistral:latest"
        self.llm = Ollama(model=self.model_name, temperature=0)
        self.chain = None;
        self.loading = False

    def set_model(self, model_name):
        self.loading =True
        try:
            self.llm = Ollama(model=model_name, temperature=0)
            self.chain = load_qa_chain(self.retriever, self.llm, self.prompt)
            self.model_name = model_name
            print("current model: ", self.model_name)
        except:
            self.set_model(self.model_name)
        self.loading = False

    def callback_for_enter(self, event):
        self.send()







if __name__ == "__main__":
    app = App()