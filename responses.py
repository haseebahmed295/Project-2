import g4f
import os
import json
import g4f.client
from PySide6.QtCore import QObject , Signal , QThread
from PySide6.QtWidgets import QTextEdit,QPushButton,QScrollArea
import utils
from qfluentwidgets import Dialog , MessageBox
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton

class Worker(QObject):
    finished = Signal()
    part = Signal(str)
    prompt:str = None
    text_box:QTextEdit = None
    error_occurred = Signal(str)
    
    def run(self):
        try:
           for part in self.process_gpt_request(self.prompt):
            self.insert_part = part
            self.part.emit(part)
            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def process_gpt_request(self, prompt_text , model = "gpt-3.5"):
    # Load the chat history from the file
        try:
        # Try to load the chat history from the file
            if os.path.exists('chat_history.json') and os.path.getsize('chat_history.json') > 0:
                with open('chat_history.json', 'r') as f:
                    chat_history = json.load(f)
            else:
                chat_history = []
        except json.JSONDecodeError:
        # If there's an error decoding the JSON, start with an empty list
            chat_history = []
    # Prepare the messages array for the GPT API
        messages = []
        for item in chat_history:
            messages.append({"role": "user", "content": item['prompt']})
            messages.append({"role": "assistant", "content": item['response']})
        messages.append({"role": "user", "content": prompt_text})

        # Using automatic a provider for the given model
        ## Streamed completion
        client = g4f.client.Client()
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        # if model.supports_stream:
        full_response = []
        for message in response:
            yield message.choices[0].delta.content
            full_response.append(message.choices[0].delta.content)


        chat_history.append({
            'prompt': prompt_text,
            'response': full_response, # full_response
        })

        if not os.path.exists('chat_history.json'):
            with open('chat_history.json', 'w') as f:
                json.dump(chat_history, f)
        else:
            with open('chat_history.json', 'w') as f:
                json.dump(chat_history, f)

class Process_Models:

    def __init__(self , prompt_text:str , res_text_box:QTextEdit , Send_Button:QPushButton ,entry, Scroll:QScrollArea):
        self.text_box = res_text_box
        self.Input_Text = prompt_text
        self.Send_button = Send_Button
        self.entry = entry
        self.Scroll_area = Scroll
        utils.set_scroll(self.Scroll_area)
        self.setup_response_thread()

    def setup_response_thread(self):
        """
        Sets up a thread for handling responses asynchronously.
        """
        # Create a worker object
        self.worker = Worker()  # Assuming Worker class is defined elsewhere
        self.worker.text_box = self.text_box  # Assuming res_text_box is accessible here
        self.worker.prompt = self.Input_Text  # Assuming prompt_text is accessible here

        # Move worker to the thread
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.part.connect(self.show_response)
        self.worker.error_occurred.connect(self.display_error_message)

        # Start the thread
        self.thread.start()

        # Final resets
        self.Send_button.setEnabled(False)
        self.entry.spin.setVisible(True)
        self.thread.finished.connect(lambda: self.Send_button.setEnabled(True))
        self.thread.finished.connect(lambda: self.entry.spin.setVisible(False))

        return self.text_box

    def show_response(self,Part:str):
        self.worker.text_box.Stream_text(Part)
        
    def display_error_message(self, message):
        w = Dialog("Error", message)
        # QMessageBox.critical(None, "Error", message)
        # w.setWindowTitle("Error")
        # w.setText(message)
        w.exec()
        self.worker.finished.emit()


    
    def clear_chat_history(self):
        try:
            with open('chat_history.json', 'r+') as f:
                data = json.load(f)
                if not data:
                    print("No chat history")
                    return
                data.clear()
                f.seek(0)
                json.dump(data, f)
                f.truncate()
        except FileNotFoundError:
            with open('chat_history.json', 'w') as f:
                json.dump([], f)
            print("No chat history")
        except json.decoder.JSONDecodeError:
            print("Error decoding JSON")
    
