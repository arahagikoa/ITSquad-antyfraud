import easyocr

reader = easyocr.Reader(['en', 'pl']) # specify the language  
result = reader.readtext(r'E:\Projekty\for_work\ai-solution\ITSquad-antyfraud\Backend\sorted_images_021b3356-c5d3-4121-93d0-1cf37485e1e5\prawoJazdy\2.jpg')

for (bbox, text, prob) in result:
    print(f'Text: {text}, Probability: {prob}')