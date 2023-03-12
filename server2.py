from fastapi import FastAPI, Request, Form, File, UploadFile

from PIL import Image
from io import BytesIO
import json
from pathlib import Path

from typing import Union


app = FastAPI(title='Wallpapers recommendation system.')

#model = Img2VecResnet18()



@app.get('/')
async def home(request: Request):
    """ Returns barebones HTML form allowing the user to select a file and model """

    html_content = '''
    <form method="post" enctype="multipart/form-data">
        <div>
            <label>Upload Image</label>
            <input name="file" type="file" multiple>
                <div>
                    <label>Select Net Model</label>
                        <select name="model_name">
                            <option>Resnet18</option>                            
                        </select>                       
                </div>
                <div>
                    <label>Select Number of image</label>
                        <select name="number">
                            <option>5</option>                            
                        </select> 
                </div>
        </div>
        <button type="submit">Submit</button>
    </form>
    '''
    return HTMLResponse(content=html_content, status_code=200)

