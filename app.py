from flask import Flask, request, render_template, send_from_directory, redirect, flash, send_file
from werkzeug.utils import secure_filename
import os
import shutil
from PIL import Image
import base64
import io
import secrets
from GFPGAN import Reconstructor


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

download_location = ""
IMG = ""


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# For performing reconstruction
@app.route('/reconstruct', methods=['GET', 'POST'])
def reconstruct():
    global IMG, download_location
    # saving the image localy
    if request.method == 'POST':

        if 'filepond' not in request.files:
            flash("No file part")

        print("Current working directory:", os.getcwd())
        
        location = "GFPGAN\\inputs\\whole_imgs"
        app.config['UPLOAD'] = location

        f = request.files['filepond']

        if f == '':
            flash('No file selected!')

        filename = secure_filename(f.filename)
        print(filename)
        IMG = filename
        f.save(os.path.join(app.config['UPLOAD'], filename))

        # file_upload(location,filename)

    # Reconstructing images
    Reconstructor.Rebuild()

    ext = IMG.split('.')[1].upper()

    rs_loc = f"GFPGAN\\results\\restored_imgs\\{IMG}"
    download_location = rs_loc
    im1 = Image.open(rs_loc)
    data1 = io.BytesIO()
    if ext == 'PNG':
        im1.save(data1, 'png')
    else:
        im1.save(data1, 'jpeg')
    rs_img = base64.b64encode(data1.getvalue())

    og_loc = f"GFPGAN\inputs\whole_imgs\\{IMG}"
    im2 = Image.open(og_loc)
    data2 = io.BytesIO()
    if ext == 'PNG':
        im2.save(data2, 'png')
    else:
        im2.save(data2, 'jpeg')
    og_img = base64.b64encode(data2.getvalue())

    print("Process Completed!")

    # cleaning the folder after processing
    folder_path = 'GFPGAN\inputs\whole_imgs'
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)

    return render_template("colorize.html", img_data1=og_img.decode('utf-8'), img_data2=rs_img.decode('utf-8'))


# For performing colorization
@app.route('/colorize', methods=['GET', 'POST'])
def colorize():

    os.chdir('c:\\Users\\RAJ\\OneDrive\\Documents\\FINAL YEAR PROJECT\\New folder\\ReViltalize\\DeOldify\\')
    global download_location
    print("inside colroize")
    print(IMG)

    if IMG == "":
        print(IMG)
        flash('You need to reconstruct the image first!', 'error')
        return redirect('/')

    import sys
    sys.path.append('c:\\Users\\RAJ\\OneDrive\\Documents\\FINAL YEAR PROJECT\\New folder\\ReViltalize\\DeOldify')
    from DeOldify import imageColorizerr

    # saving the image locally
    if request.method == 'POST':
        location1 = f"..\\GFPGAN\\results\\restored_imgs\\{IMG}"
        location2 = f"test_images\\{IMG}"

        shutil.copy(location1, location2)

    # colorizing image
    imageColorizerr.colorize(IMG)

    #extracting the extension
    ext = IMG.split('.')[1].upper()

    rs_loc = f"test_images\\{IMG}"
    im1 = Image.open(rs_loc)
    data1 = io.BytesIO()
    if ext == 'PNG':
        im1.save(data1, 'png')
    else:
        im1.save(data1, 'jpeg')
    rs_img = base64.b64encode(data1.getvalue())

    og_loc = f"..\\result_images\\{IMG}"
    download_location = og_loc
    im2 = Image.open(og_loc)
    data2 = io.BytesIO()
    if ext == 'PNG':
        im2.save(data2, 'png')
    else:
        im2.save(data2, 'jpeg')
    og_img = base64.b64encode(data2.getvalue())

    return render_template("colorize.html", img_data1=og_img.decode('utf-8'), img_data2=rs_img.decode('utf-8'))


@app.route('/download')
def download_file():
    # Path to the file to be downloaded
    if download_location == "":
        flash("Something went wrong!", "warning")
        return redirect('/')
    file_path = download_location
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
