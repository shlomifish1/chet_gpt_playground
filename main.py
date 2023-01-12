
import tkinter 
from tkinter import * 
import requests 
import json

# הגדרת הפרמטרים של gpt3
url = 'https://api-gpt3.deeppavlov.ai/v1/infer'
params = {'query': ''}
headers = {'Authorization': 'Bearer YOUR_API_KEY'}

# הגדרת הפרמטרים של הממשק gui 
root = Tk()
root.title('GPT-3')
root.geometry('400x400')

# הוספת שדה טקסט שבו המשתמש יכתוב את השאלה
query_field = Entry(root, width=50, font=('Arial',14))
query_field.grid(row=1, column=1, pady=20)

# הוספת כפתור שמשמש לשליחת השאלה
submit_button = Button(root, text='Submit', font=('Arial', 14), command=lambda: getAnswer(query_field.get()))
submit_button.grid(row=1, column=2, pady=20)

# הוספת תיבת טקסט שמשמשת להצגת התשובה
answer_field = Text(root, height=10, width=50, font=('Arial',14))
answer_field.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# הפונקציה שמשמשת לשליחת השאלה לgpt3 ולהצגת התשובה
def getAnswer(query):
  params['query'] = query
  response = requests.get(url, params=params, headers=headers).json()
  answer_field.delete('1.0', END)
  answer_field.insert(END, response['answer'])

# המסך הראשי
root.mainloop()