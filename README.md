# ChatGPT-Powered PDF Assistant

This project provides a user-friendly Document (PDF, Doc and text file) assistant powered by a conversational AI model. Users can upload documents, query them, and receive answers in an intuitive GUI built with `customtkinter`.

---

## Features

- **Chat Interface:** Interact with your PDF data through a simple and **retro themed** GUI.
- **Customizable Models:** Choose from a list of conversational AI models.
- **Document Upload Support:** Upload multiple documents to extract and query data.
- **Embeddings Support:** Leverages advanced embedding models for enhanced question-answering capabilities.
- **Easy Navigation:** Scrollable chat history for reference.

---

## Prerequisites

Before running the project, ensure you have the following:

1. Python 3.10 or later.
2. Pip (Python package manager).
3. Install [Ollama](https://ollama.com/) on your system to access conversational AI models.
4. Required Python libraries:
   - `customtkinter`
   - `Pillow`
   - `langchain`
   - `pymupdf`
   - `huggingface-hub`
   - `faiss-cpu`
   - `sentence-transformers`

---

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Rahul-Samedavar/Adept.git
   cd Adept
   ```

2. **Set up Python Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and Set Up Ollama:**
   - Download Ollama from  [Ollama](https://ollama.com/download). Pull one or two models from it.

5. **Run the Application:**
   ```bash
   python app.py
   ```

---

## Usage

1. Launch the application using the setup instructions.
2. Use the "Upload PDF" button to load one or more PDF files.
3. Start querying your PDFs via the chat interface.
4. Use change model button to select a different model.

---

## Screenshot


![Screenshot Placeholder](assets/screenshot.png)

---

## File Structure

- `app.py`: Main application file.
- `util.py`: Helper functions for embedding, PDF parsing, and model setup.
- `assets/`: Contains application assets (icons, images, etc.).
- `requirements.txt`: List of Python dependencies.

---

## Contribution

Feel free to fork the repository and submit pull requests to contribute to this project.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Credits

- Powered by [LangChain](https://www.langchain.com).
- GUI designed with [CustomTkinter](https://customtkinter.tomschimansky.com).

